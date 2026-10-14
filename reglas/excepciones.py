"""Excepciones personalizadas de la capa de reglas."""


class ReglaNegocioError(Exception):
    """Error base: una regla de negocio o una validación de datos no se cumple."""


class DatoInvalidoError(ReglaNegocioError):
    """Un dato obligatorio falta o tiene un formato o valor no válido."""


class RegistroDuplicadoError(ReglaNegocioError):
    """Ya existe un registro con el mismo identificador (NIT, cédula o código)."""


class RegistroNoEncontradoError(ReglaNegocioError):
    """No existe el registro buscado."""


class EstadoInvalidoError(ReglaNegocioError):
    """La cita no está en el estado que exige la operación."""


class ConflictoHorarioError(ReglaNegocioError):
    """El veterinario o la mascota ya tienen una cita en esa fecha y hora."""


class CancelacionExtemporaneaError(ReglaNegocioError):
    """La cancelación no se hace antes de la fecha de la cita."""
