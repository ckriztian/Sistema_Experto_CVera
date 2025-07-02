import json

def get_all_props(base):
    props = set()
    for c in base:
        props.update(c["props"])
    return sorted(list(props))

def mejor_pregunta(props_disponibles, compuestos_restantes, preguntas_ya):
        # Elige la pregunta que más balancea el "sí" y "no" (split más parejo)
        mejor = None
        mejor_diferencia = None
        for prop in props_disponibles:
            if prop in preguntas_ya or prop in ["Es sólido", "Es gas", "Es líquido"]:
                continue
            si = [c for c in compuestos_restantes if prop in c["props"]]
            no = [c for c in compuestos_restantes if prop not in c["props"]]
            diferencia = abs(len(si) - len(no))
            # Queremos la menor diferencia, es decir, la pregunta más informativa
            if mejor is None or diferencia < mejor_diferencia:
                mejor = prop
                mejor_diferencia = diferencia
        return mejor

class Consulta:
    def __init__(self, base):
        self.base = base.copy()
        self.respuestas_si = []
        self.respuestas_no = []
        self.restantes = self.base.copy()
        self.props = get_all_props(self.base)
        self.preguntas_ya = []
        self.fase_estado = True  # Etapa de filtrado por estado físico
    
    def siguiente_pregunta(self):
        # Primero, filtrado por estado físico
        if self.fase_estado:
            if "Es sólido" not in self.preguntas_ya:
                return "Es sólido"
            elif "Es gas" not in self.preguntas_ya:
                return "Es gas"
            else:
                self.filtrar_estado("Es líquido")
                self.fase_estado = False
        # Luego, elegí la pregunta óptima
        prop = mejor_pregunta(self.props, self.restantes, self.preguntas_ya)
        return prop


    def filtrar_estado(self, estado):
        self.restantes = [c for c in self.restantes if estado in c["props"]]
        self.preguntas_ya.append(estado)
        self.respuestas_si.append(estado)

    def responder(self, prop, respuesta):
        self.preguntas_ya.append(prop)
        if respuesta:
            self.respuestas_si.append(prop)
            self.restantes = [c for c in self.restantes if prop in c["props"]]
            if self.fase_estado and prop in ["Es sólido", "Es gas"]:
                self.fase_estado = False
        else:
            self.respuestas_no.append(prop)
            self.restantes = [c for c in self.restantes if prop not in c["props"]]
            if self.fase_estado and prop == "Es gas" and "Es sólido" in self.preguntas_ya:
                self.filtrar_estado("Es líquido")
                self.fase_estado = False

    def resultado(self):
        if len(self.restantes) == 1:
            return self.restantes[0]
        elif len(self.restantes) == 0:
            return None
        else:
            return None

    
