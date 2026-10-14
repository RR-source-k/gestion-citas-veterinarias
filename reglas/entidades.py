"""Entidades de la capa de reglas (atributos privados con acceso mediante @property)."""
from datetime import date

from reglas import validaciones as val
from reglas.estado_cita import EstadoCita
from reglas.excepciones import RegistroDuplicadoError, RegistroNoEncontradoError


class Servicio:
    def __init__(self, codigo: str, nombre: str, tarifa: float):
        self._codigo = val.texto_obligatorio(codigo, "código del servicio")
        self._nombre = val.texto_obligatorio(nombre, "nombre del servicio")
        self._tarifa = val.numero_positivo(tarifa, "tarifa")

    @property
    def codigo(self): return self._codigo
    @property
    def nombre(self): return self._nombre
    @property
    def tarifa(self): return self._tarifa


class Veterinario:
    def __init__(self, cedula: str, nombre: str, tarjeta_profesional: str):
        self._cedula = val.solo_digitos(cedula, "cédula del veterinario")
        self._nombre = val.texto_obligatorio(nombre, "nombre del veterinario")
        self._tarjeta_profesional = val.texto_obligatorio(tarjeta_profesional, "tarjeta profesional")

    @property
    def cedula(self): return self._cedula
    @property
    def nombre(self): return self._nombre
    @property
    def tarjeta_profesional(self): return self._tarjeta_profesional


class Mascota:
    def __init__(self, nombre: str, especie: str, raza: str, anio_nacimiento: int, peso: float):
        self._nombre = val.texto_obligatorio(nombre, "nombre de la mascota")
        self._especie = val.texto_obligatorio(especie, "especie")
        self._raza = val.texto_obligatorio(raza, "raza")
        self._anio_nacimiento = val.entero_en_rango(anio_nacimiento, "año de nacimiento", 1990, date.today().year)
        self._peso = val.numero_positivo(peso, "peso")

    @property
    def nombre(self): return self._nombre
    @property
    def especie(self): return self._especie
    @property
    def raza(self): return self._raza
    @property
    def anio_nacimiento(self): return self._anio_nacimiento
    @property
    def peso(self): return self._peso


class Propietario:
    def __init__(self, cedula: str, nombre: str, telefono: str, municipio: str):
        self._cedula = val.solo_digitos(cedula, "cédula del propietario")
        self._nombre = val.texto_obligatorio(nombre, "nombre del propietario")
        self._telefono = val.solo_digitos(telefono, "teléfono", 7, 10)
        self._municipio = val.texto_obligatorio(municipio, "municipio del propietario")
        self._mascotas = []

    @property
    def cedula(self): return self._cedula
    @property
    def nombre(self): return self._nombre
    @property
    def telefono(self): return self._telefono
    @property
    def municipio(self): return self._municipio
    @property
    def mascotas(self): return list(self._mascotas)

    def agregar_mascota(self, mascota: Mascota) -> None:
        if any(m.nombre.casefold() == mascota.nombre.casefold() for m in self._mascotas):
            raise RegistroDuplicadoError(
                f"El propietario {self._nombre} ya tiene una mascota llamada '{mascota.nombre}'.")
        self._mascotas.append(mascota)

    def buscar_mascota(self, nombre: str) -> Mascota:
        nombre = val.texto_obligatorio(nombre, "nombre de la mascota")
        for mascota in self._mascotas:
            if mascota.nombre.casefold() == nombre.casefold():
                return mascota
        raise RegistroNoEncontradoError(
            f"El propietario {self._nombre} no tiene registrada una mascota llamada '{nombre}'.")


class Factura:
    def __init__(self, codigo: str, fecha: str, propietario: Propietario, mascota: Mascota, servicios: list):
        self._codigo = val.texto_obligatorio(codigo, "código de la factura")
        self._fecha = fecha
        self._propietario = propietario
        self._mascota = mascota
        self._servicios = list(servicios)
        self._valor_total = self.calcular_total()

    @property
    def codigo(self): return self._codigo
    @property
    def fecha(self): return self._fecha
    @property
    def propietario(self): return self._propietario
    @property
    def mascota(self): return self._mascota
    @property
    def servicios(self): return list(self._servicios)
    @property
    def valor_total(self): return self._valor_total

    def calcular_total(self) -> float:
        return sum(s.tarifa for s in self._servicios)


class Cita:
    def __init__(self, codigo: str, propietario: Propietario, mascota: Mascota, fecha: str, hora: str,
                 veterinario: Veterinario, servicio_inicial: Servicio):
        self._codigo = val.texto_obligatorio(codigo, "código de la cita")
        self._propietario = propietario
        self._mascota = mascota
        self._fecha = val.formatear_fecha(val.parsear_fecha(fecha))
        self._hora = val.formatear_hora(val.parsear_hora(hora))
        self._veterinario = veterinario
        self._servicios = [servicio_inicial]
        self._estado = EstadoCita.PROGRAMADA
        self._factura = None

    @property
    def codigo(self): return self._codigo
    @property
    def propietario(self): return self._propietario
    @property
    def mascota(self): return self._mascota
    @property
    def fecha(self): return self._fecha
    @property
    def hora(self): return self._hora
    @property
    def veterinario(self): return self._veterinario
    @property
    def servicios(self): return list(self._servicios)

    @property
    def estado(self): return self._estado
    @estado.setter
    def estado(self, nuevo_estado): self._estado = nuevo_estado

    @property
    def factura(self): return self._factura
    @factura.setter
    def factura(self, nueva_factura): self._factura = nueva_factura

    def agregar_servicio(self, servicio: Servicio) -> None:
        self._servicios.append(servicio)
