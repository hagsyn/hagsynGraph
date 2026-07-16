# Auth Gate And Self Signup Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add self-signup, real user login, and a frontend auth gate that redirects all anonymous access to `/#login`.

**Architecture:** Replace the single shared credential flow with a persisted `User` model plus token-backed auth resolution. Keep the existing workspace shell, but gate all business routes behind frontend auth checks and dedicated `/#login` / `/#register` views.

**Tech Stack:** FastAPI, SQLAlchemy, Pydantic, SQLite, browser ES modules, pytest, Node-based frontend shell checks.

**Non-goals:** No forgot-password flow in this round; password recovery stays out of scope until a real verification channel exists.

---

## File Structure

### Backend

- Create: `backend/app/models/user.py`
- Modify: `backend/app/models/__init__.py`
- Create: `backend/app/schemas/user_auth.py`
- Modify: `backend/app/schemas/__init__.py`
- Create: `backend/app/services/auth.py`
- Modify: `backend/app/core/auth.py`
- Modify: `backend/app/routers/auth.py`
- Modify: `backend/app/core/config.py`
- Modify: `backend/tests/test_api.py`

### Frontend

- Create: `frontend/assets/js/views/auth.js`
- Modify: `frontend/assets/js/state/store.js`
- Modify: `frontend/assets/js/api/client.js`
- Modify: `frontend/assets/js/api/admin.js` only if token handling changes require it
- Modify: `frontend/assets/js/app.js`
- Modify: `frontend/tests/ui-shell.test.js`

### Docs

- Create: `docs/testing/reports/2026-07-03-auth-gate-and-self-signup-report.md`

---

### Task 1: Add User Persistence And Auth Schemas

**Files:**
- Create: `backend/app/models/user.py`
- Modify: `backend/app/models/__init__.py`
- Create: `backend/app/schemas/user_auth.py`
- Modify: `backend/app/schemas/__init__.py`
- Test: `backend/tests/test_api.py`

- [ ] **Step 1: Write the failing backend model/schema tests**

Add tests that expect registration and login payloads to exist:

```python
def test_register_route_is_registered():
    routes = {
        (getattr(route, "path", None), tuple(sorted(getattr(route, "methods", []) or [])))
        for route in app.routes
    }
    assert ("/api/auth/register", ("POST",)) in routes


def test_auth_me_route_is_registered():
    routes = {
        (getattr(route, "path", None), tuple(sorted(getattr(route, "methods", []) or [])))
        for route in app.routes
    }
    assert ("/api/auth/me", ("GET",)) in routes
```

- [ ] **Step 2: Run tests to verify they fail**

Run:

```bash
cd /Users/hagsyn/ai/workspace/Hagsyn-Graph/backend
.venv/bin/pytest backend/tests/test_api.py::test_register_route_is_registered backend/tests/test_api.py::test_auth_me_route_is_registered -q
```

Expected: fail because the routes are not implemented yet.

- [ ] **Step 3: Create the user model**

Create `backend/app/models/user.py`:

```python
from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from ..core.db import Base
from .knowledge import new_id


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=lambda: new_id("user"))
    username: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    phone: Mapped[str] = mapped_column(String(32), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="active", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
```

- [ ] **Step 4: Export the user model**

Update `backend/app/models/__init__.py`:

```python
from .user import User
```

and include `User` in `__all__`.

- [ ] **Step 5: Add auth request/response schemas**

Create `backend/app/schemas/user_auth.py`:

```python
from pydantic import BaseModel, Field, field_validator


class RegisterRequest(BaseModel):
    username: str = Field(min_length=3, max_length=64)
    phone: str = Field(min_length=6, max_length=32)
    password: str = Field(min_length=8, max_length=128)
    confirmPassword: str = Field(min_length=8, max_length=128)

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized.isdigit():
            raise ValueError("Phone must contain digits only")
        return normalized


class LoginRequest(BaseModel):
    account: str = Field(min_length=1, max_length=120)
    password: str = Field(min_length=1, max_length=128)


class CurrentUserOut(BaseModel):
    id: str
    username: str
    phone: str
    status: str


class AuthSuccessOut(BaseModel):
    token: str
    user: CurrentUserOut
```

- [ ] **Step 6: Export the new auth schemas**

Update `backend/app/schemas/__init__.py`:

