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
        project_id INTEGER NOT NULL,
        description TEXT NOT NULL,
        amount REAL NOT NULL,
        FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE
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

def add_expense(conn, project_id, description, amount):
    """ Add a new expense to the expenses table
    """
    sql = ''' INSERT INTO expenses(project_id, description, amount)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, (project_id, description, amount))
    conn.commit()
    return cur.lastrowid

def get_project(conn, project_id):
    """ Query project by id
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM projects WHERE id=?", (project_id,))
    rows = cur.fetchall()
    return rows

def get_presupuesto_restante(conn, project_id):
    """ Calculate the remaining budget for a given project """
    cur = conn.cursor()
    
    # Obtener el total gastado en el proyecto
    cur.execute("SELECT SUM(amount) FROM expenses WHERE project_id=?", (project_id,))
    result = cur.fetchone()
    total_spent = result[0] if result and result[0] is not None else 0

    # Obtener el presupuesto total del proyecto
    cur.execute("SELECT budget_total FROM projects WHERE id=?", (project_id,))
    result = cur.fetchone()
    if result and result[0] is not None:
        budget_total = result[0]
    else:
        # Aquí puedes manejar el caso en que el proyecto no existe o no tiene presupuesto asignado
        print(f"No se encontró el proyecto con ID {project_id} o no tiene un presupuesto definido.")
        return None  

    return budget_total - total_spent
