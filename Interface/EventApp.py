import tkinter as tk
from tkinter import messagebox
import sentry_sdk
from database.EventManager import EventManager
from datetime import datetime


sentry_sdk.init(
    dsn="https://f5901102ece55907110984ccdd2924a6@o4509985751629824.ingest.us.sentry.io/4509992387280906",
    # Add data like request headers and IP for users,
    # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
    send_default_pii=True,
)

class EventApp:
    def __init__(self, root, username):
        self.root = root
        self.root.title("Gestión de Micro-Eventos")
        self.root.state('zoomed')
        self.root.resizable(True, True)
        self.root.configure(bg="#263445")
        
        self.event_manager = EventManager()
        self.username = username
        self.selected_event_id = None

        self.main_frame = tk.Frame(root, bg="#263445")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Título
        tk.Label(
            self.main_frame, text="Gestión de Micro-Eventos",
            font=("Segoe UI", 20, "bold"), bg="#263445", fg="#fff"
        ).pack(pady=(20, 10))

        # Subtítulo
        self.subtitle_label = tk.Label(
            self.main_frame, text=f"Bienvenido, {self.username}",
            font=("Segoe UI", 12), bg="#263445", fg="#b3e5fc"
        )
        self.subtitle_label.pack(pady=(0, 20))
        
        # Frame para las dos columnas (formulario/registro y listas)
        content_frame_padre = tk.Frame(self.main_frame, bg="#34495e", bd=2, relief=tk.RIDGE)
        content_frame_padre.pack(pady=(10, 5), padx=10, fill=tk.BOTH, expand=True)

        # Frame para las dos listas de eventos y la búsqueda
        lists_and_search_frame = tk.Frame(content_frame_padre, bg="#34495e")
        lists_and_search_frame.pack(side=tk.RIGHT, fill="both", expand=True)
        
        # Frame para el formulario y el registro (comparten el mismo espacio)
        self.toggle_frame = tk.Frame(content_frame_padre, bg="#34495e")
        self.toggle_frame.pack(side=tk.LEFT, fill="y", padx=(0, 24), pady=8)

        # Frames para formulario y registro
        self.form_frame = tk.LabelFrame(
            self.toggle_frame, text="Crear/Actualizar Evento",
            bg="#34495e", fg="#fff", font=("Segoe UI", 13, "bold"),
            bd=2, relief=tk.GROOVE, padx=16, pady=16
        )
        
        self.registro_frame = tk.LabelFrame(
            self.toggle_frame, text="Registro",
            bg="#34495e", fg="#fff", font=("Segoe UI", 13, "bold"),
            bd=2, relief=tk.GROOVE, padx=16, pady=16
        )

        # Frame para los botones de alternancia
        btn_frame = tk.Frame(self.toggle_frame, bg="#34495e")
        btn_frame.pack(fill="x", pady=(0, 10))

        # Botones para alternar entre formulario y registro con depuración
        tk.Button(btn_frame, text="Eventos", command=self.mostrar_formulario,
            bg="#4a6a8b", fg="#fff", font=("Segoe UI", 10, "bold")
        ).pack(side="left", padx=5, pady=5)
        tk.Button(btn_frame, text="Registros", command=self.mostrar_registros,
            bg="#4a6a8b", fg="#fff", font=("Segoe UI", 10, "bold")
        ).pack(side="left", padx=5, pady=5)       
        #tk.Button(btn_frame, text="Probar Sentry", command=self.probar_sentry_error,bg="#8B0000", fg="#fff", font=("Segoe UI", 10, "bold")).pack(side="right", padx=5, pady=5)
        
        # Contenido de prueba para el formulario
        self.crear_formulario_evento()
        # Contenido de prueba para el registro
        self.crear_registros()

        # Métodos para las listas y búsqueda
        self.crear_seccion_busqueda(lists_and_search_frame)
        self.crear_listas_eventos(lists_and_search_frame)
        self.actualizar_listas_eventos()

        # Mostrar inicialmente el formulario
        print("Inicializando: Mostrando formulario por defecto")
        self.mostrar_formulario()

    def mostrar_formulario(self):
        """Muestra el formulario y oculta el registro."""
        print("Botón Formulario: Mostrando formulario")
        self.registro_frame.pack_forget()
        self.form_frame.pack(fill="y", padx=(0, 24), pady=8, ipadx=8, ipady=8)

    def mostrar_registros(self):
        """Muestra el registro y oculta el formulario."""
        print("Botón Registros: Mostrando registros")
        self.form_frame.pack_forget()
        self.registro_frame.pack(fill="y", padx=(0, 24), pady=8, ipadx=8, ipady=8)
        self.crear_registros()

    def crear_registros(self):
        # Limpiar contenido previo
        for widget in self.registro_frame.winfo_children():
            widget.destroy()

        label_font = ("Segoe UI", 11)
        label_fg = "#fff"

        eventos = self.event_manager.obtener_eventos()
        agotados = sum(1 for e in eventos if e[6] == 0)

        # Total eventos
        tk.Label(self.registro_frame, text="Total eventos registrados:", 
                 font=label_font, fg=label_fg, bg="#34495e").grid(row=0, column=0, sticky="w", padx=6, pady=6)
        tk.Label(self.registro_frame, text=len(eventos), 
                 font=label_font, fg=label_fg, bg="#34495e").grid(row=0, column=1, sticky="w", padx=6, pady=6)

        # Total agotados
        tk.Label(self.registro_frame, text="Total eventos agotados:", 
                 font=label_font, fg=label_fg, bg="#34495e").grid(row=1, column=0, sticky="w", padx=6, pady=6)
        tk.Label(self.registro_frame, text=agotados, 
                 font=label_font, fg=label_fg, bg="#34495e").grid(row=1, column=1, sticky="w", padx=6, pady=6)

        # Cupos disponibles con scroll
        tk.Label(self.registro_frame, text="Cupos disponibles:", 
                 font=label_font, fg=label_fg, bg="#34495e").grid(row=2, column=0, sticky="w", padx=6, pady=6, columnspan=2)

        # Canvas + Scrollbar
        canvas = tk.Canvas(self.registro_frame, bg="#34495e", highlightthickness=0)
        scrollbar = tk.Scrollbar(self.registro_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#34495e")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.grid(row=3, column=0, columnspan=2, sticky="nsew")
        scrollbar.grid(row=3, column=2, sticky="ns", pady=2)

        # Aseguramos que el canvas crezca con el frame
        self.registro_frame.grid_rowconfigure(3, weight=1)
        self.registro_frame.grid_columnconfigure(0, weight=1)

        # Agregamos los registros dentro del scrollable_frame
        for i, evento in enumerate(eventos):
            tk.Label(scrollable_frame, text=f"- {evento[1]}", 
                     font=label_font, fg=label_fg, bg="#34495e").grid(row=i, column=0, sticky="w", padx=6, pady=2)
            tk.Label(scrollable_frame, text=evento[6], 
                     font=label_font, fg=label_fg, bg="#34495e").grid(row=i, column=1, sticky="w", padx=6, pady=2)

    def crear_formulario_evento(self):
        label_font = ("Segoe UI", 11)
        entry_font = ("Segoe UI", 11)
        label_fg = "#fff"

        campos = [
            ("Nombre:", "nombre_entry"),
            ("Descripción:", "descripcion_entry"),
            ("Fecha (DD-MM-YYYY):", "fecha_entry"),
            ("Categoría:", "categoria_entry"),
            ("Precio:", "precio_entry"),
            ("Cupos:", "cupos_entry"),
        ]
        for i, (label, attr) in enumerate(campos):
            tk.Label(self.form_frame, text=label, font=label_font, fg=label_fg, bg="#34495e").grid(row=i, column=0, sticky="w", padx=6, pady=6)
            entry = tk.Entry(self.form_frame, font=entry_font, bg="#f8f8f8", fg="#263445", relief=tk.FLAT, bd=2)
            entry.grid(row=i, column=1, sticky="we", padx=6, pady=6, ipady=3)
            setattr(self, attr, entry)
            #

        button_font = ("Segoe UI", 11, "bold")
        self.crear_btn = tk.Button(
            self.form_frame, text="Crear Evento", command=self.guardar_evento,
            font=button_font, bg="#1abc9c", fg="white", bd=0, relief=tk.FLAT, padx=18, pady=8,
            cursor="hand2", activebackground="#16a085"
        )
        self.crear_btn.grid(row=6, column=0, columnspan=2, pady=(18, 6), sticky="we")

        self.cancelar_btn = tk.Button(
            self.form_frame, text="Cancelar", command=self.limpiar_campos,
            font=button_font, bg="#f44336", fg="white", bd=0, relief=tk.FLAT, padx=18, pady=8,
            cursor="hand2", activebackground="#c62828"
        )
        self.cancelar_btn.grid(row=7, column=0, columnspan=2, pady=(6, 6), sticky="we")


        self.form_frame.grid_columnconfigure(1, weight=1)

    def guardar_evento(self):
        try:
            nombre = self.nombre_entry.get().strip()
            descripcion = self.descripcion_entry.get().strip()
            fecha = self.fecha_entry.get().strip()
            categoria = self.categoria_entry.get().strip()
            precio = self.precio_entry.get().strip()
            cupos = self.cupos_entry.get().strip()
            
            if not descripcion or len(descripcion.strip()) < 3:
                messagebox.showerror("Error", "La descripción debe tener al menos 3 caracteres.")
                return


            try:
                datetime.strptime(fecha, "%d-%m-%Y")
            except ValueError:
                messagebox.showerror("Error", "La fecha ingresada no es válida (use formato DD-MM-YYYY)")
                return
            

            try:
                precio_val = int(precio)
                if precio_val <= 0:
                    messagebox.showerror("Error", "El precio no puede ser negativo o cero")
                    return
            except ValueError:
                messagebox.showerror("Error", "El precio debe ser un número")
                return
            
            try:
                cupos_val = int(cupos)
                if cupos_val <= 0:
                    messagebox.showerror("Error", "Los cupos no pueden ser negativos o cero")
                    return
            except ValueError:
                messagebox.showerror("Error", "Los cupos deben ser un número")
                return
            
            if not nombre or not fecha or not categoria:
                messagebox.showerror("Error", "Completa todos los campos obligatorios.")
                return

            if self.selected_event_id:
                sentry_sdk.capture_message(f"Actualizando evento ID: {self.selected_event_id}")
                actualizado = self.event_manager.actualizar_evento(
                    self.selected_event_id, nombre, descripcion, fecha, categoria, precio_val, cupos_val, self.username
                )
                if actualizado:
                    messagebox.showinfo("Éxito", "Evento actualizado correctamente.")
                else:
                    messagebox.showerror("Error", "No puedes editar este evento. Solo puedes editar los eventos que creaste.")
            else:
                sentry_sdk.capture_message("Creando nuevo evento.")
                self.event_manager.crear_evento(
                    nombre, descripcion, fecha, categoria, precio_val, cupos_val, self.username
                )
                messagebox.showinfo("Éxito", "Evento creado correctamente.")

            self.limpiar_campos()
            self.actualizar_listas_eventos()
        except Exception as e:
            # Se agregó el capture_exception para enviar el error a Sentry
            sentry_sdk.capture_exception(e)
            messagebox.showerror("Error", "Ocurrió un error inesperado al guardar el evento.")
        
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
        self.search_entry = ["","","","", ""]
        search_frame = tk.LabelFrame(
            parent_frame, text="Búsqueda de Eventos",
            bg="#34495e", fg="#fff", font=("Segoe UI", 13, "bold"),
            bd=2, relief=tk.GROOVE, padx=12, pady=8
        )
        search_frame.pack(side=tk.TOP, fill="x", pady=(8, 12))
        
        sub_frame = tk.Frame(search_frame, bg="#34495e")
        sub_frame.pack(fill="x", pady=5)

        sub_frame2 = tk.Frame(search_frame, bg="#34495e")
        sub_frame2.pack(fill="x", pady=5)

        tk.Label(sub_frame, text="Buscar por Nombre/Descripcion:", bg="#34495e", fg="#fff",font=("Segoe UI", 11)).pack(side=tk.LEFT, padx=8)
        self.search_entry0 = tk.Entry(sub_frame, font=("Segoe UI", 11), bg="#f8f8f8", fg="#263445", relief=tk.FLAT, bd=2)
        self.search_entry0.pack(side=tk.LEFT, fill="x", expand=True, padx=5, pady=2)
        self.search_entry0.bind('<KeyRelease>', self.on_search_change)

        tk.Label(sub_frame, text="Categoria:", bg="#34495e", fg="#fff",font=("Segoe UI", 11)).pack(side=tk.LEFT, padx=8)
        self.search_entry1 = tk.Entry(sub_frame, font=("Segoe UI", 11), bg="#f8f8f8", fg="#263445", relief=tk.FLAT, bd=2)
        self.search_entry1.pack(side=tk.LEFT, fill="x", expand=True, padx=5, pady=2)
        self.search_entry1.bind('<KeyRelease>', self.on_search_change)

        tk.Label(sub_frame2, text="Precio Min:", bg="#34495e", fg="#fff",font=("Segoe UI", 11)).pack(side=tk.LEFT, padx=8)
        self.search_entry2 = tk.Entry(sub_frame2, font=("Segoe UI", 11), bg="#f8f8f8", fg="#263445", relief=tk.FLAT, bd=2)
        self.search_entry2.pack(side=tk.LEFT, fill="x", expand=True, padx=5, pady=2)
        self.search_entry2.bind('<KeyRelease>', self.on_search_change)

        
        tk.Label(sub_frame2, text="Precio Max:", bg="#34495e", fg="#fff",font=("Segoe UI", 11)).pack(side=tk.LEFT, padx=8)
        self.search_entry3 = tk.Entry(sub_frame2, font=("Segoe UI", 11), bg="#f8f8f8", fg="#263445", relief=tk.FLAT, bd=2)
        self.search_entry3.pack(side=tk.LEFT, fill="x", expand=True, padx=5, pady=2)
        self.search_entry3.bind('<KeyRelease>', self.on_search_change)

        
        tk.Label(sub_frame2, text="Fecha:", bg="#34495e", fg="#fff",font=("Segoe UI", 11)).pack(side=tk.LEFT, padx=8)
        self.search_entry4 = tk.Entry(sub_frame2, font=("Segoe UI", 11), bg="#f8f8f8", fg="#263445", relief=tk.FLAT, bd=2)
        self.search_entry4.pack(side=tk.LEFT, fill="x", expand=True, padx=5, pady=2)
        self.search_entry4.bind('<KeyRelease>', self.on_search_change)

        tk.Button(
            sub_frame, text="Buscar", command=self.ejecutar_busqueda,
            font=("Segoe UI", 11, "bold"), bg="#2196F3", fg="white",
            relief=tk.FLAT, bd=0, padx=10, pady=4, cursor="hand2", activebackground="#1976d2"
        ).pack(side=tk.LEFT, padx=8, pady=2)

    def crear_listas_eventos(self, parent_frame):
        # Frame para las dos listas de eventos
        event_lists_frame = tk.Frame(parent_frame, bg="#34495e")
        event_lists_frame.pack(fill="both", expand=True)

        # Mi lista de eventos
        my_events_frame = tk.LabelFrame(
            event_lists_frame, text="Mis Eventos",
            bg="#34495e", fg="#fff", font=("Segoe UI", 13, "bold"),
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

        btn_frame_my = tk.Frame(my_events_frame, bg="#34495e")
        btn_frame_my.pack(side="bottom", pady=8)
        self.eliminar_btn_mis_eventos = tk.Button(
            btn_frame_my, text="Eliminar", command=self.eliminar_evento_seleccionado,
            state="disabled", font=("Segoe UI", 11, "bold"), bg="#f44336", fg="white",
            relief=tk.FLAT, bd=0, padx=10, pady=6, cursor="hand2", activebackground="#c62828"
        )
        self.eliminar_btn_mis_eventos.pack(side="left", padx=8)

        # Todos los eventos
        all_events_frame = tk.LabelFrame(
            event_lists_frame, text="Todos los Eventos",
            bg="#34495e", fg="#fff", font=("Segoe UI", 13, "bold"),
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
        termino = [self.search_entry0.get(), self.search_entry1.get(), self.search_entry2.get(), self.search_entry3.get(), self.search_entry4.get()]
        self.actualizar_listas_eventos(termino)

    def ejecutar_busqueda(self):
        sentry_sdk.capture_message("Búsqueda de evento activada.")
        termino = [self.search_entry0.get(), self.search_entry1.get(), self.search_entry2.get(), self.search_entry3.get(), self.search_entry4.get()]
        self.actualizar_listas_eventos(termino)

    def actualizar_listas_eventos(self, termino_busqueda=["","","","",""]):
        try:
            self.my_listbox.delete(0, tk.END)
            self.all_listbox.delete(0, tk.END)

            eventos = self.event_manager.buscar_eventos(termino_busqueda)
            
            for evento in eventos:
                if evento[7] == self.username:
                    self.my_listbox.insert(tk.END, f"Nombre: {evento[1]} | Descripción: {evento[2]}| Fecha: {evento[3]} | Precio: {evento[5]}| Cupos: {evento[6]}")
                else:
                    self.all_listbox.insert(tk.END, f"Nombre: {evento[1]} | Descripción: {evento[2]}| Fecha: {evento[3]} | Precio: {evento[5]}| Cupos: {evento[6]}")
        except Exception as e:
            # Se agregó el capture_exception para enviar el error a Sentry
            sentry_sdk.capture_exception(e)
            messagebox.showerror("Error", "No se pudieron cargar los eventos.")
    
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
                        # Se agregó el capture_message para Sentry
                        sentry_sdk.capture_message(f"Evento eliminado: {id_a_eliminar}")
                        messagebox.showinfo("Éxito", f"Evento ID {id_a_eliminar} eliminado.")
                    else:
                        sentry_sdk.capture_message(f"Advertencia: Intento fallido de eliminar el evento ID: {id_a_eliminar} por un usuario no autorizado.")
                        messagebox.showerror("Error", "No se pudo eliminar el evento. Asegúrate de ser el creador.")
                    self.actualizar_listas_eventos()
                    self.limpiar_campos()
            else:
                self.limpiar_campos()
                self.actualizar_listas_eventos()

    def probar_sentry_error(self):
        """Función para forzar un error y probar la integración con Sentry."""
        try:
            # Intencionalmente causamos un error de división por cero
            resultado = 10 / 0
        except Exception as e:
            sentry_sdk.capture_exception(e)
            messagebox.showinfo("Sentry Test", "Error de prueba enviado a Sentry. Revisa tu panel.")
    

if __name__ == '__main__':
    root = tk.Tk()
    app = EventApp(root, "usuario_prueba")
    root.mainloop()