```python
from .user_auth import AuthSuccessOut, CurrentUserOut, LoginRequest, RegisterRequest
```

- [ ] **Step 7: Run the narrow tests again**

Run:

```bash
cd /Users/hagsyn/ai/workspace/Hagsyn-Graph/backend
.venv/bin/pytest backend/tests/test_api.py::test_register_route_is_registered backend/tests/test_api.py::test_auth_me_route_is_registered -q
```

Expected: still fail on missing routes, but model/schema import errors should be gone.

- [ ] **Step 8: Commit**

```bash
git add backend/app/models/user.py backend/app/models/__init__.py backend/app/schemas/user_auth.py backend/app/schemas/__init__.py backend/tests/test_api.py
git commit -m "feat: add user auth model and schemas"
```

---

### Task 2: Implement Registration, Login, And Token Resolution

**Files:**
- Create: `backend/app/services/auth.py`
- Modify: `backend/app/core/auth.py`
- Modify: `backend/app/routers/auth.py`
- Modify: `backend/app/core/config.py`
- Test: `backend/tests/test_api.py`

- [ ] **Step 1: Write failing auth behavior tests**

Add these tests to `backend/tests/test_api.py`:

```python
def test_register_success_returns_token_and_user():
    response = client.post("/api/auth/register", json={
        "username": "alice",
        "phone": "13800138000",
        "password": "abc12345",
        "confirmPassword": "abc12345",
    })
    assert response.status_code == 200
    payload = response.json()
    assert payload["token"]
    assert payload["user"]["username"] == "alice"
    assert payload["user"]["phone"] == "13800138000"


def test_login_supports_username_or_phone():
    register = client.post("/api/auth/register", json={
        "username": "bob",
        "phone": "13900139000",
        "password": "abc12345",
        "confirmPassword": "abc12345",
    })
    assert register.status_code == 200

    by_username = client.post("/api/auth/login", json={"account": "bob", "password": "abc12345"})
    by_phone = client.post("/api/auth/login", json={"account": "13900139000", "password": "abc12345"})

    assert by_username.status_code == 200
    assert by_phone.status_code == 200


def test_auth_me_requires_valid_user_token():
    register = client.post("/api/auth/register", json={
        "username": "charlie",
        "phone": "13700137000",
        "password": "abc12345",
        "confirmPassword": "abc12345",
    })
    token = register.json()["token"]
    response = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["username"] == "charlie"
```

- [ ] **Step 2: Run tests to verify they fail**

Run:

```bash
cd /Users/hagsyn/ai/workspace/Hagsyn-Graph/backend
.venv/bin/pytest \
  backend/tests/test_api.py::test_register_success_returns_token_and_user \
  backend/tests/test_api.py::test_login_supports_username_or_phone \
  backend/tests/test_api.py::test_auth_me_requires_valid_user_token -q
```

Expected: fail because the registration/login system does not exist yet.

- [ ] **Step 3: Add token and password helpers**

Create `backend/app/services/auth.py`:

```python
from __future__ import annotations

import hashlib
import secrets
from dataclasses import dataclass

from fastapi import HTTPException
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from ..core.config import settings
from ..models import User
from ..schemas.user_auth import CurrentUserOut


def hash_password(password: str) -> str:
    return hashlib.sha256(f"{settings.auth_token}:{password}".encode("utf-8")).hexdigest()


def validate_password_rules(*, username: str, password: str, confirm_password: str) -> None:
    if password != confirm_password:
        raise HTTPException(status_code=400, detail="Password confirmation does not match")
    if len(password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters")
    if password == username:
        raise HTTPException(status_code=400, detail="Password must not equal username")
    if not any(ch.isalpha() for ch in password) or not any(ch.isdigit() for ch in password):
        raise HTTPException(status_code=400, detail="Password must include letters and digits")


def issue_user_token(user: User) -> str:
    raw = secrets.token_hex(24)
    return f"{user.id}.{raw}"


def serialize_user(user: User) -> CurrentUserOut:
    return CurrentUserOut(id=user.id, username=user.username, phone=user.phone, status=user.status)


def lookup_user_by_account(db: Session, account: str) -> User | None:
    statement = select(User).where(or_(User.username == account, User.phone == account))
    return db.scalar(statement)
```

- [ ] **Step 4: Add token storage config**

Update `backend/app/core/config.py` to include:

