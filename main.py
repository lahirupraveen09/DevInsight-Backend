# from fastapi.responses import FileResponse
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.company_main import company_main_router
from routes.download_pdf import down_pdf_router
from routes.file_handling import file_router
from routes.get_profile import profile_get_router
from routes.interact_llm import llm_router
from routes.language_checker import lan_check_router
from routes.profile import profile_router
from routes.profile_settings import profile_settings_router
from routes.response_display import response_router
from routes.submissions import submission_router
from routes.manage_portal import manage_portal_router
from routes.invite_main import invite_main_router
from routes.user_request import request_router
from routes.organization_register import organization_register_router
from routes.request_display import retrieval_router
from routes.bio_metrics import bio_metrics_router
from routes.chat_bot import chat_bot_router


app = FastAPI()

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust as per your security requirements
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(file_router, tags=["File Handling"])

app.include_router(llm_router, tags=["Interact With Language Models"])

app.include_router(lan_check_router, tags=["Language Checker"])

app.include_router(submission_router, tags=["Submissions"])

app.include_router(down_pdf_router, tags=["Download PDF"])

app.include_router(company_main_router, tags=["Company Main"])

app.include_router(request_router, tags=["Request Handling"])

app.include_router(response_router, tags=["Response Handling"])

app.include_router(retrieval_router, tags=["Retrival Data"])

app.include_router(manage_portal_router, tags=["Manager Portal"])

app.include_router(invite_main_router, tags=["Send Invites"])

app.include_router(profile_get_router, tags=["Profile"])

app.include_router(profile_router, tags=["Sign-Up"])

app.include_router(profile_settings_router, tags=["Settings"])

app.include_router(organization_register_router, tags=["Organization"])

app.include_router(bio_metrics_router, tags=["Bio Metrics"])

app.include_router(chat_bot_router, tags=["Chat Bot"])






