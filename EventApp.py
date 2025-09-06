import tkinter as tk
from tkinter import messagebox
from EventManager import EventManager

class EventApp:
    def __init__(self, root, username):
        self.root = root
        self.root.title("Gestión de Micro-Eventos")
        self.root.geometry("950x500")
        self.root.configure(bg="#f0f4f8")
        self.event_manager = EventManager()
        self.username = username

        self.main_frame = tk.Frame(root, bg="#f0f4f8")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Título
        tk.Label(self.main_frame, text="Gestión de Micro-Eventos", font=("Segoe UI", 22, "bold"), bg="#f0f4f8", fg="#263445").pack(pady=(0, 20))

        # Secciones
        self.form_frame = tk.LabelFrame(self.main_frame, text="Crear/Actualizar Evento", bg="#e0e0e0", fg="#263445", font=("Segoe UI", 12, "bold"), bd=2, relief=tk.GROOVE)
        self.form_frame.pack(side=tk.LEFT, fill="y", padx=(0, 20), pady=10, ipadx=10, ipady=10)

        self.list_frame = tk.LabelFrame(self.main_frame, text="Eventos Registrados", bg="#e0e0e0", fg="#263445", font=("Segoe UI", 12, "bold"), bd=2, relief=tk.GROOVE)
        self.list_frame.pack(side=tk.RIGHT, fill="both", expand=True, pady=10, ipadx=10, ipady=10)

        self.crear_formulario_evento()
        self.crear_lista_eventos()
        self.crear_seccion_busqueda()  
        self.actualizar_lista_eventos()

    def crear_formulario_evento(self):
        label_font = ("Segoe UI", 10)
        label_fg = "#263445"

        # Campos
        tk.Label(self.form_frame, text="Nombre:", font=label_font, fg=label_fg, bg="#e0e0e0").grid(row=0, column=0, sticky="w", padx=5, pady=4)
        self.nombre_entry = tk.Entry(self.form_frame, font=label_font, bg="#fff", fg="#263445")
        self.nombre_entry.grid(row=0, column=1, sticky="we", padx=5, pady=4)

        tk.Label(self.form_frame, text="Descripción:", font=label_font, fg=label_fg, bg="#e0e0e0").grid(row=1, column=0, sticky="w", padx=5, pady=4)
        self.descripcion_entry = tk.Entry(self.form_frame, font=label_font, bg="#fff", fg="#263445")
        self.descripcion_entry.grid(row=1, column=1, sticky="we", padx=5, pady=4)

        tk.Label(self.form_frame, text="Fecha (DD-MM-YYYY):", font=label_font, fg=label_fg, bg="#e0e0e0").grid(row=2, column=0, sticky="w", padx=5, pady=4)
        self.fecha_entry = tk.Entry(self.form_frame, font=label_font, bg="#fff", fg="#263445")
        self.fecha_entry.grid(row=2, column=1, sticky="we", padx=5, pady=4)

        tk.Label(self.form_frame, text="Categoría:", font=label_font, fg=label_fg, bg="#e0e0e0").grid(row=3, column=0, sticky="w", padx=5, pady=4)
        self.categoria_entry = tk.Entry(self.form_frame, font=label_font, bg="#fff", fg="#263445")
        self.categoria_entry.grid(row=3, column=1, sticky="we", padx=5, pady=4)

        tk.Label(self.form_frame, text="Precio:", font=label_font, fg=label_fg, bg="#e0e0e0").grid(row=4, column=0, sticky="w", padx=5, pady=4)
        self.precio_entry = tk.Entry(self.form_frame, font=label_font, bg="#fff", fg="#263445")
        self.precio_entry.grid(row=4, column=1, sticky="we", padx=5, pady=4)

        tk.Label(self.form_frame, text="Cupos:", font=label_font, fg=label_fg, bg="#e0e0e0").grid(row=5, column=0, sticky="w", padx=5, pady=4)
        self.cupos_entry = tk.Entry(self.form_frame, font=label_font, bg="#fff", fg="#263445")
        self.cupos_entry.grid(row=5, column=1, sticky="we", padx=5, pady=4)

        # Botones
        button_font = ("Segoe UI", 10, "bold")
        self.crear_btn = tk.Button(self.form_frame, text="Crear Evento", command=self.guardar_evento, font=button_font, bg="#4CAF50", fg="white", relief=tk.RAISED, bd=2, padx=8, pady=4, cursor="hand2", activebackground="#388e3c")
        self.crear_btn.grid(row=6, column=0, columnspan=2, pady=(12, 4), sticky="we")

        self.cancelar_btn = tk.Button(self.form_frame, text="Cancelar", command=self.limpiar_campos, font=button_font, bg="#f44336", fg="white", relief=tk.RAISED, bd=2, padx=8, pady=4, cursor="hand2", activebackground="#c62828")
        self.cancelar_btn.grid(row=7, column=0, columnspan=2, pady=(4, 4), sticky="we")

        self.selected_event_id = None
        self.form_frame.grid_columnconfigure(1, weight=1)

    def guardar_evento(self):
        try:
            nombre = self.nombre_entry.get()
            descripcion = self.descripcion_entry.get()
            fecha = self.fecha_entry.get()
            categoria = self.categoria_entry.get()
            precio = float(self.precio_entry.get())
            cupos = int(self.cupos_entry.get())

            if not all([nombre, fecha, precio, cupos]):
                messagebox.showerror("Error", "Los campos Nombre, Fecha, Precio y Cupos son obligatorios.")
                return

            if self.selected_event_id:
                if self.event_manager.actualizar_evento(self.selected_event_id, nombre, descripcion, fecha, categoria, precio, cupos, self.username):
                    messagebox.showinfo("Éxito", f"Evento actualizado.")
                    self.crear_btn.config(text="Actualizar Evento", bg="#2196F3")
                else:
                    messagebox.showerror("Error", "No puedes editar este evento. Solo puedes editar los eventos que creaste.")
            else:
                self.event_manager.crear_evento(nombre, descripcion, fecha, categoria, precio, cupos, self.username)
                messagebox.showinfo("Éxito", f"Evento '{nombre}' creado.")
                self.crear_btn.config(text="Crear Evento", bg="#4CAF50")

            self.limpiar_campos()
            self.actualizar_lista_eventos()
        except ValueError:
            messagebox.showerror("Error", "El precio y los cupos deben ser números válidos.")

    def limpiar_campos(self):
        self.nombre_entry.delete(0, tk.END)
        self.descripcion_entry.delete(0, tk.END)
        self.fecha_entry.delete(0, tk.END)
        self.categoria_entry.delete(0, tk.END)
        self.precio_entry.delete(0, tk.END)
        self.cupos_entry.delete(0, tk.END)
        self.crear_btn.config(text="Crear Evento", bg="#4CAF50")
        self.selected_event_id = None
        if hasattr(self, 'eliminar_btn'):
            self.eliminar_btn.config(state="disabled")

    def crear_lista_eventos(self):
        self.listbox = tk.Listbox(self.list_frame, height=18, font=("Segoe UI", 10), bg="#fff", fg="#263445", selectbackground="#b3e5fc", selectforeground="#263445", bd=1, relief=tk.FLAT)
        self.listbox.pack(side="left", fill="both", expand=True, padx=(0, 8), pady=8)
        self.listbox.bind('<<ListboxSelect>>', self.seleccionar_evento)
        self.listbox.bind('<ButtonRelease-1>', self.seleccionar_evento)

        scrollbar = tk.Scrollbar(self.list_frame, orient="vertical", command=self.listbox.yview)
        scrollbar.pack(side="right", fill="y", pady=8)
        self.listbox.config(yscrollcommand=scrollbar.set)

        btn_frame = tk.Frame(self.list_frame, bg="#e0e0e0")
        btn_frame.pack(side="bottom", pady=8)

        button_font_small = ("Segoe UI", 10, "bold")
        self.eliminar_btn = tk.Button(btn_frame, text="Eliminar", command=self.eliminar_evento_seleccionado, state="disabled", font=button_font_small, bg="#f44336", fg="white", relief=tk.RAISED, bd=2, padx=8, pady=4, cursor="hand2", activebackground="#c62828")
        self.eliminar_btn.pack(side="left", padx=8)

    def crear_seccion_busqueda(self):
        search_frame = tk.LabelFrame(self.main_frame, text="Búsqueda de Eventos", bg="#e0e0e0", fg="#263445", font=("Segoe UI", 12, "bold"), bd=2, relief=tk.GROOVE)
        search_frame.pack(side=tk.TOP, fill="x", padx=5, pady=5)  # Usa pack en vez de grid
    
        tk.Label(search_frame, text="Buscar por Nombre/Categoría:", bg="#e0e0e0").pack(side=tk.LEFT, padx=5, pady=2)
        self.search_entry = tk.Entry(search_frame)
        self.search_entry.pack(side=tk.LEFT, fill="x", expand=True, padx=5, pady=2)
        tk.Button(search_frame, text="Buscar", command=self.ejecutar_busqueda).pack(side=tk.LEFT, padx=5, pady=2)
        tk.Button(search_frame, text="Mostrar Todos", command=lambda: self.actualizar_lista_eventos()).pack(side=tk.LEFT, padx=5, pady=2)
        search_frame.grid_columnconfigure(1, weight=1)

    def ejecutar_busqueda(self):
        termino = self.search_entry.get()
        self.actualizar_lista_eventos(termino)

    def actualizar_lista_eventos(self, termino_busqueda=None):
        self.listbox.delete(0, tk.END)
        if termino_busqueda:
            eventos = self.event_manager.buscar_eventos(termino_busqueda)
        else:
            eventos = self.event_manager.obtener_eventos()
            
        for evento in eventos:
            self.listbox.insert(tk.END, f"Nombre: {evento[1]} | Fecha: {evento[3]} | Categoría: {evento[4]} | Precio: {evento[5]} | Cupos: {evento[6]}")

    def seleccionar_evento(self, event=None):
        seleccion = self.listbox.curselection()
        if seleccion:
            index = seleccion[0]
            eventos_disponibles = self.event_manager.obtener_eventos()
            if index < len(eventos_disponibles):
                evento = eventos_disponibles[index]
                self.selected_event_id = evento[0]
                self.nombre_entry.delete(0, tk.END)
                self.descripcion_entry.delete(0, tk.END)
                self.fecha_entry.delete(0, tk.END)
                self.categoria_entry.delete(0, tk.END)
                self.precio_entry.delete(0, tk.END)
                self.cupos_entry.delete(0, tk.END)
                self.nombre_entry.insert(0, evento[1])
                self.descripcion_entry.insert(0, evento[2])
                self.fecha_entry.insert(0, evento[3])
                self.categoria_entry.insert(0, evento[4])
                self.precio_entry.insert(0, str(evento[5]))
                self.cupos_entry.insert(0, str(evento[6]))
                if evento[7] == self.username:
                    self.crear_btn.config(text="Actualizar Evento", bg="#2196F3")
                    self.eliminar_btn.config(state="normal")
                    self.nombre_entry.config(state="normal")
                    self.descripcion_entry.config(state="normal")
                    self.fecha_entry.config(state="normal")
                    self.categoria_entry.config(state="normal")
                    self.precio_entry.config(state="normal")
                    self.cupos_entry.config(state="normal")
                else:
                    self.crear_btn.config(text="Crear Evento", bg="#4CAF50")
                    self.eliminar_btn.config(state="disabled")
                    self.nombre_entry.config(state="disabled")
                    self.descripcion_entry.config(state="disabled")
                    self.fecha_entry.config(state="disabled")
                    self.categoria_entry.config(state="disabled")
                    self.precio_entry.config(state="disabled")
                    self.cupos_entry.config(state="disabled")
                    if event and event.type == tk.EventType.ButtonRelease:
                        messagebox.showinfo("Información", "No puedes editar o eliminar este evento. Solo puedes editar los eventos que creaste.")
            else:
                self.limpiar_campos()
                self.actualizar_lista_eventos()

    def eliminar_evento_seleccionado(self):
        seleccion = self.listbox.curselection()
        if seleccion:
            index = seleccion[0]
            eventos_disponibles = self.event_manager.obtener_eventos()
            if index < len(eventos_disponibles):
                evento = eventos_disponibles[index]
                id_a_eliminar = evento[0]
                confirmar = messagebox.askyesno("Confirmar", f"¿Estás seguro de que quieres eliminar el evento ID {id_a_eliminar}?")
                if confirmar:
                    if self.event_manager.eliminar_evento(id_a_eliminar, self.username):
                        messagebox.showinfo("Éxito", f"Evento ID {id_a_eliminar} eliminado.")
                    else:
                        messagebox.showerror("Error", "No se pudo eliminar el evento. Asegúrate de ser el creador.")
                    self.actualizar_lista_eventos()
                    self.limpiar_campos()
            else:
                self.limpiar_campos()
                self.actualizar_lista_eventos()

if __name__ == '__main__':
    root = tk.Tk()
    app = EventApp(root, "usuario_prueba")
    root.mainloop()