```python
auth_session_file: str = "./auth_sessions.json"
```

- [ ] **Step 5: Implement auth routes against the user table**

Update `backend/app/routers/auth.py` to:

- load/store user-backed sessions
- register users
- login users
- return `GET /api/auth/me`

Use this shape:

```python
@router.post("/api/auth/register", response_model=AuthSuccessOut)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    ...


@router.post("/api/auth/login", response_model=AuthSuccessOut)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    ...


@router.get("/api/auth/me", response_model=CurrentUserOut)
def auth_me(current_user: User = Depends(require_current_user)):
    return serialize_user(current_user)
```

- [ ] **Step 6: Replace shared-token auth resolution**

Update `backend/app/core/auth.py` so that:

- `require_current_user` resolves the Bearer token to a real user
- `require_auth` becomes a compatibility wrapper that returns `current_user.username`
- `require_admin` checks the resolved user identity against admin config

Use this structure:

```python
def require_current_user(authorization: str = Header(default=""), db: Session = Depends(get_db)) -> User:
    ...


def require_auth(current_user: User = Depends(require_current_user)) -> str:
    return current_user.username
```

- [ ] **Step 7: Run the focused auth tests**

Run:

```bash
cd /Users/hagsyn/ai/workspace/Hagsyn-Graph/backend
.venv/bin/pytest \
  backend/tests/test_api.py::test_register_success_returns_token_and_user \
  backend/tests/test_api.py::test_login_supports_username_or_phone \
  backend/tests/test_api.py::test_auth_me_requires_valid_user_token -q
```

Expected: PASS.

- [ ] **Step 8: Commit**

```bash
git add backend/app/services/auth.py backend/app/core/auth.py backend/app/routers/auth.py backend/app/core/config.py backend/tests/test_api.py
git commit -m "feat: implement user registration and login"
```

---

### Task 3: Add Remaining Auth Regression Coverage

**Files:**
- Modify: `backend/tests/test_api.py`

- [ ] **Step 1: Add failing validation and permission tests**

Add:

```python
def test_register_rejects_duplicate_username():
    ...


def test_register_rejects_duplicate_phone():
    ...


def test_register_rejects_weak_password():
    ...


def test_unauthenticated_tool_route_returns_401():
    response = client.get("/api/tools/runs")
    assert response.status_code == 401
```

- [ ] **Step 2: Run the narrow tests to verify the new cases fail correctly**

Run:

```bash
cd /Users/hagsyn/ai/workspace/Hagsyn-Graph/backend
.venv/bin/pytest backend/tests/test_api.py -k "duplicate or weak_password or unauthenticated_tool_route" -q
```

Expected: any failing edge cases now point at missing validation.

- [ ] **Step 3: Adjust minimal backend validation code**

Update the registration route in `backend/app/routers/auth.py` to:

- reject duplicate usernames
- reject duplicate phones
- call `validate_password_rules(...)`

- [ ] **Step 4: Run backend full suite**

Run:

```bash
cd /Users/hagsyn/ai/workspace/Hagsyn-Graph/backend
.venv/bin/pytest -q
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add backend/tests/test_api.py backend/app/routers/auth.py
git commit -m "test: add auth validation regressions"
```

---

### Task 4: Gate The Frontend With Login And Register Routes

**Files:**
- Create: `frontend/assets/js/views/auth.js`
- Modify: `frontend/assets/js/state/store.js`
- Modify: `frontend/assets/js/api/client.js`
- Modify: `frontend/assets/js/app.js`
- Test: `frontend/tests/ui-shell.test.js`

- [ ] **Step 1: Add failing frontend shell assertions**

Extend `frontend/tests/ui-shell.test.js` with checks for:

```js
expectFile('assets/js/views/auth.js', 'missing auth view module');
expectAppIncludes("'#login'", 'missing login route handling');
expectAppIncludes("'#register'", 'missing register route handling');
expectAppIncludes('auth/me', 'missing current-user auth check');
```

- [ ] **Step 2: Run the UI shell test to verify it fails**

Run:

```bash
cd /Users/hagsyn/ai/workspace/Hagsyn-Graph
node frontend/tests/ui-shell.test.js
```

Expected: fail on missing auth view and route guard logic.

- [ ] **Step 3: Add auth view module**

Create `frontend/assets/js/views/auth.js`:

