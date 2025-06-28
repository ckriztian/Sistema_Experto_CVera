## Instrucciones para Ejecutar la API del Sistema Experto Químico

Este repositorio contiene la API backend del Sistema Experto para identificación y descarte seguro de compuestos químicos en laboratorios.

### Requisitos

- **Python 3.8+**
- **pip** (gestor de paquetes de Python)
- Se recomienda entorno virtual (`venv`)

### Instalación de dependencias

Desde la terminal, navega a la carpeta del proyecto y ejecuta:

```bash
pip install fastapi uvicorn
```

Si usas entorno virtual, primero actívalo:

```bash
python -m venv venv
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate
```

### Archivos principales

- **app.py** – Archivo principal con la API FastAPI.
- **compuestos.json** (o `compuestos_descartes.json`) – Base de conocimiento de compuestos.
- **index.html** – Interfaz web (opcional).
- **style.css** – Hoja de estilos (opcional).

### Ejecución de la API

1. **Asegúrate de estar en el directorio correcto y tener las dependencias instaladas.**
2. Ejecuta el siguiente comando en la terminal:

```bash
uvicorn app:app --reload
```

Esto iniciará el servidor en modo desarrollo.

### Acceso a la API

- **Documentación interactiva (Swagger UI):**
  - [http://localhost:8000/docs](http://localhost:8000/docs)
- **Consultar una pregunta de decisión:**
  - `GET http://localhost:8000/pregunta`
- **Enviar una respuesta (sí/no):**
  - `POST http://localhost:8000/respuesta?prop=PROP&respuesta=true|false`
- **Reiniciar consulta:**
  - `GET http://localhost:8000/reiniciar`
- **Listar todos los compuestos:**
  - `GET http://localhost:8000/compuestos`
- **Ver historial de la consulta:**
  - `GET http://localhost:8000/historial`

### Uso con la interfaz web

1. Abre `index.html` en tu navegador preferido.
2. Asegúrate de que la API esté corriendo en `localhost:8000`.
3. Responde las preguntas y consulta el resultado.

### Notas

- Si cambias la base de conocimiento (`compuestos.json`), reinicia el servidor para recargar datos.
- Puedes modificar `style.css` o las imágenes para personalizar la interfaz.

### Soporte

Para dudas o sugerencias, contacta a Cristian Vera.

---

*Desarrollado para la Tecnicatura en Ciencia de Datos e IA – Politécnico Malvinas Argentinas, 2024.*