import pytz
import datetime


class Funcion():
    def __init__(self, id, pelicula, sala, hora):
        self.id = id
        self.pelicula = pelicula
        self.sala = sala
        self.hora = hora
        self.asientos = self.vacio()

    def disponible(self):
        if self.llena():
            return "Llena"
        else:
            timezone = pytz.timezone('America/Guatemala')
            fecha_completa = datetime.datetime.now(tz=timezone)
            hora = fecha_completa.strftime("%H")
            minutos = fecha_completa.strftime("%M")
            hora_actual = int(hora)
            min_actual = int(minutos)
            tiempo_funcion = self.hora.split(":")
            hora_funcion = int(tiempo_funcion[0])
            min_funcion = int(tiempo_funcion[1])
            if hora_actual > hora_funcion:
                return "No Disponible"
            elif hora_actual == hora_funcion:
                if min_actual > min_funcion:
                    return "No Disponible"
                else:
                    return "Disponible"
            else:
                return "Disponible"

    def vacio(self):
        sala = []
        for i in range(9):
            sala.append({"identificador": i+1, "disponible": True})
        return sala

    def apartar(self, identificador):
        i = identificador - 1
        self.asientos[i]["disponible"] = False

    def llena(self):
        for asiento in self.asientos:
            if asiento["disponible"]:
                return False
        return True
