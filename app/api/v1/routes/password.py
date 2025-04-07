from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.user import PasswordResetRequest, PasswordResetConfirm
from app.services.user import request_password_reset, confirm_password_reset

router = APIRouter()


@router.post("/password/request")
async def request_reset(data: PasswordResetRequest):
    await request_password_reset(data.email)
    return {"message": "Password reset email sent."}


@router.post("/password/confirm")
async def confirm_reset(data: PasswordResetConfirm):
    await confirm_password_reset(data.token, data.new_password)
    return {"message": "Password reset successful."}
