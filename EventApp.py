import tkinter as tk
from tkinter import messagebox
from EventManager import EventManager

class EventApp:
    def __init__(self, root, username):
        self.root = root
        self.root.title("Gestión de Micro-Eventos")
        
        self.event_manager = EventManager()
        self.username = username
        
        self.main_frame = tk.Frame(root, bg="#f0f0f0") # Fondo gris claro para el frame principal
        self.main_frame.grid(padx=10, pady=10, sticky="nsew") 
        
        root.grid_columnconfigure(0, weight=1)
        root.grid_rowconfigure(0, weight=1)

        self.crear_formulario_evento()
        self.crear_lista_eventos()
        self.actualizar_lista_eventos()

    def crear_formulario_evento(self):
        form_frame = tk.LabelFrame(self.main_frame, text="Crear/Actualizar Evento", bg="#e0e0e0", bd=2, relief=tk.GROOVE) # Estilo para LabelFrame
        form_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        # Estilo para las etiquetas (Label)
        label_font = ("Helvetica", 10)
        label_fg = "#333333" # Gris oscuro para el texto

        tk.Label(form_frame, text="Nombre:", font=label_font, fg=label_fg).grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.nombre_entry = tk.Entry(form_frame, font=("Helvetica", 10))
        self.nombre_entry.grid(row=0, column=1, sticky="we", padx=5, pady=2)

        tk.Label(form_frame, text="Descripción:", font=label_font, fg=label_fg).grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.descripcion_entry = tk.Entry(form_frame, font=("Helvetica", 10))
        self.descripcion_entry.grid(row=1, column=1, sticky="we", padx=5, pady=2)

        tk.Label(form_frame, text="Fecha (YYYY-MM-DD):", font=label_font, fg=label_fg).grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.fecha_entry = tk.Entry(form_frame, font=("Helvetica", 10))
        self.fecha_entry.grid(row=2, column=1, sticky="we", padx=5, pady=2)

        tk.Label(form_frame, text="Categoría:", font=label_font, fg=label_fg).grid(row=3, column=0, sticky="w", padx=5, pady=2)
        self.categoria_entry = tk.Entry(form_frame, font=("Helvetica", 10))
        self.categoria_entry.grid(row=3, column=1, sticky="we", padx=5, pady=2)
        
        tk.Label(form_frame, text="Precio:", font=label_font, fg=label_fg).grid(row=4, column=0, sticky="w", padx=5, pady=2)
        self.precio_entry = tk.Entry(form_frame, font=("Helvetica", 10))
        self.precio_entry.grid(row=4, column=1, sticky="we", padx=5, pady=2)
        
        tk.Label(form_frame, text="Cupos:", font=label_font, fg=label_fg).grid(row=5, column=0, sticky="w", padx=5, pady=2)
        self.cupos_entry = tk.Entry(form_frame, font=("Helvetica", 10))
        self.cupos_entry.grid(row=5, column=1, sticky="we", padx=5, pady=2)
        
        # Estilo para los botones
        button_font = ("Helvetica", 10, "bold")
        button_bg_create = "#4CAF50" # Verde para crear
        button_fg = "white"
        button_bg_cancel = "#f44336" # Rojo para cancelar
        button_bg_edit_update = "#2196F3" # Azul para editar/actualizar

        self.crear_btn = tk.Button(form_frame, text="Crear Evento", command=self.guardar_evento, font=button_font, bg=button_bg_create, fg=button_fg, relief=tk.RAISED, bd=2, padx=5, pady=2)
        self.crear_btn.grid(row=6, column=0, columnspan=2, pady=5)
        
        self.cancelar_btn = tk.Button(form_frame, text="Cancelar", command=self.limpiar_campos, font=button_font, bg=button_bg_cancel, fg=button_fg, relief=tk.RAISED, bd=2, padx=5, pady=2)
        self.cancelar_btn.grid(row=7, column=0, columnspan=2, pady=5)
        
        self.selected_event_id = None
        form_frame.grid_columnconfigure(1, weight=1)

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
                    # Cambiar color del botón a azul para indicar actualización
                    self.crear_btn.config(text="Actualizar Evento", bg="#2196F3")
                else:
                    messagebox.showerror("Error", "No puedes editar este evento. Solo puedes editar los eventos que creaste.")
            else:
                self.event_manager.crear_evento(nombre, descripcion, fecha, categoria, precio, cupos, self.username)
                messagebox.showinfo("Éxito", f"Evento '{nombre}' creado.")
                # Resetear color del botón a verde si se crea un nuevo evento
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
        
        self.crear_btn.config(text="Crear Evento", bg="#4CAF50") # Resetear a Crear Evento y color verde
        self.selected_event_id = None
        
        if hasattr(self, 'eliminar_btn'):
            self.eliminar_btn.config(state="disabled")

    def crear_lista_eventos(self):
        list_frame = tk.LabelFrame(self.main_frame, text="Eventos Registrados", bg="#e0e0e0", bd=2, relief=tk.GROOVE)
        list_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        
        self.listbox = tk.Listbox(list_frame, height=15, width=50, font=("Helvetica", 10), bg="#ffffff", fg="#333333", selectbackground="#b3e5fc", selectforeground="#000000")
        self.listbox.pack(side="left", fill="both", expand=True)
        self.listbox.bind('<<ListboxSelect>>', self.seleccionar_evento)
        
        scrollbar = tk.Scrollbar(list_frame, orient="vertical")
        scrollbar.config(command=self.listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.listbox.config(yscrollcommand=scrollbar.set)
        
        btn_frame = tk.Frame(list_frame, bg="#e0e0e0")
        btn_frame.pack(side="bottom", pady=5)
        
        button_font_small = ("Helvetica", 10, "bold")
        button_bg_del = "#f44336" # Rojo para eliminar
        button_bg_edit = "#FFC107" # Amarillo para editar
        button_fg = "white"

        self.eliminar_btn = tk.Button(btn_frame, text="Eliminar", command=self.eliminar_evento_seleccionado, state="disabled", font=button_font_small, bg=button_bg_del, fg=button_fg, relief=tk.RAISED, bd=2, padx=5, pady=2)
        self.eliminar_btn.pack(side="left", padx=5)
        
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)

    def actualizar_lista_eventos(self):
        self.listbox.delete(0, tk.END)
        eventos = self.event_manager.obtener_eventos()
        for evento in eventos:
            # Formato más claro para la lista
            self.listbox.insert(tk.END, f"ID: {evento[0]} - {evento[1]} ({evento[3]}) - Cupos: {evento[6]} - Creado por: {evento[7]}")
    
    def seleccionar_evento(self, event=None):
        seleccion = self.listbox.curselection()
        if seleccion:
            index = seleccion[0]
            eventos_disponibles = self.event_manager.obtener_eventos() # Obtener la lista actualizada
            
            # Asegurarse de que el índice sea válido
            if index < len(eventos_disponibles):
                evento = eventos_disponibles[index]
                self.selected_event_id = evento[0]
                
                # Limpiamos los campos antes de cargar los nuevos datos
                self.nombre_entry.delete(0, tk.END)
                self.descripcion_entry.delete(0, tk.END)
                self.fecha_entry.delete(0, tk.END)
                self.categoria_entry.delete(0, tk.END)
                self.precio_entry.delete(0, tk.END)
                self.cupos_entry.delete(0, tk.END)
                
                # Cargar los datos del evento
                self.nombre_entry.insert(0, evento[1])
                self.descripcion_entry.insert(0, evento[2])
                self.fecha_entry.insert(0, evento[3])
                self.categoria_entry.insert(0, evento[4])
                self.precio_entry.insert(0, str(evento[5]))
                self.cupos_entry.insert(0, str(evento[6]))
                
                # Lógica para habilitar/deshabilitar según el creador
                if evento[7] == self.username: # evento[7] es 'creado_por'
                    self.crear_btn.config(text="Actualizar Evento", bg="#2196F3") # Botón azul para actualizar
                    self.eliminar_btn.config(state="normal")
                    # Habilitar los campos de entrada
                    self.nombre_entry.config(state="normal")
                    self.descripcion_entry.config(state="normal")
                    self.fecha_entry.config(state="normal")
                    self.categoria_entry.config(state="normal")
                    self.precio_entry.config(state="normal")
                    self.cupos_entry.config(state="normal")
                else:
                    self.crear_btn.config(text="Crear Evento", bg="#4CAF50") # Resetear a Crear Evento y color verde
                    self.eliminar_btn.config(state="disabled")
                    # Deshabilitar los campos de entrada
                    self.nombre_entry.config(state="disabled")
                    self.descripcion_entry.config(state="disabled")
                    self.fecha_entry.config(state="disabled")
                    self.categoria_entry.config(state="disabled")
                    self.precio_entry.config(state="disabled")
                    self.cupos_entry.config(state="disabled")
                    messagebox.showinfo("Información", "No puedes editar o eliminar este evento. Solo puedes editar los eventos que creaste.")
            else:
                # Si el índice ya no es válido (ej. evento eliminado mientras se veía la lista)
                self.limpiar_campos() # Limpia todo y resetea el estado
                self.actualizar_lista_eventos() # Refresca la lista
    
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