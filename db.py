import sqlite3
from contextlib import contextmanager

@contextmanager
def get_db_connection():
    conn = sqlite3.connect('portfolio.db')
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Create projects table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                tech_stack TEXT NOT NULL,
                github_url TEXT NOT NULL,
                category TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Clear existing data to prevent duplicates
        cursor.execute('DELETE FROM projects')
        
        # Add sample projects
        projects = [
            ('ATS-V2', 'An intelligent resume analysis system', 'Python • NLP • Machine Learning', 'https://github.com/hemanth090/ATS-V2', 'ml-ai'),
            ('Expense Tracker', 'A web application for tracking personal expenses', 'React • Node.js • MongoDB', 'https://github.com/hemanth090/expense-tracker', 'web-dev'),
            ('Multi-Chat-AI', 'A multi-model AI chat application', 'Python • OpenAI API • Streamlit', 'https://github.com/hemanth090/Multi-Chat-AI', 'ml-ai'),
            ('Portfolio Site', 'Personal portfolio website', 'HTML • CSS • JavaScript', 'https://github.com/hemanth090/Portfolio-Site', 'web-dev'),
            ('Market Analysis', 'Stock market analysis tool using Streamlit', 'Python • Streamlit • yfinance', 'https://github.com/hemanth090/MarketAnalysis', 'other')
        ]
        
        cursor.executemany('''
            INSERT INTO projects (title, description, tech_stack, github_url, category)
            VALUES (?, ?, ?, ?, ?)
        ''', projects)
        
        conn.commit()

def get_all_projects():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM projects')
        return cursor.fetchall()

def get_projects_by_category(category):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM projects WHERE category = ?', (category,))
        return cursor.fetchall()

def get_project_by_id(project_id):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM projects WHERE id = ?', (project_id,))
        return cursor.fetchone() 