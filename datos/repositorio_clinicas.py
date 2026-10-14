"""Repositorio en memoria de las clínicas registradas."""
from reglas import validaciones as val
from reglas.clinica import Clinica
from reglas.excepciones import RegistroDuplicadoError, RegistroNoEncontradoError


class RepositorioClinicas:
    def __init__(self):
        self._clinicas = {}

    def registrar(self, clinica: Clinica) -> None:
        if clinica.nit in self._clinicas:
            raise RegistroDuplicadoError(f"Ya existe una clínica registrada con el NIT {clinica.nit}.")
        self._clinicas[clinica.nit] = clinica

    def buscar(self, nit: str) -> Clinica:
        nit = val.texto_obligatorio(nit, "NIT de la clínica")
        clinica = self._clinicas.get(nit)
        if clinica is None:
            raise RegistroNoEncontradoError(f"No existe una clínica con el NIT {nit}.")
        return clinica

    def existe(self, nit: str) -> bool:
        return val.texto_obligatorio(nit, "NIT de la clínica") in self._clinicas

    def vaciar(self) -> None:
        self._clinicas.clear()
