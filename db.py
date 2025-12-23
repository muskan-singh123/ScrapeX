import os
from dotenv import load_dotenv
load_dotenv()
import mysql.connector
from mysql.connector import Error

# Configuration via environment variables (loaded from .env if present)
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", 3306))
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
MYSQL_DB = os.getenv("MYSQL_DB", "scraper_db")


def get_server_connection():
    return mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        port=MYSQL_PORT,
    )


def get_connection():
    return mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB,
        port=MYSQL_PORT,
    )


def init_db():
    try:
        # create database if not exists
        server_conn = get_server_connection()
        server_cursor = server_conn.cursor()
        server_cursor.execute(f"CREATE DATABASE IF NOT EXISTS {MYSQL_DB}")
        server_cursor.close()
        server_conn.close()

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS products (
                id INT AUTO_INCREMENT PRIMARY KEY,
                product_name TEXT,
                price VARCHAR(255),
                description LONGTEXT,
                reviews VARCHAR(50),
                link TEXT,
                scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()
        cursor.close()
        conn.close()
    except Error as e:
        print("Error initializing database:", e)


def insert_products(products):
    if not products:
        return 0
    try:
        conn = get_connection()
        cursor = conn.cursor()
        sql = (
            "INSERT INTO products (product_name, price, description, reviews, link) "
            "VALUES (%s, %s, %s, %s, %s)"
        )
        data = []
        for p in products:
            data.append(
                (
                    p.get("Product_name"),
                    p.get("Prices"),
                    p.get("Description"),
                    p.get("Reviews"),
                    p.get("Links"),
                )
            )
        cursor.executemany(sql, data)
        conn.commit()
        rowcount = cursor.rowcount
        cursor.close()
        conn.close()
        return rowcount
    except Error as e:
        print("Error inserting products:", e)
        return 0
