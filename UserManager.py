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

    def hash_password(self, password):
        return hashlib.sha256(password.strip().encode('utf-8')).hexdigest()
    
    def crear_usuario(self, username, password):
        hashed = self.hash_password(password)
        try:
            self.cursor.execute(
                "INSERT INTO usuarios (username, password) VALUES (?, ?)",
                (username.strip(), hashed)
            )
            self.conn.commit() 
            return True
        except sqlite3.IntegrityError:
            return False

    def verificar_usuario(self, username, password):
        hashed = self.hash_password(password)
        self.cursor.execute(
            "SELECT password FROM usuarios WHERE username = ?",
            (username.strip(),)
        )
        row = self.cursor.fetchone()
        if row and row[0] == hashed:
            return True
        return False