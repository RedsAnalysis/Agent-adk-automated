# tools/social_media_tools.py

from google.adk.tools.tool_context import ToolContext
from typing import Dict

def generate_linkedin_post(text_content: str) -> dict:
    """
    Generates a LinkedIn post draft from the provided text content.
    Includes relevant hashtags and a call to action.

    Args:
        text_content (str): The original text (article, announcement, docs) to convert.

    Returns:
        dict: A dictionary with 'status' and the 'post_draft'.
    """
    print(f"--- Tool: generate_linkedin_post called for content of length: {len(text_content)} ---")
    if not text_content or len(text_content) < 20:
        return {"status": "error", "error_message": "Input content is too short for a meaningful LinkedIn post."}

    # Mock generation
    post_draft = (
        f"📢 New insights from our latest content! ✨\n\n"
        f"{text_content[:200].strip()}...\n\n" # Summarize first 200 chars
        f"Read more to dive deep into this topic. #AI #Marketing #ContentCreation #LinkedIn"
        f"\n\n🔗 [Link to Original Content - Placeholder]"
    )
    return {"status": "success", "post_draft": post_draft}

def generate_blog_post(text_content: str, tool_context: ToolContext) -> dict:
    """
    Generates a blog post draft from the provided text content, including a blank image space
    and a suggestion for the image type. It can also access session state.

    Args:
        text_content (str): The original text (article, announcement, docs) to convert.
        tool_context (ToolContext): ADK's context object for accessing session state.

    Returns:
        dict: A dictionary with 'status', 'blog_draft', and 'image_suggestion'.
    """
    print(f"--- Tool: generate_blog_post called for content of length: {len(text_content)} ---")
    if not text_content or len(text_content) < 50:
        return {"status": "error", "error_message": "Input content is too short for a meaningful blog post."}

    # Read from session state (e.g., preferred blog style)
    preferred_style = tool_context.state.get("preferred_blog_style", "professional")
    print(f"--- Tool: Reading state 'preferred_blog_style': {preferred_style} ---")

    # Mock generation
    blog_draft = (
        f"--- BLOG POST DRAFT ({preferred_style.capitalize()} Style) ---\n\n"
        f"# Unleashing the Power of Your Ideas\n\n"
        f"[IMAGE PLACEHOLDER: Insert a captivating image here]\n\n"
        f"{text_content[:400].strip()}...\n\n" # Use first 400 chars as body
        f"Stay tuned for more in-depth analyses!\n"
        f"-----------------------------------------"
    )

    # Suggest image type based on content (mock logic)
    image_suggestion = "Abstract representation of concepts, data visualization, or innovative tech."
    if "art" in text_content.lower():
        image_suggestion = "Creative artwork or a dynamic visual related to artistic expression."
    elif "finance" in text_content.lower():
        image_suggestion = "Financial charts, growth graphs, or illustrations of investment."

    # Example of writing to session state
    tool_context.state["last_generated_content_type"] = "blog_post"
    print(f"--- Tool: Updated state 'last_generated_content_type': blog_post ---")

    return {
        "status": "success",
        "blog_draft": blog_draft,
        "image_suggestion": image_suggestion
    }