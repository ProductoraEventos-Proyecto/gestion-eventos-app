import pytest
from unittest.mock import MagicMock
import tkinter as tk
from Interface.EventApp import EventApp

# ----------------- Fixture -----------------
@pytest.fixture
def app(monkeypatch):
    # Mock EventManager
    mock_event_manager = MagicMock()
    mock_root = tk.Tk()
    mock_root.withdraw()  # Evita mostrar ventana
    test_app = EventApp(mock_root, "usuario_test")
    test_app.event_manager = mock_event_manager

    # Mock messagebox
    monkeypatch.setattr("tkinter.messagebox.showerror", MagicMock())
    monkeypatch.setattr("tkinter.messagebox.showinfo", MagicMock())
    monkeypatch.setattr("tkinter.messagebox.askyesno", MagicMock(return_value=True))
    
    # Mock pack para frames de interfaz
    test_app.form_frame.pack = MagicMock()
    test_app.registro_frame.pack = MagicMock()

    yield test_app
    mock_root.destroy()

@pytest.mark.parametrize("nombre,descripcion,fecha,categoria,precio,cupos,esperado", [
    ("Concierto", "Música en vivo", "10-09-2025", "Musica", "5000", "100", True),
    ("E"*500, "Descripción larga", "10-09-2025", "Categoria", "1000", "50", True),
    ("Evento", "", "10-09-2025", "Cat", "1000", "10", False),
    ("", "Desc", "10-09-2025", "Cat", "1000", "10", False),
    ("Evento", "Desc", "32-13-2025", "Cat", "1000", "10", False),  # Fecha inválida
    ("Evento", "Desc", "10-09-2025", "Cat", "abc", "10", False),
    ("Evento", "Desc", "10-09-2025", "Cat", "1000", "abc", False),
    ("🎉Evento🎵", "🎤🎶🌟", "29-02-2024", "Entretenimiento", "2000", "50", True),
    ("EventoNeg", "Desc", "10-09-2025", "Cat", "-500", "10", False),
    ("CeroCupos", "Desc", "10-09-2025", "Cat", "100", "0", False),
])
def test_crear_eventos_varios(app, nombre, descripcion, fecha, categoria, precio, cupos, esperado):
    app.nombre_entry.delete(0, tk.END)
    app.descripcion_entry.delete(0, tk.END)
    app.fecha_entry.delete(0, tk.END)
    app.categoria_entry.delete(0, tk.END)
    app.precio_entry.delete(0, tk.END)
    app.cupos_entry.delete(0, tk.END)

    app.nombre_entry.insert(0, nombre)
    app.descripcion_entry.insert(0, descripcion)
    app.fecha_entry.insert(0, fecha)
    app.categoria_entry.insert(0, categoria)
    app.precio_entry.insert(0, precio)
    app.cupos_entry.insert(0, cupos)

    app.guardar_evento()

    if esperado:
        app.event_manager.crear_evento.assert_called()
    else:
        app.event_manager.crear_evento.assert_not_called()

# ------------------------ ACTUALIZACIÓN DE EVENTOS ------------------------
def test_actualizar_evento_valido(app):
    app.selected_event_id = 1
    app.nombre_entry.insert(0, "ConciertoMod")
    app.descripcion_entry.insert(0, "Desc Mod")
    app.fecha_entry.insert(0, "11-09-2025")
    app.categoria_entry.insert(0, "Musica")
    app.precio_entry.insert(0, "6000")
    app.cupos_entry.insert(0, "150")
    app.guardar_evento()
    app.event_manager.actualizar_evento.assert_called()

def test_actualizar_evento_nombre_vacio(app):
    app.selected_event_id = 1
    app.nombre_entry.insert(0, "")
    app.descripcion_entry.insert(0, "Desc")
    app.fecha_entry.insert(0, "10-09-2025")
    app.categoria_entry.insert(0, "Cat")
    app.precio_entry.insert(0, "1000")
    app.cupos_entry.insert(0, "10")
    app.guardar_evento()
    app.event_manager.actualizar_evento.assert_not_called()

def test_actualizar_evento_unicode(app):
    app.selected_event_id = 2
    app.nombre_entry.insert(0, "🎉EventoModificado🎵")
    app.descripcion_entry.insert(0, "🎤🎶Mod")
    app.fecha_entry.insert(0, "01-03-2024")
    app.categoria_entry.insert(0, "Entretenimiento")
    app.precio_entry.insert(0, "10")
    app.cupos_entry.insert(0, "5")
    app.guardar_evento()
    app.event_manager.actualizar_evento.assert_called()

