# Gestion de entradas para Micro-Eventos 

## Equipo 
- Daniel Zeballos 
- Carlos Arévalo 

---

## Decripción del proyecto 
Esta es una aplicación desarrollada en **Python** para una productora de eventos local. La herramienta está diseñada para gestionar micro-eventos, permitiendo un control completo sobre el ciclo de vida de cada evento, desde su creación hasta la gestión de entradas.

El sistema incluye funcionalidades de:
- CRUD de eventos (Crear, Leer, Actualizar, Eliminar)
- Distintos tipos de filtrado de eventos
- Módulo de autenticación básica
- Validación de datos y manejo de errores
- Reportes de eventos para seguimiento ágil

El proyecto fue desarrollado en el marco del curso **Pruebas de Software**, con enfoque en:
- Validación y Verificación del software
- Flujo de trabajo colaborativo con **Git**
- Buenas prácticas de programación

---

## Tabla de Contenidos
1. [Instalación](#instalación)  
2. [Estructura del Proyecto](#estructura-del-proyecto)  
3. [Dependencias](#dependencias)  
4. [Uso](#uso)  
5. [Testing](#testing)   
6. [Monitoreo y Reporte de Errores](#monitoreo-y-reporte-de-errores)
7. [Contribución](#contribución)
8. [Licencia](#licencia)

---

## Instalación 
1.  Asegúrate de tener instalado **Python 3.12+**:
    ```bash
    python --version
    ```
2.  Clona el repositorio:
    ```bash
    git clone <URL_DEL_REPOSITORIO>
    cd gestion-eventos-app
    ```
3.  Instala las dependencias necesarias para testing:
    ```bash
    pip install pytest
    ```

---


## Estructura del Proyecto


gestion-eventos-app/

├─ main.py                  
├─ LICENSE         
├─ README.md     
├─ data/                
│   ├─ eventos.db           
│   └─ usuarios.db


├─ database/             
│   ├─ EventManager.py      
│   └─ UserManager.py



├─ Interface/                
│   ├─ EventApp.py   
│   └─ LoginApp.py


├─ Test/                     
    ├─ test_event.py   
    └─ test_login.py     

---

## Dependencias

Algunas de las dependencias externas utilizadas en el proyecto son las siguientes: 
* **sentry_sdk**: Para monitoreo y captura de errores
* **pytest**: Framework de testing.

    Comando para instalar pytest:
    ```bash
    pip install pytest
    ```

    Comando para instalar sentry_sdk:
    ```bash
    pip install sentry_sdk
    ```

---

## Uso
Para utilizar el progama, asegurate estar en la carpeta principal del proyecto. Luego abre el terminal y ejecuta el siguiente comando:
```bash
    Python main.py
```
La interfaz gráfica permitirá:

* Crear nuevos eventos.
* Actualizar información de eventos existentes.
* Eliminar eventos.
* Gestionar cupos y entradas.
* Buscar eventos por nombre, fecha, categoría o precio.

---

## Testing 

Se incluye un conjunto de pruebas automatizadas usando `pytest`, para verificar la correcta funcionalidad del sistema.

Ejecutar todos los tests:

```bash
python -m pytest Test/test_event.py
python -m pytest Test/test_login.py
```
Se verifican 29 casos de prueba para EventApp y 26 casos de prueba para LoginApp

---

## Monitoreo y Reporte de Errores

Este proyecto utiliza [Sentry](https://sentry.io) para el monitoreo de errores en tiempo real. Gracias a Sentry, podemos detectar y resolver problemas antes de que afecten a los usuarios.

### Estado del proyecto
- **Errores nuevos en los últimos 14 días:** 41
- **Releases recientes:** 5 versiones desplegadas
- **Sesiones libres de errores:** Activado
- **Usuarios libres de errores:** Activado


Puedes ver el panel completo en [Sentry Insights del proyecto](https://usm-iv.sentry.io/insights/projects/python/?issuesType=new&project=4509992387280906)


---

## Contribución

Para contribuir al proyecto haz un fork del repositorio, crea una rama con los cambios que propones, confirma los cambios hechos con sus respectivos commits y envía un Pull Request con una descripción clara de tu aporte.

--- 

## Licencia

Este proyecto está bajo la licencia MIT. Puedes usarlo, modificarlo y distribuirlo libremente, siempre que se mantenga el aviso de copyright y la licencia.
