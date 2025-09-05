import tkinter as tk
from tkinter import messagebox
from UserManager import UserManager

class LoginApp:
    def __init__(self, root, on_success_callback):
        self.root = root
        self.on_success_callback = on_success_callback
        self.root.title("Iniciar Sesión / Registrarse")
        
        self.user_manager = UserManager()
        
        self.frame = tk.Frame(root)
        self.frame.pack(padx=20, pady=20)

        tk.Label(self.frame, text="Usuario:").pack()
        self.username_entry = tk.Entry(self.frame)
        self.username_entry.pack()

        tk.Label(self.frame, text="Contraseña:").pack()
        self.password_entry = tk.Entry(self.frame, show="*")
        self.password_entry.pack()

        tk.Button(self.frame, text="Iniciar Sesión", command=self.iniciar_sesion).pack(pady=5)
        tk.Button(self.frame, text="Crear Cuenta", command=self.crear_cuenta).pack(pady=5)

    def iniciar_sesion(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.user_manager.verificar_usuario(username, password):
            self.on_success_callback(username)
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")
    
    def crear_cuenta(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if not username or not password:
            messagebox.showerror("Error", "Usuario y contraseña no pueden estar vacíos.")
            return

        if self.user_manager.crear_usuario(username, password):
            messagebox.showinfo("Éxito", "¡Cuenta creada con éxito! Ahora puedes iniciar sesión.")
        else:
            messagebox.showerror("Error", "El usuario ya existe. Por favor, elige otro.")