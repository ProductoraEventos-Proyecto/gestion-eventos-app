import tkinter as tk
from tkinter import messagebox
from EventManager import EventManager

class EventApp:
    def __init__(self, root, username):
        self.root = root
        self.root.title("Gestión de Micro-Eventos")
        self.root.geometry("1100x600")
        self.root.configure(bg="#f5f7fa")
        
        self.event_manager = EventManager()
        self.username = username
        self.selected_event_id = None

        self.main_frame = tk.Frame(root, bg="#f5f7fa")
        self.main_frame.pack(fill="both", expand=True, padx=24, pady=24)

        tk.Label(
            self.main_frame, text="Gestión de Micro-Eventos",
            font=("Segoe UI", 24, "bold"), bg="#f5f7fa", fg="#263445"
        ).pack(pady=(0, 18))
        
        # Frame para las dos columnas (formulario y listas)
        content_frame = tk.Frame(self.main_frame, bg="#f5f7fa")
        content_frame.pack(fill="both", expand=True)

        self.form_frame = tk.LabelFrame(
            content_frame, text="Crear/Actualizar Evento",
            bg="#e3eaf2", fg="#263445", font=("Segoe UI", 13, "bold"),
            bd=2, relief=tk.GROOVE, padx=16, pady=16
        )
        self.form_frame.pack(side=tk.LEFT, fill="y", padx=(0, 24), pady=8, ipadx=8, ipady=8)

        # Frame para las dos listas de eventos y la búsqueda
        lists_and_search_frame = tk.Frame(content_frame, bg="#f5f7fa")
        lists_and_search_frame.pack(side=tk.RIGHT, fill="both", expand=True)
        
        self.crear_seccion_busqueda(lists_and_search_frame)
        self.crear_listas_eventos(lists_and_search_frame)
        self.crear_formulario_evento()
        self.actualizar_listas_eventos()
        
    def crear_formulario_evento(self):
        label_font = ("Segoe UI", 11)
        entry_font = ("Segoe UI", 11)
        label_fg = "#263445"

        campos = [
            ("Nombre:", "nombre_entry"),
            ("Descripción:", "descripcion_entry"),
            ("Fecha (DD-MM-YYYY):", "fecha_entry"),
            ("Categoría:", "categoria_entry"),
            ("Precio:", "precio_entry"),
            ("Cupos:", "cupos_entry"),
        ]
        for i, (label, attr) in enumerate(campos):
            tk.Label(self.form_frame, text=label, font=label_font, fg=label_fg, bg="#e3eaf2").grid(row=i, column=0, sticky="w", padx=6, pady=6)
            entry = tk.Entry(self.form_frame, font=entry_font, bg="#fff", fg="#263445", relief=tk.FLAT, bd=2)
            entry.grid(row=i, column=1, sticky="we", padx=6, pady=6, ipady=3)
            setattr(self, attr, entry)

        button_font = ("Segoe UI", 11, "bold")
        self.crear_btn = tk.Button(
            self.form_frame, text="Crear Evento", command=self.guardar_evento,
            font=button_font, bg="#4CAF50", fg="white", relief=tk.RAISED, bd=2,
            padx=10, pady=6, cursor="hand2", activebackground="#388e3c"
        )
        self.crear_btn.grid(row=6, column=0, columnspan=2, pady=(18, 6), sticky="we")

        self.cancelar_btn = tk.Button(
            self.form_frame, text="Cancelar", command=self.limpiar_campos,
            font=button_font, bg="#f44336", fg="white", relief=tk.RAISED, bd=2,
            padx=10, pady=6, cursor="hand2", activebackground="#c62828"
        )
        self.cancelar_btn.grid(row=7, column=0, columnspan=2, pady=(6, 6), sticky="we")

        self.form_frame.grid_columnconfigure(1, weight=1)

    def guardar_evento(self):
        nombre = self.nombre_entry.get()
        descripcion = self.descripcion_entry.get()
        fecha = self.fecha_entry.get()
        categoria = self.categoria_entry.get()
        try:
            precio = float(self.precio_entry.get())
            cupos = int(self.cupos_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Precio y cupos deben ser números válidos.")
            return

        if not nombre or not fecha or not categoria:
            messagebox.showerror("Error", "Completa todos los campos obligatorios.")
            return

        if self.selected_event_id:
            actualizado = self.event_manager.actualizar_evento(
                self.selected_event_id, nombre, descripcion, fecha, categoria, precio, cupos, self.username
            )
            if actualizado:
                messagebox.showinfo("Éxito", "Evento actualizado correctamente.")
            else:
                messagebox.showerror("Error", "No puedes editar este evento. Solo puedes editar los eventos que creaste.")
        else:
            self.event_manager.crear_evento(
                nombre, descripcion, fecha, categoria, precio, cupos, self.username
            )
            messagebox.showinfo("Éxito", "Evento creado correctamente.")

        self.limpiar_campos()
        self.actualizar_listas_eventos()
    
    def limpiar_campos(self):
        self.nombre_entry.delete(0, tk.END)
        self.descripcion_entry.delete(0, tk.END)
        self.fecha_entry.delete(0, tk.END)
        self.categoria_entry.delete(0, tk.END)
        self.precio_entry.delete(0, tk.END)
        self.cupos_entry.delete(0, tk.END)
        self.crear_btn.config(text="Crear Evento", bg="#4CAF50")
        self.selected_event_id = None
        self.eliminar_btn_mis_eventos.config(state="disabled")

    def crear_seccion_busqueda(self, parent_frame):
        search_frame = tk.LabelFrame(
            parent_frame, text="Búsqueda de Eventos",
            bg="#e3eaf2", fg="#263445", font=("Segoe UI", 13, "bold"),
            bd=2, relief=tk.GROOVE, padx=12, pady=8
        )
        search_frame.pack(side=tk.TOP, fill="x", pady=(8, 12))
        
        tk.Label(search_frame, text="Buscar por Nombre/Categoría:", bg="#e3eaf2", font=("Segoe UI", 11)).pack(side=tk.LEFT, padx=8)
        self.search_entry = tk.Entry(search_frame)
        self.search_entry.pack(side=tk.LEFT, fill="x", expand=True, padx=5, pady=2)
        self.search_entry.bind('<KeyRelease>', self.on_search_change)
        
        tk.Button(search_frame, text="Buscar", command=self.ejecutar_busqueda, font=("Segoe UI", 11, "bold"), bg="#2196F3", fg="white", relief=tk.RAISED, bd=2, padx=10, pady=4, cursor="hand2", activebackground="#1976d2").pack(side=tk.LEFT, padx=8, pady=2)

    def crear_listas_eventos(self, parent_frame):
        # Frame para las dos listas de eventos
        event_lists_frame = tk.Frame(parent_frame, bg="#f5f7fa")
        event_lists_frame.pack(fill="both", expand=True)

        # Mi lista de eventos
        my_events_frame = tk.LabelFrame(
            event_lists_frame, text="Mis Eventos",
            bg="#e3eaf2", fg="#263445", font=("Segoe UI", 13, "bold"),
            bd=2, relief=tk.GROOVE, padx=16, pady=16
        )
        my_events_frame.pack(side=tk.LEFT, fill="both", expand=True, padx=(0, 12))

        self.my_listbox = tk.Listbox(
            my_events_frame, height=18, font=("Segoe UI", 11),
            bg="#fff", fg="#263445", selectbackground="#b3e5fc",
            selectforeground="#263445", bd=1, relief=tk.FLAT
        )
        self.my_listbox.pack(side="left", fill="both", expand=True, padx=(0, 8), pady=8)
        self.my_listbox.bind('<<ListboxSelect>>', self.seleccionar_evento_propio)
        self.my_listbox.bind('<ButtonRelease-1>', self.seleccionar_evento_propio)

        scrollbar_my = tk.Scrollbar(my_events_frame, orient="vertical", command=self.my_listbox.yview)
        scrollbar_my.pack(side="right", fill="y", pady=8)
        self.my_listbox.config(yscrollcommand=scrollbar_my.set)

        btn_frame_my = tk.Frame(my_events_frame, bg="#e3eaf2")
        btn_frame_my.pack(side="bottom", pady=8)
        self.eliminar_btn_mis_eventos = tk.Button(
            btn_frame_my, text="Eliminar", command=self.eliminar_evento_seleccionado,
            state="disabled", font=("Segoe UI", 11, "bold"), bg="#f44336", fg="white",
            relief=tk.RAISED, bd=2, padx=10, pady=6, cursor="hand2", activebackground="#c62828"
        )
        self.eliminar_btn_mis_eventos.pack(side="left", padx=8)

        # Todos los eventos
        all_events_frame = tk.LabelFrame(
            event_lists_frame, text="Todos los Eventos",
            bg="#e3eaf2", fg="#263445", font=("Segoe UI", 13, "bold"),
            bd=2, relief=tk.GROOVE, padx=16, pady=16
        )
        all_events_frame.pack(side=tk.RIGHT, fill="both", expand=True, padx=(12, 0))

        self.all_listbox = tk.Listbox(
            all_events_frame, height=18, font=("Segoe UI", 11),
            bg="#fff", fg="#263445", selectbackground="#b3e5fc",
            selectforeground="#263445", bd=1, relief=tk.FLAT
        )
        self.all_listbox.pack(side="left", fill="both", expand=True, padx=(0, 8), pady=8)
        self.all_listbox.bind('<ButtonRelease-1>', self.seleccionar_evento_ajeno)

        scrollbar_all = tk.Scrollbar(all_events_frame, orient="vertical", command=self.all_listbox.yview)
        scrollbar_all.pack(side="right", fill="y", pady=8)
        self.all_listbox.config(yscrollcommand=scrollbar_all.set)

    def on_search_change(self, event=None):
        termino = self.search_entry.get()
        self.actualizar_listas_eventos(termino)

    def ejecutar_busqueda(self):
        termino = self.search_entry.get()
        self.actualizar_listas_eventos(termino)

    def actualizar_listas_eventos(self, termino_busqueda=""):
        self.my_listbox.delete(0, tk.END)
        self.all_listbox.delete(0, tk.END)

        eventos = self.event_manager.buscar_eventos(termino_busqueda)
        
        for evento in eventos:
            if evento[7] == self.username:
                self.my_listbox.insert(tk.END, f"Nombre: {evento[1]} | Fecha: {evento[3]} | Cupos: {evento[6]}")
            else:
                self.all_listbox.insert(tk.END, f"Nombre: {evento[1]} | Fecha: {evento[3]} | Cupos: {evento[6]}")

    def seleccionar_evento_propio(self, event=None):
        seleccion = self.my_listbox.curselection()
        if seleccion:
            index = seleccion[0]
            eventos_propios = [e for e in self.event_manager.obtener_eventos() if e[7] == self.username]
            
            if index < len(eventos_propios):
                evento = eventos_propios[index]
                self.selected_event_id = evento[0]
                self.cargar_datos_evento(evento, True)
            else:
                self.limpiar_campos()

    def seleccionar_evento_ajeno(self, event=None):
        seleccion = self.all_listbox.curselection()
        if seleccion:
            index = seleccion[0]
            eventos_ajenos = [e for e in self.event_manager.obtener_eventos() if e[7] != self.username]

            if index < len(eventos_ajenos):
                evento = eventos_ajenos[index]
                self.selected_event_id = evento[0]
                self.cargar_datos_evento(evento, False)
                messagebox.showinfo("Información", "No puedes editar o eliminar este evento. Solo puedes editar los eventos que creaste.")
            else:
                self.limpiar_campos()
                
    def cargar_datos_evento(self, evento, es_propio):
        self.limpiar_campos_sin_resetear_id()
        self.nombre_entry.insert(0, evento[1])
        self.descripcion_entry.insert(0, evento[2])
        self.fecha_entry.insert(0, evento[3])
        self.categoria_entry.insert(0, evento[4])
        self.precio_entry.insert(0, str(evento[5]))
        self.cupos_entry.insert(0, str(evento[6]))

        if es_propio:
            self.crear_btn.config(text="Actualizar Evento", bg="#2196F3")
            self.eliminar_btn_mis_eventos.config(state="normal")
            self.habilitar_campos()
        else:
            self.crear_btn.config(text="Crear Evento", bg="#4CAF50")
            self.eliminar_btn_mis_eventos.config(state="disabled")
            self.deshabilitar_campos()
    
    def limpiar_campos_sin_resetear_id(self):
        self.nombre_entry.delete(0, tk.END)
        self.descripcion_entry.delete(0, tk.END)
        self.fecha_entry.delete(0, tk.END)
        self.categoria_entry.delete(0, tk.END)
        self.precio_entry.delete(0, tk.END)
        self.cupos_entry.delete(0, tk.END)

    def habilitar_campos(self):
        self.nombre_entry.config(state="normal")
        self.descripcion_entry.config(state="normal")
        self.fecha_entry.config(state="normal")
        self.categoria_entry.config(state="normal")
        self.precio_entry.config(state="normal")
        self.cupos_entry.config(state="normal")

    def deshabilitar_campos(self):
        self.nombre_entry.config(state="disabled")
        self.descripcion_entry.config(state="disabled")
        self.fecha_entry.config(state="disabled")
        self.categoria_entry.config(state="disabled")
        self.precio_entry.config(state="disabled")
        self.cupos_entry.config(state="disabled")
    
    def eliminar_evento_seleccionado(self):
        seleccion = self.my_listbox.curselection()
        if seleccion:
            index = seleccion[0]
            eventos_propios = [e for e in self.event_manager.obtener_eventos() if e[7] == self.username]
            if index < len(eventos_propios):
                evento = eventos_propios[index]
                id_a_eliminar = evento[0]
                
                confirmar = messagebox.askyesno("Confirmar", f"¿Estás seguro de que quieres eliminar el evento ID {id_a_eliminar}?")
                if confirmar:
                    if self.event_manager.eliminar_evento(id_a_eliminar, self.username):
                        messagebox.showinfo("Éxito", f"Evento ID {id_a_eliminar} eliminado.")
                    else:
                        messagebox.showerror("Error", "No se pudo eliminar el evento. Asegúrate de ser el creador.")
                    self.actualizar_listas_eventos()
                    self.limpiar_campos()
            else:
                self.limpiar_campos()
                self.actualizar_listas_eventos()

if __name__ == '__main__':
    root = tk.Tk()
    app = EventApp(root, "usuario_prueba")
    root.mainloop()