
from database import (
    create_session, save_message, get_messages,
    list_sessions, delete_session
)
session_id = create_session()
print("Created:", session_id)
save_message(session_id, "user", "Hello, remember this test.")
save_message(session_id, "assistant", "I can retrieve this from PostgreSQL.")
history = get_messages(session_id)
print("Retrieved history:", history)
assert len(history) == 2
assert history[0]["role"] == "user"
assert history[1]["role"] == "assistant"
delete_session(session_id)
assert all(str(row["id"]) != session_id for row in list_sessions())
print("Database CRUD test passed.")