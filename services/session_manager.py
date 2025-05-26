# services/session_manager.py

from google.adk.sessions import InMemorySessionService
from config import APP_NAME, USER_ID, SESSION_ID

# Create a NEW session service instance for this state demonstration
session_service_sm = InMemorySessionService()

# Define initial state data - example preference for blog style
initial_state_sm = {
    "preferred_blog_style": "informal"
}

# Will be used in main.py to create the session
async def get_or_create_session():
    """Retrieves or creates a session with initial state."""
    session = await session_service_sm.get_session( # <-- ADDED 'await' HERE!
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID
    )
    if session is None:
        session = await session_service_sm.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id=SESSION_ID,
            state=initial_state_sm
        )
    return session