```js
export function renderAuthView({ mode }) {
  const isRegister = mode === "register";
  return `...`;
}
```

The rendered markup must include:

- login form for `/#login`
- register form for `/#register`
- visible switch links/buttons between the two
- no tool workspace content

- [ ] **Step 4: Extend frontend state**

Update `frontend/assets/js/state/store.js` to track:

```js
authUser: null,
authChecked: false,
```

- [ ] **Step 5: Add current-user and auth submit helpers**

Update `frontend/assets/js/api/client.js` with:

```js
export async function authJson(path, payload) {
  return apiRequest(path, {
    method: "POST",
    body: JSON.stringify(payload),
    headers: { "Content-Type": "application/json" },
  });
}
```

Use this from `app.js` for login/register submits and `/api/auth/me`.

- [ ] **Step 6: Add route guard and auth rendering**

Update `frontend/assets/js/app.js` so that:

- startup calls `/api/auth/me` when a token exists
- anonymous users hitting business pages redirect to `/#login`
- logged-in users hitting `/#login` or `/#register` redirect to `/#dashboard`
- auth submit success stores token and user info, then routes to `/#dashboard`
- logout clears token and user info, then routes to `/#login`

- [ ] **Step 7: Re-run the frontend shell test**

Run:

```bash
cd /Users/hagsyn/ai/workspace/Hagsyn-Graph
node frontend/tests/ui-shell.test.js
find frontend/assets/js -type f | sort | xargs -I{} node --check {}
```

Expected: PASS.

- [ ] **Step 8: Commit**

```bash
git add frontend/assets/js/views/auth.js frontend/assets/js/state/store.js frontend/assets/js/api/client.js frontend/assets/js/app.js frontend/tests/ui-shell.test.js
git commit -m "feat: add frontend auth gate and routes"
```

---

### Task 5: Verify Redirect Behavior And Update Test Report

**Files:**
- Modify: `frontend/tests/ui-shell.test.js`
- Create: `docs/testing/reports/2026-07-03-auth-gate-and-self-signup-report.md`

- [ ] **Step 1: Add explicit route guard test notes**

Record the manual/browser checks that must pass:

```text
- anonymous open / -> /#login
- anonymous open /#tools/video-compress -> /#login
- logged in open /#login -> /#dashboard
```

- [ ] **Step 2: Run backend and frontend verification**

Run:

```bash
cd /Users/hagsyn/ai/workspace/Hagsyn-Graph/backend
.venv/bin/pytest -q

cd /Users/hagsyn/ai/workspace/Hagsyn-Graph
node frontend/tests/ui-shell.test.js
find frontend/assets/js -type f | sort | xargs -I{} node --check {}
```

Expected: all pass.

- [ ] **Step 3: Write the testing report**

Create `docs/testing/reports/2026-07-03-auth-gate-and-self-signup-report.md` with:

```markdown
# 2026-07-03 Auth Gate And Self Signup Report

## Goal
- Add login/register entry gate
- Redirect anonymous access to `/#login`
- Support self-signup with username, phone, password

## Automated Verification
- `pytest -q`
- `node frontend/tests/ui-shell.test.js`
- `find frontend/assets/js -type f | sort | xargs -I{} node --check {}`

## Manual Verification
- Anonymous visit `/#dashboard` redirects to `/#login`
- Anonymous visit `/#tools/video-compress` redirects to `/#login`
- Register success enters `/#dashboard`
- Logout returns to `/#login`

## Result
- PASS / FAIL with notes
```

- [ ] **Step 4: Commit**

```bash
git add docs/testing/reports/2026-07-03-auth-gate-and-self-signup-report.md
git commit -m "docs: add auth gate test report"
```

---

## Self-Review

- Spec coverage:
  - auth gate, self-signup, redirect rules, password validation, user/token model, admin boundary, testing coverage all map to tasks above
- Placeholder scan:
  - no `TODO` / `TBD`
- Type consistency:
  - use `RegisterRequest`, `LoginRequest`, `AuthSuccessOut`, `CurrentUserOut`, `require_current_user` consistently

## Execution Handoff

Plan complete and saved to `docs/superpowers/plans/2026-07-03-auth-gate-and-self-signup-implementation.md`. Two execution options:

**1. Subagent-Driven (recommended)** - I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints

Which approach?
