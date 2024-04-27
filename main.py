from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database.test import db_router
from models import code_request
from routes.file_handling import file_router
from utilis.language_detector import CodeLanguageDetector
import textwrap
from utilis.generate_response import TestLLM
import logging
from models import code_context_data

CHUNK_SIZE = 20000  # Adjust based on transcript length and model limits
FILE_CONTENT = ""

app = FastAPI()

logging.basicConfig(level=logging.INFO)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust as per your security requirements
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(file_router)
app.include_router(db_router)


@app.post("/detect-language/")
async def detect_language(code_req: code_request.CodeRequest):
    supported_languages = ["python", "javascript", "java", "csharp", "cpp", "php", "ruby", "swift", "go", "typescript",
                           "html", "c"]
    if code_req.language.lower() in supported_languages:
        is_language = CodeLanguageDetector.detect_language(code_req.code, code_req.language)
        if is_language:
            return 1  # {"message": "Code is in the specified language"}
        else:
            return 2  # {"message": "Code language does not match the selected language"}
    else:
        return 3  # {"error": "Unsupported language"}


@app.post("/get_code")
def get_code(code_context: code_context_data.CodeContextData):  # Receive codeContext from the request body
    try:
        file_content = code_context.code  # Extracting data attribute from instance

        if not file_content:
            raise HTTPException(status_code=400, detail="File content is empty or not provided")

        chunks = textwrap.wrap(file_content, width=CHUNK_SIZE)
        input_chunks = chunks

        result = TestLLM.test_llm(input_chunks,code_context.language,code_context.description)

        if not result:
            raise HTTPException(status_code=500, detail="LLM test failed or returned empty result")

        print(code_context.language,code_context.description)

        return result

    except HTTPException as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
        raise http_err

    except Exception as e:
        logging.error(f"Error in get_code: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
