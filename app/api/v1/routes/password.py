from fastapi import APIRouter, HTTPException
from app.schemas.user import PasswordResetRequest, PasswordResetConfirm
from app.services.user import request_password_reset, confirm_password_reset

router = APIRouter()

@router.post("/password/request", status_code=200, summary="Request password reset")
async def request_reset(data: PasswordResetRequest):
    """Send an email with a password reset link"""
    await request_password_reset(data.email)
    return {"message": "Password reset email sent."}

@router.post("/password/confirm", status_code=200, summary="Confirm password reset")
async def confirm_reset(data: PasswordResetConfirm):
    """Reset the password using the provided token"""
    await confirm_password_reset(data.token, data.new_password)
    return {"message": "Password reset successful."}
