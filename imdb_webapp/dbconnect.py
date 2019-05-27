import sqlite3

def connection():
    conn=sqlite3.connect('site.db')

    c=conn.cursor()
    return c,conn

