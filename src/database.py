#src/database.py
import sqlite3
from sqlite3 import Error

def create_connection(db_file='database/presupuestador.db'):
    """ create a database connection to the SQLite database
        specified by db_file
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("Connection established. SQLite DB version:", sqlite3.version)
    except Error as e:
        print(e)
    return conn

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def setup_database(conn):
    """Create tables if they do not exist already in the database."""
    sql_create_projects_table = """
    CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        budget_total REAL NOT NULL
    );
    """
    sql_create_expenses_table = """
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        presupuesto_id INTEGER NOT NULL,
        description TEXT NOT NULL,
        amount REAL NOT NULL,
        FOREIGN KEY (presupuesto_id) REFERENCES projects (id) ON DELETE CASCADE
    );
    """
    create_table(conn, sql_create_projects_table)
    create_table(conn, sql_create_expenses_table)

def add_project(conn, name, budget_total):
    """ Add a new project into the projects table
    """
    sql = ''' INSERT INTO projects(name, budget_total)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, (name, budget_total))
    conn.commit()
    return cur.lastrowid

def add_expense(conn, presupuesto_id, description, amount):
    """ Add a new expense to the expenses table
    """
    sql = ''' INSERT INTO expenses(presupuesto_id, description, amount)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, (presupuesto_id, description, amount))
    conn.commit()
    return cur.lastrowid

def get_project(conn, presupuesto_id):
    """ Query project by id
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM projects WHERE id=?", (presupuesto_id,))
    rows = cur.fetchall()
    return rows

def get_presupuesto_restante(conn, presupuesto_id):
    """ Calculate the remaining budget for a given project """
    try:
        cur = conn.cursor()
        cur.execute("SELECT SUM(amount) FROM expenses WHERE presupuesto_id=?", (presupuesto_id,))
        result = cur.fetchone()
        if result[0] is None:  # Verificación mejorada para casos donde no hay gastos registrados.
            return 0
        else:
            return result[0]
    except sqlite3.OperationalError as e:
        print(f"Se produjo un error al intentar calcular el presupuesto restante: {e}")
        if "no such column" in str(e):
            print("Verifique que la columna 'presupuesto_id' existe en la tabla 'expenses'.")
        return None
