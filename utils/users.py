import os
import psycopg2
from datetime import datetime

def get_db_connection():
    """Get database connection."""
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise ValueError("DATABASE_URL environment variable is not set.")
    return psycopg2.connect(db_url)

def init_db():
    """Initialize database table."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                email VARCHAR(255) UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Database initialization failed: {e}")

def add_user(email: str):
    """Add email to users database."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (email) VALUES (%s) ON CONFLICT (email) DO NOTHING",
            (email,)
        )
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Failed to add email: {e}")
        import traceback
        traceback.print_exc()

def user_exists(email: str) -> bool:
    """Check if email exists in users."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM users WHERE email = %s", (email,))
        result = cur.fetchone() is not None
        cur.close()
        conn.close()
        return result
    except Exception as e:
        print(f"Database check failed: {e}")
        return False