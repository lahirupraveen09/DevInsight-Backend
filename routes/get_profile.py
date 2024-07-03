from fastapi import APIRouter,HTTPException, Depends
from database.db import DatabaseConnector
from models.email import EmailRequest
from models.user import User, UserProfile
import logging
from utilis.profile import get_current_user, oauth2_scheme, generate_otp, send_email

profile_get_router = APIRouter()
user_db = DatabaseConnector("user")


@profile_get_router.get("/user/{email}", response_model=User)
async def get_user(email: str):
    user = await user_db.get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
@profile_get_router.get("/api/profile")
async def read_profile(current_user: dict = Depends(get_current_user)):
    return current_user

@profile_get_router.post("/api/profile/{email}")
async def create_user_profile(email: str, profile: UserProfile, token: str = Depends(oauth2_scheme)):
    try:
        await user_db.save_user_profile(email, profile.dict())
        return {"message": "Profile created/updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating/updating profile: {str(e)}")

@profile_get_router.get("/api/profile/{email}", response_model=UserProfile)
async def get_user_profile(email: str):
    user_profile = await user_db.get_user_profile_by_id(email)
    if not user_profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return user_profile

@profile_get_router.post("/api/send-email")
async def send_email_endpoint(email_request: EmailRequest):
    try:
        otp = generate_otp()
        logging.info(f"Generated OTP: {otp} for email: {email_request.email}")
        if send_email(email_request.email, otp):
            return {"message": "Email sent successfully!", "otp": otp}
        else:
            raise HTTPException(status_code=500, detail="Email sending failed.")
    except Exception as e:
        logging.error(f"Error in send_email_endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")