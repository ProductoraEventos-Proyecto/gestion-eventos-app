import sqlite3
import hashlib

class UserManager:
    def __init__(self, db_path='usuarios.db'):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self._crear_tabla_usuarios()

    def _crear_tabla_usuarios(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def crear_usuario(self, username, password):
        try:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            self.cursor.execute("INSERT INTO usuarios (username, password) VALUES (?, ?)", (username, hashed_password))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def verificar_usuario(self, username, password):
        self.cursor.execute("SELECT password FROM usuarios WHERE username=?", (username,))
        result = self.cursor.fetchone()
        
        if result:
            hashed_password = result[0]
            if hashed_password == hashlib.sha256(password.encode()).hexdigest():
                return True
        return False