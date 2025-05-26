# agents/blog.py

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from tools.social_media_tools import generate_blog_post
from utils.callbacks import forbidden_topic_tool_guardrail # <-- ADD THIS IMPORT
from config import MODEL_GEMINI_2_5_FLASH

blog_agent = Agent(
    model=LiteLlm(model=MODEL_GEMINI_2_5_FLASH),
    name="blog_post_agent",
    instruction="You are the Blog Post Agent. Your ONLY task is to create a blog post draft "
                "from provided text content using the 'generate_blog_post' tool. "
                "Include the image placeholder and suggestion in your final output. "
                "Do not perform any other actions.",
    description="Specializes in drafting blog posts with image suggestions from raw text.",
    tools=[generate_blog_post],
    before_tool_callback=forbidden_topic_tool_guardrail # <-- ADDED THIS LINE
)