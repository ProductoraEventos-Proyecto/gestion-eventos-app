import sqlite3

class EventManager:
    def __init__(self, db_path='eventos.db'):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self._crear_tabla()

    def _crear_tabla(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS eventos (
                id INTEGER PRIMARY KEY,
                nombre TEXT NOT NULL,
                descripcion TEXT,
                fecha TEXT NOT NULL,
                categoria TEXT,
                precio_entrada REAL NOT NULL,
                cupos_disponibles INTEGER NOT NULL,
                creado_por TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def crear_evento(self, nombre, descripcion, fecha, categoria, precio, cupos, creado_por):
        self.cursor.execute('''
            INSERT INTO eventos (nombre, descripcion, fecha, categoria, precio_entrada, cupos_disponibles, creado_por)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (nombre, descripcion, fecha, categoria, precio, cupos, creado_por))
        self.conn.commit()
        return self.cursor.lastrowid

    def obtener_eventos(self):
        self.cursor.execute("SELECT * FROM eventos")
        return self.cursor.fetchall()
    
    def obtener_evento_por_id(self, id_evento):
        self.cursor.execute("SELECT * FROM eventos WHERE id=?", (id_evento,))
        return self.cursor.fetchone()

    def actualizar_evento(self, id_evento, nombre, descripcion, fecha, categoria, precio, cupos, creado_por):
        self.cursor.execute('''
            UPDATE eventos SET
            nombre = ?, descripcion = ?, fecha = ?, categoria = ?,
            precio_entrada = ?, cupos_disponibles = ?
            WHERE id = ? AND creado_por = ?
        ''', (nombre, descripcion, fecha, categoria, precio, cupos, id_evento, creado_por))
        self.conn.commit()
        return self.cursor.rowcount > 0

    def eliminar_evento(self, id_evento, creado_por):
        self.cursor.execute("DELETE FROM eventos WHERE id=? AND creado_por=?", (id_evento, creado_por))
        self.conn.commit()
        return self.cursor.rowcount > 0