# utils/callbacks.py

from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse
from google.genai import types # For creating response content
from google.adk.tools.base_tool import BaseTool
from google.adk.tools.tool_context import ToolContext # <-- ADD THIS IMPORT
from typing import Optional, Dict, Any

def input_length_guardrail(
    callback_context: CallbackContext, llm_request: LlmRequest
) -> Optional[LlmResponse]:
    """
    Blocks LLM calls if the user's input text is too short.
    """
    agent_name = callback_context.agent_name
    # print(f"--- Callback: input_length_guardrail running for agent: {agent_name} ---")

    last_user_message_text = ""
    if llm_request.contents:
        for content in reversed(llm_request.contents):
            if content.role == 'user' and content.parts:
                if content.parts[0].text:
                    last_user_message_text = content.parts[0].text
                    break

    min_length = 30 # A reasonable minimum for social media content
    if len(last_user_message_text.strip()) < min_length:
        print(f"--- Callback: Input too short ({len(last_user_message_text.strip())} chars). Blocking LLM call! ---")
        callback_context.state["guardrail_input_length_triggered"] = True
        return LlmResponse(
            content=types.Content(
                role="model",
                parts=[types.Part(text=f"I need more content to generate a meaningful social media post. Please provide at least {min_length} characters.")],
            )
        )
    else:
        # print(f"--- Callback: Input length OK ({len(last_user_message_text.strip())} chars). Allowing LLM call for {agent_name}. ---")
        return None

def forbidden_topic_tool_guardrail(
    tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext
) -> Optional[Dict]:
    """
    Checks if social media content generation tools are called for a 'forbidden topic'.
    If so, blocks the tool execution.
    """
    tool_name = tool.name
    agent_name = tool_context.agent_name
    # print(f"--- Callback: forbidden_topic_tool_guardrail running for tool '{tool_name}' in agent '{agent_name}' ---")
    # print(f"--- Callback: Inspecting args: {args} ---")

    forbidden_topic = "politics" # Example of a forbidden topic
    detected_topic = None

    # Check the 'text_content' argument for forbidden keywords
    text_argument = args.get("text_content", "")
    if forbidden_topic in text_argument.lower():
        detected_topic = forbidden_topic

    if detected_topic:
        print(f"--- Callback: Detected forbidden topic '{detected_topic}'. Blocking tool execution! ---")
        tool_context.state["guardrail_forbidden_topic_triggered"] = True
        return {
            "status": "error",
            "error_message": f"Policy restriction: Content related to '{detected_topic}' is currently not allowed for social media posting."
        }
    else:
        # print(f"--- Callback: No forbidden topic found. Allowing tool '{tool_name}' to proceed. ---")
        return None