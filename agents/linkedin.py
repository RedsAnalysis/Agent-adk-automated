# agents/linkedin.py

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from tools.social_media_tools import generate_linkedin_post
from utils.callbacks import forbidden_topic_tool_guardrail # <-- ADD THIS IMPORT
from config import MODEL_GEMINI_2_5_FLASH

linkedin_agent = Agent(
    model=LiteLlm(model=MODEL_GEMINI_2_5_FLASH),
    name="linkedin_post_agent",
    instruction="You are the LinkedIn Post Agent. Your ONLY task is to create a professional LinkedIn post draft "
                "from provided text content using the 'generate_linkedin_post' tool. "
                "Present the generated post clearly. Do not engage in other conversations or tasks.",
    description="Specializes in converting raw text into professional LinkedIn post drafts.",
    tools=[generate_linkedin_post],
    before_tool_callback=forbidden_topic_tool_guardrail # <-- ADDED THIS LINE
)