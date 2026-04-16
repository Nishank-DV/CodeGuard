from dataclasses import dataclass
from functools import lru_cache
from typing import Callable

from fastapi import Depends, HTTPException, Query, status
from fastapi.security import APIKeyHeader

from config import settings


ALLOWED_ROLES = {"admin", "analyst", "viewer"}


@dataclass
class AuthPrincipal:
    role: str
    api_key: str


api_key_header = APIKeyHeader(name=settings.auth_header_name, auto_error=False)


@lru_cache(maxsize=1)
def _parse_auth_map() -> dict[str, str]:
    entries = [e.strip() for e in settings.auth_api_keys.split(",") if e.strip()]
    parsed: dict[str, str] = {}
    for entry in entries:
        if ":" not in entry:
            continue
        role, key = entry.split(":", 1)
        role = role.strip().lower()
        key = key.strip()
        if role in ALLOWED_ROLES and key:
            parsed[key] = role
    return parsed


def _resolve_role_from_key(api_key: str) -> str | None:
    return _parse_auth_map().get(api_key)


def resolve_role_from_key(api_key: str) -> str | None:
    return _resolve_role_from_key(api_key)


def validate_auth_configuration() -> None:
    if not settings.auth_enabled:
        return
    auth_map = _parse_auth_map()
    if not auth_map:
        raise RuntimeError("Auth is enabled but AUTH_API_KEYS is empty or invalid")
    roles_present = set(auth_map.values())
    required = {"admin", "analyst", "viewer"}
    if not required.issubset(roles_present):
        missing = sorted(required - roles_present)
        raise RuntimeError(f"AUTH_API_KEYS missing required roles: {', '.join(missing)}")


async def get_current_principal(
    api_key_header_value: str | None = Depends(api_key_header),
    api_key_query_value: str | None = Query(default=None, alias="api_key"),
) -> AuthPrincipal:
    if not settings.auth_enabled:
        return AuthPrincipal(role="admin", api_key="auth-disabled")

    api_key = api_key_header_value or api_key_query_value

    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API key",
        )

    role = _resolve_role_from_key(api_key)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )

    return AuthPrincipal(role=role, api_key=api_key)


def require_roles(*roles: str) -> Callable[[AuthPrincipal], AuthPrincipal]:
    normalized = {r.lower() for r in roles}

    async def dependency(principal: AuthPrincipal = Depends(get_current_principal)) -> AuthPrincipal:
        if principal.role not in normalized:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient role permissions",
            )
        return principal

    return dependency
