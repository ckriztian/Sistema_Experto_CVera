from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json

from engine import Consulta

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

with open("compuestos.json", encoding="utf-8") as f:
    data = json.load(f)
    base = data["entries"]

# Historial global (puedes mejorarlo en el futuro por usuario)
historial = []

# Instancia del motor de inferencia
consulta = Consulta(base)

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
    # Guardar en historial
    historial.append({"pregunta": prop, "respuesta": respuesta})
    return get_pregunta()

@app.get("/reiniciar")
def reiniciar():
    global consulta, historial
    consulta = Consulta(base)
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

# CRUD de compuestos (pueden seguir igual)
from pydantic import BaseModel

class NuevoCompuesto(BaseModel):
    name: str
    description: str
    props: list[str]

@app.post("/agregar_compuesto")
def agregar_compuesto(compuesto: NuevoCompuesto):
    with open("compuestos.json", encoding="utf-8") as f:
        data = json.load(f)
    data["entries"].append(compuesto.dict())
    with open("compuestos.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return {"mensaje": "Compuesto agregado exitosamente"}

@app.delete("/eliminar_compuesto")
def eliminar_compuesto(nombre: str):
    with open("compuestos.json", encoding="utf-8") as f:
        data = json.load(f)

    originales = data["entries"]
    nuevos = [c for c in originales if c["name"].lower() != nombre.lower()]

    if len(nuevos) == len(originales):
        raise HTTPException(status_code=404, detail="Compuesto no encontrado")

    data["entries"] = nuevos
    with open("compuestos.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    return {"mensaje": f"Compuesto '{nombre}' eliminado exitosamente"}

@app.put("/modificar_compuesto")
def modificar_compuesto(compuesto: NuevoCompuesto):
    with open("compuestos.json", encoding="utf-8") as f:
        data = json.load(f)

    for i, c in enumerate(data["entries"]):
        if c["name"].lower() == compuesto.name.lower():
            data["entries"][i] = compuesto.dict()
            with open("compuestos.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return {"mensaje": f"Compuesto '{compuesto.name}' modificado"}

    raise HTTPException(status_code=404, detail="Compuesto no encontrado")