# ------------------------ ELIMINACIÓN DE EVENTOS ------------------------
def test_eliminar_evento_propietario(app):
    app.my_listbox.curselection = MagicMock(return_value=[0])
    app.event_manager.obtener_eventos.return_value = [(1, "Evento1", "", "", "", 1000, 10, "usuario_test")]
    app.eliminar_evento_seleccionado()
    app.event_manager.eliminar_evento.assert_called()
    tk.messagebox.showinfo.assert_called()

def test_eliminar_evento_ajeno(app):
    app.my_listbox.curselection = MagicMock(return_value=[0])
    app.event_manager.obtener_eventos.return_value = [(1, "EventoAjeno", "", "", "", 1000, 10, "otro_usuario")]
    app.eliminar_evento_seleccionado()
    app.event_manager.eliminar_evento.assert_not_called()

def test_eliminar_evento_sin_seleccion(app):
    app.my_listbox.curselection = MagicMock(return_value=[])
    app.eliminar_evento_seleccionado()
    app.event_manager.eliminar_evento.assert_not_called()

# ------------------------ BÚSQUEDA ------------------------
def test_busqueda_nombre(app):
    app.search_entry0.insert(0, "Concierto")
    app.actualizar_listas_eventos = MagicMock()
    app.on_search_change()
    app.actualizar_listas_eventos.assert_called()

def test_busqueda_categoria(app):
    app.search_entry1.insert(0, "Musica")
    app.actualizar_listas_eventos = MagicMock()
    app.on_search_change()
    app.actualizar_listas_eventos.assert_called()

def test_busqueda_precio_min_max(app):
    app.search_entry2.insert(0, "1000")
    app.search_entry3.insert(0, "5000")
    app.actualizar_listas_eventos = MagicMock()
    app.on_search_change()
    app.actualizar_listas_eventos.assert_called()

def test_busqueda_fecha(app):
    app.search_entry4.insert(0, "10-09-2025")
    app.actualizar_listas_eventos = MagicMock()
    app.on_search_change()
    app.actualizar_listas_eventos.assert_called()

# ------------------------ INTERFAZ ------------------------
def test_mostrar_formulario(app):
    app.mostrar_formulario()
    assert app.form_frame.pack.called

def test_mostrar_registros(app):
    app.mostrar_registros()
    assert app.registro_frame.pack.called

def test_habilitar_campos(app):
    app.habilitar_campos()
    assert app.nombre_entry.cget("state") == "normal"

def test_deshabilitar_campos(app):
    app.deshabilitar_campos()
    assert app.nombre_entry.cget("state") == "disabled"

def test_limpiar_campos_sin_resetear_id(app):
    app.selected_event_id = 99
    app.nombre_entry.insert(0, "X")
    app.limpiar_campos_sin_resetear_id()
    assert app.selected_event_id == 99
    assert app.nombre_entry.get() == ""

# ------------------------ CASOS LÍMITE ------------------------
def test_nombre_un_caracter(app):
    app.nombre_entry.insert(0, "A")
    app.descripcion_entry.insert(0, "Desc")
    app.fecha_entry.insert(0, "01-01-2025")
    app.categoria_entry.insert(0, "Cat")
    app.precio_entry.insert(0, "10")
    app.cupos_entry.insert(0, "1")
    app.guardar_evento()
    app.event_manager.crear_evento.assert_called()

def test_descripcion_larga(app):
    app.nombre_entry.insert(0, "Evento")
    app.descripcion_entry.insert(0, "D"*1000)
    app.fecha_entry.insert(0, "01-01-2025")
    app.categoria_entry.insert(0, "Cat")
    app.precio_entry.insert(0, "100")
    app.cupos_entry.insert(0, "10")
    app.guardar_evento()
    app.event_manager.crear_evento.assert_called()

def test_precio_grande(app):
    app.nombre_entry.insert(0, "Evento")
    app.descripcion_entry.insert(0, "Desc")
    app.fecha_entry.insert(0, "01-01-2025")
    app.categoria_entry.insert(0, "Cat")
    app.precio_entry.insert(0, "1000000000")
    app.cupos_entry.insert(0, "10")
    app.guardar_evento()
    app.event_manager.crear_evento.assert_called()

def test_cupos_grande(app):
    app.nombre_entry.insert(0, "Evento")
    app.descripcion_entry.insert(0, "Desc")
    app.fecha_entry.insert(0, "01-01-2025")
    app.categoria_entry.insert(0, "Cat")
    app.precio_entry.insert(0, "1000")
    app.cupos_entry.insert(0, "100000")
    app.guardar_evento()
    app.event_manager.crear_evento.assert_called()