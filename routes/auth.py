from fastapi import APIRouter, Depends

from config import settings
from security.auth import AuthPrincipal, get_current_principal


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.get("/whoami", response_model=dict)
async def whoami(principal: AuthPrincipal = Depends(get_current_principal)):
    return {
        "role": principal.role,
        "auth_enabled": settings.auth_enabled,
    }
