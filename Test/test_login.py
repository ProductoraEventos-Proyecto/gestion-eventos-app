import pytest
from unittest.mock import MagicMock
from Interface.LoginApp import LoginApp
import tkinter as tk


@pytest.fixture
def app(monkeypatch):
    # Creamos un Tk real pero oculto
    root = tk.Tk()
    root.withdraw()  # evita que la ventana aparezca

    on_success_callback = MagicMock()
    test_app = LoginApp(root, on_success_callback)

    # Solo mockeamos lo que puede abrir ventanas o hacer side-effects
    test_app.user_manager = MagicMock()
    monkeypatch.setattr("tkinter.messagebox.showerror", MagicMock())
    monkeypatch.setattr("tkinter.messagebox.showinfo", MagicMock())

    yield test_app

    root.destroy()

def test_iniciar_sesion_exitoso(app):
    app.username_entry.insert(0, "test_user")
    app.password_entry.insert(0, "password123")
    app.user_manager.verificar_usuario.return_value = True
    app.iniciar_sesion()
    app.on_success_callback.assert_called_with("test_user")
    tk.messagebox.showerror.assert_not_called()

def test_iniciar_sesion_incorrecto(app):
    app.username_entry.insert(0, "test_user")
    app.password_entry.insert(0, "wrong_pass")
    app.user_manager.verificar_usuario.return_value = False
    app.iniciar_sesion()
    tk.messagebox.showerror.assert_called_with("Error", "Usuario o contraseña incorrectos.")

def test_iniciar_sesion_campos_vacios_username(app):
    app.username_entry.insert(0, "")
    app.password_entry.insert(0, "pass")
    app.iniciar_sesion()
    app.user_manager.verificar_usuario.assert_not_called()
    tk.messagebox.showerror.assert_called_with("Error", "Usuario y contraseña no pueden estar vacíos.")

def test_iniciar_sesion_campos_vacios_password(app):
    app.username_entry.insert(0, "user")
    app.password_entry.insert(0, "")
    app.iniciar_sesion()
    app.user_manager.verificar_usuario.assert_not_called()
    tk.messagebox.showerror.assert_called_with("Error", "Usuario y contraseña no pueden estar vacíos.")

def test_iniciar_sesion_campos_vacios_total(app):
    app.username_entry.insert(0, "")
    app.password_entry.insert(0, "")
    app.iniciar_sesion()
    app.user_manager.verificar_usuario.assert_not_called()
    tk.messagebox.showerror.assert_called_with("Error", "Usuario y contraseña no pueden estar vacíos.")

def test_iniciar_sesion_username_con_espacios(app):
    app.username_entry.insert(0, "  user123  ")
    app.password_entry.insert(0, "password")
    app.user_manager.verificar_usuario.return_value = True
    app.iniciar_sesion()
    app.user_manager.verificar_usuario.assert_called_with("user123", "password")

def test_iniciar_sesion_password_con_espacios(app):
    app.username_entry.insert(0, "user")
    app.password_entry.insert(0, " pass ")
    app.user_manager.verificar_usuario.return_value = False
    app.iniciar_sesion()
    tk.messagebox.showerror.assert_called()

def test_iniciar_sesion_sensible_a_mayusculas(app):
    app.username_entry.insert(0, "User")
    app.password_entry.insert(0, "pass")
    app.user_manager.verificar_usuario.return_value = False
    app.iniciar_sesion()
    tk.messagebox.showerror.assert_called()

def test_iniciar_sesion_username_unicode(app):
    app.username_entry.insert(0, "usuario_ñ")
    app.password_entry.insert(0, "clave")
    app.user_manager.verificar_usuario.return_value = True
    app.iniciar_sesion()
    app.user_manager.verificar_usuario.assert_called_with("usuario_ñ", "clave")

def test_iniciar_sesion_username_caracteres_especiales(app):
    app.username_entry.insert(0, "user!@#")
    app.password_entry.insert(0, "pass!@#")
    app.user_manager.verificar_usuario.return_value = True
    app.iniciar_sesion()
    app.user_manager.verificar_usuario.assert_called_with("user!@#", "pass!@#")

def test_iniciar_sesion_username_largo(app):
    username = "a" * 200
    app.username_entry.insert(0, username)
    app.password_entry.insert(0, "password")
    app.user_manager.verificar_usuario.return_value = True
    app.iniciar_sesion()
    app.user_manager.verificar_usuario.assert_called_with(username, "password")

