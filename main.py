# main.py

import asyncio
import logging
import sys # Import sys for exiting the script

# Configure logging to suppress INFO and DEBUG messages from ADK/LiteLLM
logging.basicConfig(level=logging.ERROR) # Only show ERROR and higher

# Imports from your project structure
from config import APP_NAME, USER_ID, SESSION_ID, MODEL_GEMINI_2_5_FLASH
from agents.coordinator import social_media_coordinator_v3
from services.session_manager import session_service_sm, get_or_create_session
from utils.agent_interaction import call_agent_async

async def main():
    print(f"--- Starting Social Media Agent Team Chatbot (Model: {MODEL_GEMINI_2_5_FLASH}) ---")
    print("Type 'exit' or 'quit' to end the conversation.")
    print("-" * 60)

    # Verify API Keys (Optional, but good for troubleshooting)
    import os
    print(f"Google API Key set: {'Yes' if os.environ.get('GOOGLE_API_KEY') and os.environ['GOOGLE_API_KEY'] != 'YOUR_GOOGLE_API_KEY' else 'No (REPLACE PLACEHOLDER!)'}")

    # Create or retrieve the session
    current_session = await get_or_create_session()
    print(f"\nSession created/retrieved: App='{APP_NAME}', User='{USER_ID}', Session='{SESSION_ID}'")
    print(f"Initial Session State: {current_session.state}")

    # Create the Runner for the root agent
    from google.adk.runners import Runner
    runner = Runner(
        agent=social_media_coordinator_v3,
        app_name=APP_NAME,
        session_service=session_service_sm
    )
    print(f"\nRunner created for agent '{runner.agent.name}'.")

    # Define a helper lambda for cleaner interaction calls
    interaction_func = lambda query: call_agent_async(query,
                                                     runner,
                                                     USER_ID,
                                                     SESSION_ID
                                                    )

    # --- Interactive Chatbot Loop ---
    while True:
        try:
            user_input = input("\nYour Query: ") # Get user input

            if user_input.lower() in ["exit", "quit"]:
                print("Ending conversation. Goodbye!")
                break # Exit the loop

            # Manually update session state for blog style (for testing purposes, as before)
            # You can remove this block if you don't want this specific manual state manipulation.
            if user_input.lower() == "set style professional":
                print("\n--- Manually Updating State: Setting preferred blog style to 'professional' ---")
                try:
                    stored_session = session_service_sm.sessions[APP_NAME][USER_ID][SESSION_ID]
                    stored_session.state["preferred_blog_style"] = "professional"
                    print(f"--- Stored session state updated. Current 'preferred_blog_style': {stored_session.state.get('preferred_blog_style', 'Not Set')} ---")
                except KeyError:
                    print(f"--- Error: Could not retrieve session for state update. ---")
                except Exception as e:
                     print(f"--- Error updating internal session state: {e} ---")
                continue # Don't process this as a regular query

            elif user_input.lower() == "set style informal":
                print("\n--- Manually Updating State: Setting preferred blog style to 'informal' ---")
                try:
                    stored_session = session_service_sm.sessions[APP_NAME][USER_ID][SESSION_ID]
                    stored_session.state["preferred_blog_style"] = "informal"
                    print(f"--- Stored session state updated. Current 'preferred_blog_style': {stored_session.state.get('preferred_blog_style', 'Not Set')} ---")
                except KeyError:
                    print(f"--- Error: Could not retrieve session for state update. ---")
                except Exception as e:
                     print(f"--- Error updating internal session state: {e} ---")
                continue # Don't process this as a regular query


            await interaction_func(user_input)

        except KeyboardInterrupt:
            print("\nEnding conversation. Goodbye!")
            break # Exit on Ctrl+C

        except Exception as e:
            print(f"\nAn error occurred during interaction: {e}")
            logging.error(f"Interaction error: {e}", exc_info=True) # Log full traceback
            print("Please try again.")


    # --- Inspect final session state after the conversation (when user exits) ---
    print("\n--- Inspecting Final Session State ---")
    final_session = await session_service_sm.get_session(app_name=APP_NAME,
                                                         user_id=USER_ID,
                                                         session_id=SESSION_ID)
    if final_session:
        print(f"Input Length Guardrail Triggered: {final_session.state.get('guardrail_input_length_triggered', 'Not Set (or False)')}")
        print(f"Forbidden Topic Guardrail Triggered: {final_session.state.get('guardrail_forbidden_topic_triggered', 'Not Set (or False)')}")
        print(f"Preferred Blog Style: {final_session.state.get('preferred_blog_style', 'Not Set')}")
        print(f"Last Generated Content Type (by tool): {final_session.state.get('last_generated_content_type', 'Not Set')}")
        # Print only the first 200 characters to avoid huge output for long posts
        last_content = final_session.state.get('last_generated_social_media_content', 'Not Set')
        if isinstance(last_content, str):
            print(f"Last Generated Social Media Content (by root agent output_key): {last_content[:200]}...")
        else:
            print(f"Last Generated Social Media Content (by root agent output_key): {last_content}")

        # print(f"Full State Dict: {final_session.state.as_dict()}") # For detailed view
    else:
        print("\n❌ Error: Could not retrieve final session state.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"\nAn error occurred during execution: {e}")
        import traceback
        traceback.print_exc()