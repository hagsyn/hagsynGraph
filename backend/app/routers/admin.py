from fastapi import APIRouter, Depends

from ..core.auth import require_admin
from ..schemas.admin import CleanupResult, StoragePolicyResponse
from ..services.storage_policy import coerce_storage_policy, load_storage_policy, run_storage_cleanup, save_storage_policy

router = APIRouter()


@router.get("/api/admin/storage-policy", response_model=StoragePolicyResponse)
def get_storage_policy(_: str = Depends(require_admin)):
    return StoragePolicyResponse(isAdmin=True, policy=load_storage_policy())


@router.put("/api/admin/storage-policy", response_model=StoragePolicyResponse)
def update_storage_policy(payload: dict, _: str = Depends(require_admin)):
    policy = save_storage_policy(coerce_storage_policy(payload))
    return StoragePolicyResponse(isAdmin=True, policy=policy)


@router.post("/api/admin/storage-policy/run-cleanup", response_model=CleanupResult)
def run_cleanup(_: str = Depends(require_admin)):
    policy = load_storage_policy()
    return run_storage_cleanup(policy if policy.autoCleanupEnabled else policy)
