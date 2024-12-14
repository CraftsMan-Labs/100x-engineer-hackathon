import sqlite3
from pathlib import Path

def init_db():
    db_path = Path("users.db")
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # Create users table if it doesn't exist
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create products table
    c.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT NOT NULL,
            product_name TEXT NOT NULL,
            product_description TEXT,
            domain TEXT,
            offerings TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_email) REFERENCES users(email)
        )
    ''')
    
    # Create reports table
    c.execute('''
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT NOT NULL,
            report_type TEXT NOT NULL,
            report_data TEXT NOT NULL,
            product_name TEXT,
            domain TEXT,
            offerings TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_email) REFERENCES users(email)
        )
    ''')
    
    conn.commit()
    conn.close()

def add_user(email: str, password: str) -> bool:
    try:
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('INSERT INTO users (email, password) VALUES (?, ?)', (email, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def verify_user(email: str, password: str) -> bool:
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT password FROM users WHERE email = ?', (email,))
    result = c.fetchone()
    conn.close()
    
    if result and result[0] == password:
        return True
    return False

def save_report(email: str, report_type: str, report_data: str, product_name: str, domain: str = None, offerings: str = None) -> bool:
    try:
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute(
            '''INSERT INTO reports 
               (user_email, report_type, report_data, product_name, domain, offerings) 
               VALUES (?, ?, ?, ?, ?, ?)''',
            (email, report_type, report_data, product_name, domain, offerings)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Error saving report: {e}")
        return False
    finally:
        conn.close()

def save_product(email: str, product_name: str, product_description: str, domain: str, offerings: str) -> bool:
    try:
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute(
            '''INSERT INTO products 
               (user_email, product_name, product_description, domain, offerings) 
               VALUES (?, ?, ?, ?, ?)''',
            (email, product_name, product_description, domain, offerings)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Error saving product: {e}")
        return False
    finally:
        conn.close()

def get_user_products(email: str) -> list:
    try:
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute(
            '''SELECT id, product_name, product_description, domain, offerings, created_at 
               FROM products 
               WHERE user_email = ? 
               ORDER BY created_at DESC''',
            (email,)
        )
        return c.fetchall()
    finally:
        conn.close()

def get_product_by_id(product_id: int) -> tuple:
    try:
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute(
            '''SELECT id, product_name, product_description, domain, offerings 
               FROM products 
               WHERE id = ?''',
            (product_id,)
        )
        return c.fetchone()
    finally:
        conn.close()

def get_user_reports(email: str, report_type: str = None) -> list:
    try:
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        if report_type:
            c.execute(
                '''SELECT report_type, report_data, product_name, domain, offerings, created_at 
                   FROM reports 
                   WHERE user_email = ? AND report_type = ?
                   ORDER BY created_at DESC''',
                (email, report_type)
            )
        else:
            c.execute(
                '''SELECT report_type, report_data, product_name, domain, offerings, created_at 
                   FROM reports 
                   WHERE user_email = ? 
                   ORDER BY created_at DESC''',
                (email,)
            )
        return c.fetchall()
    finally:
        conn.close()
