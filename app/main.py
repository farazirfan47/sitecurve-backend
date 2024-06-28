from fastapi import FastAPI
from .api.main import api_router
from dotenv import load_dotenv
import os

if os.getenv('ENV') != 'production':
    load_dotenv()

app = FastAPI()

app.include_router(api_router)