# agents/coordinator.py

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from agents.linkedin import linkedin_agent
from agents.blog import blog_agent
from utils.callbacks import input_length_guardrail # <-- REMOVED forbidden_topic_tool_guardrail from import
from config import MODEL_GEMINI_2_5_FLASH

social_media_coordinator_v3 = Agent(
    name="social_media_coordinator_v3_full_guardrail",
    model=LiteLlm(model=MODEL_GEMINI_2_5_FLASH),
    description="Main agent: Handles social media content generation, delegates, includes input AND tool guardrails.",
    instruction="You are the Social Media Coordinator. Your role is to convert provided text content "
                "(like an article, announcement, or document) into social media posts. "
                "If the user asks for a 'LinkedIn post' or mentions 'LinkedIn', delegate to 'linkedin_post_agent'. "
                "If the user asks for a 'blog post' or 'blog', delegate to 'blog_post_agent'. "
                "You will pass the full text content provided by the user to the delegated agent. "
                "If the request is unclear or you cannot fulfill it, politely state so.",
    tools=[], # Root agent does not have its own tools, only delegates
    sub_agents=[linkedin_agent, blog_agent],
    output_key="last_generated_social_media_content",
    before_model_callback=input_length_guardrail,
    # before_tool_callback=forbidden_topic_tool_guardrail # <-- REMOVED THIS LINE
)