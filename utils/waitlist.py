import streamlit as st
import os
import psycopg2
from datetime import datetime

def get_db_connection():
    """Get database connection."""
    return psycopg2.connect(os.getenv("DATABASE_URL"))

def init_db():
    """Initialize database table."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS waitlist (
                id SERIAL PRIMARY KEY,
                email VARCHAR(255) UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        st.error(f"Database initialization failed: {e}")

def add_to_waitlist(email: str):
    """Add email to waitlist database."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO waitlist (email) VALUES (%s) ON CONFLICT (email) DO NOTHING",
            (email,)
        )
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        st.error(f"Failed to add email: {e}")

def is_on_waitlist(email: str) -> bool:
    """Check if email exists in waitlist."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM waitlist WHERE email = %s", (email,))
        result = cur.fetchone() is not None
        cur.close()
        conn.close()
        return result
    except Exception as e:
        st.error(f"Database check failed: {e}")
        return False