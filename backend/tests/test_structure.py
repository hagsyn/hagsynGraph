from importlib import import_module
from pathlib import Path


def test_backend_domain_packages_exist():
    expected_modules = [
        "app.core.auth",
        "app.core.config",
        "app.core.db",
        "app.models.knowledge",
        "app.models.tool_run",
        "app.routers.admin",
        "app.routers.auth",
        "app.routers.dashboard",
        "app.routers.health",
        "app.routers.knowledge",
        "app.routers.tools",
        "app.schemas.admin",
        "app.schemas.auth",
        "app.schemas.knowledge",
        "app.schemas.tools",
        "app.services.storage_policy",
        "app.services.tool_runs",
        "app.services.tools.subtitle",
        "app.services.tools.video",
    ]

    missing = []
    for module_name in expected_modules:
        try:
            import_module(module_name)
        except ModuleNotFoundError:
            missing.append(module_name)

    assert not missing, f"missing refactor modules: {missing}"


def test_main_is_composition_root_only():
    main_path = Path(__file__).resolve().parents[1] / "app" / "main.py"
    source = main_path.read_text(encoding="utf-8")

    assert "include_router(" in source
    assert "@app.post(" not in source
    assert "@app.get(" not in source
