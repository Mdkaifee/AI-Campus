"""Authentication routes: signup, login, and current user profile."""

from fastapi import APIRouter, Depends, Header, HTTPException, status

from app.api.dependencies import get_auth_service, get_current_user_email
from app.schemas.user import AuthResponse, UserLoginRequest, UserProfile, UserSignUpRequest
from app.services.auth_service import AuthService, verify_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/signup",
    response_model=AuthResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new student account",
)
async def signup(
    payload: UserSignUpRequest,
    service: AuthService = Depends(get_auth_service),
) -> AuthResponse:
    try:
        user, token = await service.signup(payload.name, payload.email, payload.password)
        return AuthResponse(
            token=token,
            user=UserProfile(
                id=user.id,
                name=user.name,
                email=user.email,
                created_at=user.created_at,
            ),
            message="Account created successfully!",
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed. Please try again.",
        ) from exc


@router.post(
    "/login",
    response_model=AuthResponse,
    status_code=status.HTTP_200_OK,
    summary="Login to student account",
)
async def login(
    payload: UserLoginRequest,
    service: AuthService = Depends(get_auth_service),
) -> AuthResponse:
    try:
        user, token = await service.login(payload.email, payload.password)
        return AuthResponse(
            token=token,
            user=UserProfile(
                id=user.id,
                name=user.name,
                email=user.email,
                created_at=user.created_at,
            ),
            message="Logged in successfully!",
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc))
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed. Please try again.",
        ) from exc


@router.get(
    "/me",
    response_model=UserProfile,
    summary="Get current logged in user profile",
)
async def get_me(
    authorization: str = Header(None),
    service: AuthService = Depends(get_auth_service),
) -> UserProfile:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    token = authorization.split(" ", 1)[1].strip()
    payload = verify_access_token(token)
    if not payload or not payload.get("email"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

    user = await service.get_user_by_email(payload["email"])
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return UserProfile(
        id=user.id,
        name=user.name,
        email=user.email,
        created_at=user.created_at,
    )
