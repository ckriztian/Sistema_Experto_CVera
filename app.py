from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

# Permitir conexión desde cualquier origen (útil para pruebas locales)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Carga de la base de conocimiento
with open("compuestos.json", encoding="utf-8") as f:
    data = json.load(f)
    base = data["entries"]

# Historial de consultas (global, 1 usuario a la vez)
historial = []

# Extrae todas las props posibles para hacer preguntas
def get_all_props():
    props = set()
    for c in base:
        props.update(c["props"])
    return sorted(list(props))

# Lógica principal de preguntas y filtrado
class Consulta:
    def __init__(self):
        self.respuestas_si = []
        self.respuestas_no = []
        self.restantes = base.copy()
        self.props = get_all_props()
        self.preguntas_ya = []

    def siguiente_pregunta(self):
        for p in self.props:
            if p not in self.preguntas_ya:
                return p
        return None

    def responder(self, prop, respuesta):
        self.preguntas_ya.append(prop)
        historial.append({"pregunta": prop, "respuesta": respuesta})
        if respuesta:
            self.respuestas_si.append(prop)
            self.restantes = [c for c in self.restantes if prop in c["props"]]
        else:
            self.respuestas_no.append(prop)
            self.restantes = [c for c in self.restantes if prop not in c["props"]]

    def resultado(self):
        if len(self.restantes) == 1:
            return self.restantes[0]
        elif len(self.restantes) == 0:
            return None
        else:
            return None

# Guardar consulta activa en memoria (para demo simple, 1 usuario a la vez)
consulta = Consulta()

@app.get("/pregunta")
def get_pregunta():
    res = consulta.resultado()
    if res:
        return {
            "name": res["name"],
            "description": res["description"],
            "props": res["props"]
        }
    prop = consulta.siguiente_pregunta()
    if prop:
        return {"pregunta": prop}
    return {"mensaje": "No se pudo identificar el compuesto. Intenta reiniciar."}

@app.post("/respuesta")
def post_respuesta(prop: str, respuesta: bool):
    consulta.responder(prop, respuesta)
    return get_pregunta()

@app.get("/reiniciar")
def reiniciar():
    global consulta, historial
    consulta = Consulta()
    historial = []
    return {"mensaje": "Consulta reiniciada"}

@app.get("/compuestos")
def get_compuestos():
    """
    Devuelve toda la base de conocimiento de compuestos químicos y sus propiedades.
    """
    return base

@app.get("/historial")
def get_historial():
    """
    Devuelve el historial de preguntas y respuestas de la consulta actual.
    """
    return historial

