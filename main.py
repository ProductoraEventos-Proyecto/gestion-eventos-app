import tkinter as tk
from Interface.EventApp import EventApp
from Interface.LoginApp import LoginApp

def iniciar_app_eventos(login_root, username):
    login_root.destroy()
    
    root_eventos = tk.Tk()
    app = EventApp(root_eventos, username)
    root_eventos.mainloop()

if __name__ == '__main__':
    root_login = tk.Tk()
    login_app = LoginApp(root_login, lambda username: iniciar_app_eventos(root_login, username))
    root_login.mainloop()