# config.py

import os
from google.adk.models.lite_llm import LiteLlm

os.environ["GOOGLE_API_KEY"] = GEMINI_API_KEY # <--- REPLACE
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "False"
MODEL_GEMINI_2_5_FLASH = "gemini/gemini-2.5-flash-preview-04-17"

# Application constants
APP_NAME = "social_media_bot_app"
USER_ID = "sm_user_1"
SESSION_ID = "sm_session_001"