def test_iniciar_sesion_password_largo(app):
    password = "p" * 200
    app.username_entry.insert(0, "user")
    app.password_entry.insert(0, password)
    app.user_manager.verificar_usuario.return_value = True
    app.iniciar_sesion()
    app.user_manager.verificar_usuario.assert_called_with("user", password)

def test_crear_cuenta_exitoso(app):
    app.username_entry.insert(0, "new_user")
    app.password_entry.insert(0, "new_pass")
    app.user_manager.crear_usuario.return_value = True
    app.crear_cuenta()
    app.confirmar_creacion_cuenta()
    tk.messagebox.showinfo.assert_called()

def test_crear_cuenta_existente(app):
    app.username_entry.insert(0, "existente")
    app.password_entry.insert(0, "pass")
    app.user_manager.crear_usuario.return_value = False
    app.crear_cuenta()
    app.confirmar_creacion_cuenta()
    tk.messagebox.showerror.assert_called_with("Error", "El usuario ya existe. Por favor, elige otro.")

def test_crear_cuenta_campos_vacios(app):
    app.username_entry.insert(0, "")
    app.password_entry.insert(0, "")
    app.crear_cuenta()
    app.confirmar_creacion_cuenta()
    tk.messagebox.showerror.assert_called_with("Error", "Usuario y contraseña no pueden estar vacíos.")

def test_crear_cuenta_username_con_espacios(app):
    app.username_entry.insert(0, "  user  ")
    app.password_entry.insert(0, "pass")
    app.user_manager.crear_usuario.return_value = True
    app.crear_cuenta()
    app.confirmar_creacion_cuenta()
    app.user_manager.crear_usuario.assert_called_with("user", "pass")

def test_crear_cuenta_password_con_espacios(app):
    app.username_entry.insert(0, "user")
    app.password_entry.insert(0, " pass ")
    app.user_manager.crear_usuario.return_value = True
    app.crear_cuenta()
    app.confirmar_creacion_cuenta()
    app.user_manager.crear_usuario.assert_called_with("user", " pass ")

def test_crear_cuenta_username_unicode(app):
    app.username_entry.insert(0, "软件测试")
    app.password_entry.insert(0, "clave")
    app.user_manager.crear_usuario.return_value = True
    app.crear_cuenta()
    app.confirmar_creacion_cuenta()
    app.user_manager.crear_usuario.assert_called_with("软件测试", "clave")

def test_crear_cuenta_username_largo(app):
    username = "a" * 300
    app.username_entry.insert(0, username)
    app.password_entry.insert(0, "pass")
    app.user_manager.crear_usuario.return_value = True
    app.crear_cuenta()
    app.confirmar_creacion_cuenta()
    app.user_manager.crear_usuario.assert_called_with(username, "pass")

def test_crear_cuenta_password_largo(app):
    password = "p" * 300
    app.username_entry.insert(0, "user")
    app.password_entry.insert(0, password)
    app.user_manager.crear_usuario.return_value = True
    app.crear_cuenta()
    app.confirmar_creacion_cuenta()
    app.user_manager.crear_usuario.assert_called_with("user", password)

def test_crear_cuenta_username_igual_a_password(app):
    app.username_entry.insert(0, "same")
    app.password_entry.insert(0, "same")
    app.user_manager.crear_usuario.return_value = True
    app.crear_cuenta()
    app.confirmar_creacion_cuenta()
    app.user_manager.crear_usuario.assert_called_with("same", "same")

def test_volver_a_login_restaura_estado(app):
    app.crear_cuenta()
    app.volver_a_login()
    assert app.mode == "login"
    assert app.subtitle_label.cget("text") == "Inicia sesión o crea tu cuenta"

def test_crear_cuenta_cambia_estado(app):
    app.crear_cuenta()
    assert app.mode == "register"
    assert app.subtitle_label.cget("text") == "Creando nueva cuenta"

def test_volver_a_login_limpia_campos(app):
    app.username_entry.insert(0, "user")
    app.password_entry.insert(0, "pass")
    app.crear_cuenta()
    app.volver_a_login()
    assert app.username_entry.get() == ""
    assert app.password_entry.get() == ""

def test_crear_cuenta_oculta_boton_login(app):
    app.crear_cuenta()
    assert app.login_button.winfo_manager() == ""

def test_crear_cuenta_muestra_boton_volver(app):
    app.crear_cuenta()
    assert app.volver_button.winfo_manager() != ""
