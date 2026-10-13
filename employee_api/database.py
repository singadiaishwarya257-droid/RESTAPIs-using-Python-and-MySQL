# database.py - MySQL Database Connection Management
# This module handles all database connections and operations
# Uses mysql-connector-python to communicate with MySQL

import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database configuration from environment variables
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'employee_management'),
    'port': int(os.getenv('DB_PORT', 3306))
}

def get_connection():
    """
    Creates and returns a MySQL database connection.
    
    Returns:
        mysql.connector.MySQLConnection: Active database connection
        
    Raises:
        Error: If connection cannot be established
        
    Example:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM employees")
        data = cursor.fetchall()
        cursor.close()
        conn.close()
    """
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            db_info = connection.get_server_info()
            print(f"✅ Successfully connected to MySQL Server version {db_info}")
            return connection
    except Error as e:
        if e.errno == 2003:
            print("❌ Error: Cannot connect to MySQL Server. Make sure it's running.")
        elif e.errno == 1045:
            print("❌ Error: Access denied. Check your username and password in .env")
        elif e.errno == 1049:
            print(f"❌ Error: Database '{DB_CONFIG['database']}' does not exist.")
        else:
            print(f"❌ Database Error: {e}")
        return None

def close_connection(connection):
    """
    Safely closes a database connection.
    
    Args:
        connection: The MySQL connection to close
    """
    if connection and connection.is_connected():
        connection.close()
        print("✅ Database connection closed")

def execute_query(query, params=None):
    """
    Executes a single query (INSERT, UPDATE, DELETE).
    
    Args:
        query (str): SQL query with %s placeholders
        params (tuple): Parameters to insert into query
        
    Returns:
        int: Number of rows affected, or -1 if error
        
    Example:
        result = execute_query(
            "INSERT INTO employees (name, email, department, salary) VALUES (%s, %s, %s, %s)",
            ("John", "john@email.com", "IT", 50000)
        )
    """
    connection = None
    try:
        connection = get_connection()
        if not connection:
            return -1
            
        cursor = connection.cursor()
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        connection.commit()
        affected_rows = cursor.rowcount
        cursor.close()
        return affected_rows
        
    except Error as e:
        print(f"❌ Query Error: {e}")
        return -1
    finally:
        close_connection(connection)

def fetch_query(query, params=None):
    """
    Executes a SELECT query and returns results.
    
    Args:
        query (str): SQL SELECT query with %s placeholders
        params (tuple): Parameters to insert into query
        
    Returns:
        list: List of tuples (rows), or empty list if error
        
    Example:
        results = fetch_query(
            "SELECT * FROM employees WHERE department = %s",
            ("IT",)
        )
    """
    connection = None
    try:
        connection = get_connection()
        if not connection:
            return []
            
        cursor = connection.cursor()
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        results = cursor.fetchall()
        cursor.close()
        return results
        
    except Error as e:
        print(f"❌ Query Error: {e}")
        return []
    finally:
        close_connection(connection)

def fetch_one(query, params=None):
    """
    Executes a SELECT query and returns first row only.
    
    Args:
        query (str): SQL SELECT query
        params (tuple): Parameters for the query
        
    Returns:
        tuple: Single row or None
        
    Example:
        employee = fetch_one(
            "SELECT * FROM employees WHERE id = %s",
            (1,)
        )
    """
    connection = None
    try:
        connection = get_connection()
        if not connection:
            return None
            
        cursor = connection.cursor()
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        result = cursor.fetchone()
        cursor.close()
        return result
        
    except Error as e:
        print(f"❌ Query Error: {e}")
        return None
    finally:
        close_connection(connection)

def test_connection():
    """
    Tests the database connection and prints result.
    Useful for debugging connection issues.
    """
    print("\n🔍 Testing Database Connection...")
    print(f"Host: {DB_CONFIG['host']}")
    print(f"User: {DB_CONFIG['user']}")
    print(f"Database: {DB_CONFIG['database']}")
    print(f"Port: {DB_CONFIG['port']}")
    
    connection = get_connection()
    if connection:
        close_connection(connection)
        print("✅ Connection test PASSED!\n")
        return True
    else:
        print("❌ Connection test FAILED!\n")
        return False
