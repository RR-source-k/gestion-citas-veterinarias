"""Funciones de validación de datos usadas por la capa de reglas."""
import math
import re
from datetime import date, datetime, time

from reglas.excepciones import DatoInvalidoError

FORMATO_FECHA = "%d/%m/%Y"
FORMATO_HORA = "%H:%M"


def texto_obligatorio(valor, campo: str) -> str:
    texto = "" if valor is None else str(valor).strip()
    if not texto:
        raise DatoInvalidoError(f"El campo '{campo}' es obligatorio.")
    return texto


def solo_digitos(valor, campo: str, minimo: int = 5, maximo: int = 15) -> str:
    texto = texto_obligatorio(valor, campo)
    if not re.fullmatch(r"[0-9]+", texto) or not minimo <= len(texto) <= maximo:
        if minimo == maximo:
            requisito = f"exactamente {minimo} dígitos"
        else:
            requisito = f"entre {minimo} y {maximo} dígitos"
        raise DatoInvalidoError(f"El campo '{campo}' debe contener solo números ({requisito}).")
    return texto


def nit_valido(valor) -> str:
    texto = texto_obligatorio(valor, "NIT")
    if not re.fullmatch(r"[0-9]{6,12}-[0-9]", texto):
        raise DatoInvalidoError("El NIT debe tener el formato 901456789-1.")
    return texto


def numero_positivo(valor, campo: str) -> float:
    try:
        numero = float(valor)
    except (TypeError, ValueError):
        raise DatoInvalidoError(f"El campo '{campo}' debe ser un número.") from None
    if not math.isfinite(numero) or numero <= 0:
        raise DatoInvalidoError(f"El campo '{campo}' debe ser un número mayor que cero.")
    return numero


def entero_en_rango(valor, campo: str, minimo: int, maximo: int) -> int:
    try:
        numero = float(valor)
    except (TypeError, ValueError):
        raise DatoInvalidoError(f"El campo '{campo}' debe ser un número entero.") from None
    if not math.isfinite(numero) or not numero.is_integer():
        raise DatoInvalidoError(f"El campo '{campo}' debe ser un número entero.")
    numero = int(numero)
    if not minimo <= numero <= maximo:
        raise DatoInvalidoError(f"El campo '{campo}' debe estar entre {minimo} y {maximo}.")
    return numero


def parsear_fecha(valor, campo: str = "fecha") -> date:
    texto = texto_obligatorio(valor, campo)
    try:
        return datetime.strptime(texto, FORMATO_FECHA).date()
    except ValueError:
        raise DatoInvalidoError(f"La {campo} '{texto}' no es válida; use el formato DD/MM/AAAA.") from None


def parsear_hora(valor, campo: str = "hora") -> time:
    texto = texto_obligatorio(valor, campo)
    try:
        return datetime.strptime(texto, FORMATO_HORA).time()
    except ValueError:
        raise DatoInvalidoError(f"La {campo} '{texto}' no es válida; use el formato HH:MM (24 horas).") from None


def formatear_fecha(fecha: date) -> str:
    return fecha.strftime(FORMATO_FECHA)


def formatear_hora(hora: time) -> str:
    return hora.strftime(FORMATO_HORA)
