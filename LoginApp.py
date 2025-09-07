import tkinter as tk
from tkinter import messagebox
from UserManager import UserManager

class LoginApp:
    def __init__(self, root, on_success_callback):
        self.root = root
        self.on_success_callback = on_success_callback
        self.root.title("Bienvenido a Micro-Eventos")
        self.root.state('zoomed') 
        self.root.resizable(True, True)
        self.user_manager = UserManager()

        self.mode = 'login'  

        # Fondo principal
        self.root.configure(bg="#263445")

        # Frame principal
        self.main_frame = tk.Frame(root, bg="#263445")
        self.main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Título
        tk.Label(self.main_frame, text="Gestión de Micro-Eventos", font=("Segoe UI", 20, "bold"), bg="#263445", fg="#fff").pack(pady=(20, 10))

        # Subtítulo
        self.subtitle_label = tk.Label(self.main_frame, text="Inicia sesión o crea tu cuenta", font=("Segoe UI", 12), bg="#263445", fg="#b3e5fc")
        self.subtitle_label.pack(pady=(0, 20))

        # Frame de inputs
        input_frame = tk.Frame(self.main_frame, bg="#34495e", bd=2, relief=tk.RIDGE)
        input_frame.pack(pady=10, padx=10)

        # Usuario
        tk.Label(input_frame, text="Usuario:", font=("Segoe UI", 11), bg="#34495e", fg="#fff").grid(row=0, column=0, sticky="w", padx=8, pady=8)
        self.username_entry = tk.Entry(input_frame, font=("Segoe UI", 11), bd=1, relief=tk.FLAT, fg="#263445", bg="#f8f8f8", insertbackground="#263445")
        self.username_entry.grid(row=0, column=1, padx=8, pady=8, ipady=4)

        # Contraseña
        tk.Label(input_frame, text="Contraseña:", font=("Segoe UI", 11), bg="#34495e", fg="#fff").grid(row=1, column=0, sticky="w", padx=8, pady=8)
        self.password_entry = tk.Entry(input_frame, font=("Segoe UI", 11), show="*", bd=1, relief=tk.FLAT, fg="#263445", bg="#f8f8f8", insertbackground="#263445")
        self.password_entry.grid(row=1, column=1, padx=8, pady=8, ipady=4)

        # Botones
        button_frame = tk.Frame(self.main_frame, bg="#263445")
        button_frame.pack(pady=24)

        self.login_button = tk.Button(
            button_frame, text="Iniciar Sesión", font=("Segoe UI", 11, "bold"),
            bg="#1abc9c", fg="#fff", bd=0, relief=tk.FLAT, padx=18, pady=8,
            command=self.iniciar_sesion, cursor="hand2", activebackground="#16a085"
        )
        self.login_button.pack(side=tk.LEFT, padx=10)

        self.register_button = tk.Button(
            button_frame, text="Crear Cuenta", font=("Segoe UI", 11, "bold"),
            bg="#3498db", fg="#fff", bd=0, relief=tk.FLAT, padx=18, pady=8,
            command=self.crear_cuenta, cursor="hand2", activebackground="#2980b9"
        )
        self.register_button.pack(side=tk.LEFT, padx=10)

        self.volver_button = tk.Button(
            button_frame, text="Volver", font=("Segoe UI", 11, "bold"),
            bg="#607d8b", fg="#fff", bd=0, relief=tk.FLAT, padx=18, pady=8,
            command=self.volver_a_login, cursor="hand2", activebackground="#455a64"
        )

        self.volver_button.pack(side=tk.LEFT, padx=10)
        self.volver_button.pack_forget() 


        # Estilos de focus
        self.username_entry.bind("<FocusIn>", lambda e: self.username_entry.config(bg="#e3f2fd"))
        self.username_entry.bind("<FocusOut>", lambda e: self.username_entry.config(bg="#f8f8f8"))
        self.password_entry.bind("<FocusIn>", lambda e: self.password_entry.config(bg="#e3f2fd"))
        self.password_entry.bind("<FocusOut>", lambda e: self.password_entry.config(bg="#f8f8f8"))

    def iniciar_sesion(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.user_manager.verificar_usuario(username, password):
            self.on_success_callback(username)
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

    def crear_cuenta(self):
        self.mode = "register"
        self.subtitle_label.config(text="Creando nueva cuenta")
        self.login_button.pack_forget()
        self.register_button.config(text="Registrar", command=self.confirmar_creacion_cuenta)
        self.volver_button.pack(side=tk.LEFT, padx=10)
        
    def confirmar_creacion_cuenta(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if not username or not password:
            messagebox.showerror("Error", "Usuario y contraseña no pueden estar vacíos.")
            return

        if self.user_manager.crear_usuario(username, password):
            messagebox.showinfo("¡Éxito!", "Cuenta creada con éxito. ¡Ahora puedes iniciar sesión!")
            self.volver_a_login()
        else:
            messagebox.showerror("Error", "El usuario ya existe. Por favor, elige otro.")

    def volver_a_login(self):
        # Vuelve al modo login
        self.mode = "login"
        self.subtitle_label.config(text="Inicia sesión o crea tu cuenta")
        self.login_button.pack(side=tk.LEFT, padx=10)
        self.register_button.config(text="Crear Cuenta", command=self.crear_cuenta)
        self.volver_button.pack_forget()
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)