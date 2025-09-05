import tkinter as tk
from tkinter import messagebox
from EventManager import EventManager

class EventApp:
    def __init__(self, root, username):
        self.root = root
        self.root.title("Gestión de Micro-Eventos")
        
        self.event_manager = EventManager()
        self.username = username
        
        self.main_frame = tk.Frame(root)
        self.main_frame.grid(padx=10, pady=10, sticky="nsew") 
        
        root.grid_columnconfigure(0, weight=1)
        root.grid_rowconfigure(0, weight=1)

        self.crear_formulario_evento()
        self.crear_lista_eventos()
        self.actualizar_lista_eventos()

    def crear_formulario_evento(self):
        form_frame = tk.LabelFrame(self.main_frame, text="Crear/Actualizar Evento")
        form_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        tk.Label(form_frame, text="Nombre:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.nombre_entry = tk.Entry(form_frame)
        self.nombre_entry.grid(row=0, column=1, sticky="we", padx=5, pady=2)

        tk.Label(form_frame, text="Descripción:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.descripcion_entry = tk.Entry(form_frame)
        self.descripcion_entry.grid(row=1, column=1, sticky="we", padx=5, pady=2)

        tk.Label(form_frame, text="Fecha (YYYY-MM-DD):").grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.fecha_entry = tk.Entry(form_frame)
        self.fecha_entry.grid(row=2, column=1, sticky="we", padx=5, pady=2)

        tk.Label(form_frame, text="Categoría:").grid(row=3, column=0, sticky="w", padx=5, pady=2)
        self.categoria_entry = tk.Entry(form_frame)
        self.categoria_entry.grid(row=3, column=1, sticky="we", padx=5, pady=2)
        
        tk.Label(form_frame, text="Precio:").grid(row=4, column=0, sticky="w", padx=5, pady=2)
        self.precio_entry = tk.Entry(form_frame)
        self.precio_entry.grid(row=4, column=1, sticky="we", padx=5, pady=2)
        
        tk.Label(form_frame, text="Cupos:").grid(row=5, column=0, sticky="w", padx=5, pady=2)
        self.cupos_entry = tk.Entry(form_frame)
        self.cupos_entry.grid(row=5, column=1, sticky="we", padx=5, pady=2)
        
        self.crear_btn = tk.Button(form_frame, text="Crear Evento", command=self.guardar_evento)
        self.crear_btn.grid(row=6, column=0, columnspan=2, pady=5)
        
        self.cancelar_btn = tk.Button(form_frame, text="Cancelar", command=self.limpiar_campos)
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
                else:
                    messagebox.showerror("Error", "No puedes editar este evento. Solo puedes editar los eventos que creaste.")
            else:
                self.event_manager.crear_evento(nombre, descripcion, fecha, categoria, precio, cupos, self.username)
                messagebox.showinfo("Éxito", f"Evento '{nombre}' creado.")

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
        self.crear_btn.config(text="Crear Evento")
        self.selected_event_id = None
        if hasattr(self, 'eliminar_btn'):
            self.eliminar_btn.config(state="disabled")
        if hasattr(self, 'editar_btn'):
            self.editar_btn.config(state="disabled")

    def crear_lista_eventos(self):
        list_frame = tk.LabelFrame(self.main_frame, text="Eventos Registrados")
        list_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        
        self.listbox = tk.Listbox(list_frame, height=15, width=50)
        self.listbox.pack(side="left", fill="both", expand=True)
        self.listbox.bind('<<ListboxSelect>>', self.seleccionar_evento)
        
        scrollbar = tk.Scrollbar(list_frame, orient="vertical")
        scrollbar.config(command=self.listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.listbox.config(yscrollcommand=scrollbar.set)
        
        btn_frame = tk.Frame(list_frame)
        btn_frame.pack(side="bottom", pady=5)
        
        self.eliminar_btn = tk.Button(btn_frame, text="Eliminar", command=self.eliminar_evento_seleccionado, state="disabled")
        self.eliminar_btn.pack(side="left", padx=5)
        self.editar_btn = tk.Button(btn_frame, text="Editar", command=self.seleccionar_evento, state="disabled")
        self.editar_btn.pack(side="left", padx=5)
        
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)

    def actualizar_lista_eventos(self):
        self.listbox.delete(0, tk.END)
        eventos = self.event_manager.obtener_eventos()
        for evento in eventos:
            self.listbox.insert(tk.END, f"ID: {evento[0]} - Nombre: {evento[1]} - Cupos: {evento[6]} - Creado por: {evento[7]}")
    
    def seleccionar_evento(self, event=None):
        seleccion = self.listbox.curselection()
        if seleccion:
            index = seleccion[0]
            evento = self.event_manager.obtener_eventos()[index]
            self.selected_event_id = evento[0]
            
            self.limpiar_campos()
            self.nombre_entry.insert(0, evento[1])
            self.descripcion_entry.insert(0, evento[2])
            self.fecha_entry.insert(0, evento[3])
            self.categoria_entry.insert(0, evento[4])
            self.precio_entry.insert(0, str(evento[5]))
            self.cupos_entry.insert(0, str(evento[6]))
            
            if evento[7] == self.username:
                self.crear_btn.config(text="Actualizar Evento")
                self.eliminar_btn.config(state="normal")
                self.editar_btn.config(state="normal")
            else:
                self.crear_btn.config(text="Crear Evento")
                self.eliminar_btn.config(state="disabled")
                self.editar_btn.config(state="disabled")
                messagebox.showinfo("Información", "No puedes editar o eliminar este evento. Solo puedes editar los eventos que creaste.")

    def eliminar_evento_seleccionado(self):
        seleccion = self.listbox.curselection()
        if seleccion:
            index = seleccion[0]
            evento = self.event_manager.obtener_eventos()[index]
            id_a_eliminar = evento[0]
            
            confirmar = messagebox.askyesno("Confirmar", f"¿Estás seguro de que quieres eliminar el evento ID {id_a_eliminar}?")
            if confirmar:
                if self.event_manager.eliminar_evento(id_a_eliminar, self.username):
                    messagebox.showinfo("Éxito", f"Evento ID {id_a_eliminar} eliminado.")
                else:
                    messagebox.showerror("Error", "No se pudo eliminar el evento. Asegúrate de ser el creador.")
                self.actualizar_lista_eventos()
                self.limpiar_campos()

if __name__ == '__main__':
    root = tk.Tk()
    app = EventApp(root, "usuario_prueba")
    root.mainloop()