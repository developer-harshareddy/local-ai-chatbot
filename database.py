
import os
from uuid import uuid4
from dotenv import load_dotenv
import psycopg
from psycopg.rows import dict_row
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is missing. Check your .env file.")

def get_connection():
    """Create a PostgreSQL connection."""
    return psycopg.connect(DATABASE_URL, row_factory=dict_row)

def create_session():
    """Create and return a new conversation UUID."""
    session_id = uuid4()
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO chat_sessions (id) VALUES (%s)",
            (session_id,)
        )
    return str(session_id)

def save_message(session_id, role, content):
    """Persist one user or assistant message."""
    if role not in ("user", "assistant"):
        raise ValueError("Only user and assistant messages can be saved.")
    with get_connection() as conn:
        conn.execute(
            """INSERT INTO chat_messages (session_id, role, content)
               VALUES (%s, %s, %s)""",
            (session_id, role, content)
        )

def get_messages(session_id):
    """Return messages in chronological order for the LLM."""
    with get_connection() as conn:
        rows = conn.execute(
            """SELECT role, content
               FROM chat_messages
               WHERE session_id = %s
               ORDER BY id ASC""",
            (session_id,)
        ).fetchall()
    return [{"role": row["role"], "content": row["content"]} for row in rows]

def list_sessions():
    """Return sessions newest first."""
    with get_connection() as conn:
        return conn.execute(
            """SELECT s.id, s.created_at,
                      COUNT(m.id) AS message_count
               FROM chat_sessions s
               LEFT JOIN chat_messages m ON m.session_id = s.id
               GROUP BY s.id
               ORDER BY s.created_at DESC"""
        ).fetchall()

def delete_session(session_id):
    """Delete a session; its messages are removed by ON DELETE CASCADE."""
    with get_connection() as conn:
        conn.execute(
            "DELETE FROM chat_sessions WHERE id = %s",
            (session_id,)
        )