import psycopg2
from psycopg2.extras import RealDictCursor
from config import Config

def get_db_connection():
    conn = psycopg2.connect(
        host=Config.DB_HOST,
        database=Config.DB_NAME,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        port=Config.DB_PORT
    )
    return conn

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS murid (
            id SERIAL PRIMARY KEY,
            nama VARCHAR(100) NOT NULL,
            nilai1 FLOAT NOT NULL,
            nilai2 FLOAT NOT NULL,
            nilai3 FLOAT NOT NULL,
            rata_rata FLOAT,
            grade VARCHAR(2),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    cur.close()
    conn.close()
    print("✓ Database initialized successfully!")
