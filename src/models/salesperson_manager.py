class SalespersonManager:
    def __init__(self, cursor, conn):
        self.cursor = cursor
        self.conn = conn

    def get_new_budget_id(self):
        new_id = self.get_next_budget_id()
        print(f"\nCreando un nuevo presupuesto con ID {new_id}\n")
        return new_id

    def get_next_budget_id(self):
        self.cursor.execute("SELECT MAX(ID_presupuesto) FROM presupuestos;")
        max_id = self.cursor.fetchone()[0]
        return max_id + 1 if max_id is not None else 1

    def list_salespeople(self):
        if not self.table_exists('vendedores'):
            print("La tabla 'vendedores' no existe. Creándola ahora...")
            self.create_vendedores_table()
        
        self.cursor.execute("SELECT ID_vendedor, Legajo_vendedor, nombre, apellido FROM vendedores;")
        vendedores = self.cursor.fetchall()
        
        if not vendedores:
            print("No hay vendedores disponibles.")
            response = input("¿Desea agregar un nuevo vendedor? (S/N): ")
            if response.strip().upper() == 'S':
                new_vendedor_id = self.agregar_vendedor()
                if new_vendedor_id:
                    self.cursor.execute("SELECT ID_vendedor, Legajo_vendedor, nombre, apellido FROM vendedores;")
                    vendedores = self.cursor.fetchall()
                else:
                    return []
            else:
                return [] 
        return vendedores

    def agregar_vendedor(self):
        print("Ingrese los datos del nuevo vendedor:")
        legajo = input("Legajo: ")
        nombre = input("Nombre: ")
        apellido = input("Apellido: ")

        try:
            sql = """
            INSERT INTO vendedores (nombre, apellido, Legajo_vendedor)
            VALUES (%s, %s, %s);
            """
            self.cursor.execute(sql, (nombre, apellido, legajo))
            self.conn.commit()
            new_vendedor_id = self.cursor.lastrowid
            print(Fore.GREEN + f"Vendedor agregado con éxito. ID asignado: {new_vendedor_id}")
            return new_vendedor_id
        except mysql.connector.Error as error:
            print(Fore.RED + f"Error al añadir vendedor: {error}")
            self.conn.rollback()
            return None

    def table_exists(self, table_name):
        self.cursor.execute(f"SHOW TABLES LIKE '{table_name}';")
        return self.cursor.fetchone() is not None

    def create_vendedores_table(self):
        try:
            self.cursor.execute("""
            CREATE TABLE vendedores (
                ID_vendedor INT AUTO_INCREMENT PRIMARY KEY,
                Legajo_vendedor INT NOT NULL,
                nombre VARCHAR(255) NOT NULL,
                apellido VARCHAR(255) NOT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
            """)
            self.conn.commit()
            print("Tabla 'vendedores' creada exitosamente.")
        except (mysql.connector.Error, mysql.connector.IntegrityError, 
                mysql.connector.ProgrammingError, mysql.connector.DatabaseError) as e:
            self.conn.rollback()
            print(f"Error al crear la tabla 'vendedores': {e}")
