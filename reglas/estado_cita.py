"""Estados posibles de una cita."""
from enum import Enum


class EstadoCita(Enum):
    PROGRAMADA = "Programada"
    CANCELADA = "Cancelada"
    ATENDIDA = "Atendida"

    def __str__(self) -> str:
        return self.value
