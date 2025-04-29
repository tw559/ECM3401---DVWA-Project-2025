import sqlite3


def init_db(dbname: str):
    """
    This function is for establishing new SQL databases. It should only be run if a future task developed requires a new
    database.
    """

    # Connect to the database (or create it if it doesn't exist)
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()

    # Create the 'users' table if it doesn't exist, with the rows 'id', 'username' and 'password'
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')

    # Commit changes and close the connection
    conn.commit()
    conn.close()
    print("Database and 'users' table created successfully.")


if __name__ == '__main__':
    # Run to create the database, with the designed name as an argument
    init_db('task5_database.db')
