"""Clase Clinica: concentra las reglas de negocio de la gestión de citas."""
from reglas import validaciones as val
from reglas.entidades import Cita, Factura, Mascota, Propietario, Servicio, Veterinario
from reglas.estado_cita import EstadoCita
from reglas.excepciones import (
    CancelacionExtemporaneaError,
    ConflictoHorarioError,
    EstadoInvalidoError,
    RegistroDuplicadoError,
    RegistroNoEncontradoError,
)


class Clinica:
    def __init__(self, nit: str, nombre: str, municipio: str, codigo_dane: str, departamento: str,
                 direccion: str, barrio: str):
        self._nit = val.nit_valido(nit)
        self._nombre = val.texto_obligatorio(nombre, "nombre de la clínica")
        self._municipio = val.texto_obligatorio(municipio, "municipio")
        self._codigo_dane = val.solo_digitos(codigo_dane, "código DANE", 5, 5)
        self._departamento = val.texto_obligatorio(departamento, "departamento")
        self._direccion = val.texto_obligatorio(direccion, "dirección")
        self._barrio = val.texto_obligatorio(barrio, "barrio")
        self._veterinarios = []
        self._servicios = []
        self._propietarios = []
        self._citas = []
        self._facturas = []

    @property
    def nit(self): return self._nit
    @property
    def nombre(self): return self._nombre
    @property
    def municipio(self): return self._municipio
    @property
    def codigo_dane(self): return self._codigo_dane
    @property
    def departamento(self): return self._departamento
    @property
    def direccion(self): return self._direccion
    @property
    def barrio(self): return self._barrio
    @property
    def veterinarios(self): return list(self._veterinarios)
    @property
    def servicios(self): return list(self._servicios)
    @property
    def propietarios(self): return list(self._propietarios)
    @property
    def citas(self): return list(self._citas)
    @property
    def facturas(self): return list(self._facturas)

    # ------------------------------------------------------------------ registros
    def registrar_veterinario(self, cedula: str, nombre: str, tarjeta_profesional: str) -> Veterinario:
        veterinario = Veterinario(cedula, nombre, tarjeta_profesional)
        if any(v.cedula == veterinario.cedula for v in self._veterinarios):
            raise RegistroDuplicadoError(
                f"Ya existe un veterinario con cédula {veterinario.cedula} en esta clínica.")
        self._veterinarios.append(veterinario)
        return veterinario

    def registrar_servicio(self, codigo: str, nombre: str, tarifa: float) -> Servicio:
        servicio = Servicio(codigo, nombre, tarifa)
        if any(s.codigo == servicio.codigo for s in self._servicios):
            raise RegistroDuplicadoError(
                f"Ya existe un servicio con el código {servicio.codigo} en esta clínica.")
        self._servicios.append(servicio)
        return servicio

    def registrar_propietario(self, cedula: str, nombre: str, telefono: str, municipio: str) -> Propietario:
        propietario = Propietario(cedula, nombre, telefono, municipio)
        if any(p.cedula == propietario.cedula for p in self._propietarios):
            raise RegistroDuplicadoError(
                f"Ya existe un propietario con la cédula {propietario.cedula} en esta clínica.")
        self._propietarios.append(propietario)
        return propietario

    def registrar_mascota(self, cedula_propietario: str, nombre: str, especie: str, raza: str,
                          anio_nacimiento: int, peso: float) -> Mascota:
        propietario = self.buscar_propietario(cedula_propietario)
        mascota = Mascota(nombre, especie, raza, anio_nacimiento, peso)
        propietario.agregar_mascota(mascota)
        return mascota

    # ------------------------------------------------------------------ búsquedas
    def buscar_veterinario(self, cedula: str) -> Veterinario:
        cedula = val.texto_obligatorio(cedula, "cédula del veterinario")
        for veterinario in self._veterinarios:
            if veterinario.cedula == cedula:
                return veterinario
        raise RegistroNoEncontradoError(f"No existe un veterinario con cédula {cedula} en esta clínica.")

    def buscar_servicio(self, codigo: str) -> Servicio:
        codigo = val.texto_obligatorio(codigo, "código del servicio")
        for servicio in self._servicios:
            if servicio.codigo == codigo:
                return servicio
        raise RegistroNoEncontradoError(f"No existe un servicio con el código {codigo} en esta clínica.")

    def buscar_propietario(self, cedula: str) -> Propietario:
        cedula = val.texto_obligatorio(cedula, "cédula del propietario")
        for propietario in self._propietarios:
            if propietario.cedula == cedula:
                return propietario
        raise RegistroNoEncontradoError(f"No existe un propietario con la cédula {cedula} en esta clínica.")

    def buscar_cita(self, codigo: str) -> Cita:
        codigo = val.texto_obligatorio(codigo, "código de la cita")
        for cita in self._citas:
            if cita.codigo == codigo:
                return cita
        raise RegistroNoEncontradoError(f"No se encontró la cita {codigo}.")

    # ------------------------------------------------------------------ citas
    def programar_cita(self, codigo: str, cedula_propietario: str, nombre_mascota: str, fecha: str, hora: str,
                       cedula_veterinario: str, codigo_servicio: str) -> Cita:
        codigo = val.texto_obligatorio(codigo, "código de la cita")
        val.parsear_fecha(fecha)
        val.parsear_hora(hora)
        if any(c.codigo == codigo for c in self._citas):
            raise RegistroDuplicadoError(f"Ya existe una cita con el código {codigo} en esta clínica.")

        propietario = self.buscar_propietario(cedula_propietario)
        mascota = propietario.buscar_mascota(nombre_mascota)
        veterinario = self.buscar_veterinario(cedula_veterinario)
        servicio = self.buscar_servicio(codigo_servicio)

        cita = Cita(codigo, propietario, mascota, fecha, hora, veterinario, servicio)
        self._validar_disponibilidad(cita)
        self._citas.append(cita)
        return cita

    def _validar_disponibilidad(self, cita: Cita) -> None:
        """Ni el veterinario ni la mascota pueden tener otra cita (no cancelada) a la misma fecha y hora."""
        for otra in self._citas:
            if otra.estado == EstadoCita.CANCELADA or otra.fecha != cita.fecha or otra.hora != cita.hora:
                continue
            if otra.veterinario.cedula == cita.veterinario.cedula:
                raise ConflictoHorarioError(
                    f"El/la veterinario(a) {otra.veterinario.nombre} ya tiene la cita {otra.codigo} "
                    f"asignada el {cita.fecha} a las {cita.hora}.")
            if otra.mascota is cita.mascota:
                raise ConflictoHorarioError(
                    f"La mascota {cita.mascota.nombre} ya tiene la cita {otra.codigo} "
                    f"agendada el {cita.fecha} a las {cita.hora}.")

    def cancelar_cita(self, codigo: str, fecha_cancelacion: str) -> Cita:
        fecha_cancel = val.parsear_fecha(fecha_cancelacion, "fecha de cancelación")
        cita = self.buscar_cita(codigo)
        if cita.estado != EstadoCita.PROGRAMADA:
            raise EstadoInvalidoError(
                f"La cita {cita.codigo} ya fue {cita.estado.value.lower()} y no se puede cancelar.")
        if fecha_cancel >= val.parsear_fecha(cita.fecha):
            raise CancelacionExtemporaneaError(
                f"La cita {cita.codigo} es el {cita.fecha}: solo se puede cancelar antes de esa fecha "
                f"(fecha indicada: {val.formatear_fecha(fecha_cancel)}).")
        cita.estado = EstadoCita.CANCELADA
        return cita

    def atender_cita(self, codigo: str, codigo_factura: str, codigos_extra: list) -> Cita:
        cita = self.buscar_cita(codigo)
        if cita.estado != EstadoCita.PROGRAMADA:
            raise EstadoInvalidoError(
                f"No se puede atender la cita {cita.codigo} porque se encuentra en estado '{cita.estado}'.")
        codigo_factura = val.texto_obligatorio(codigo_factura, "código de la factura")
        if any(f.codigo == codigo_factura for f in self._facturas):
            raise RegistroDuplicadoError(f"Ya existe una factura con el código {codigo_factura} en esta clínica.")
        # Se validan todos los servicios adicionales antes de modificar la cita.
        servicios_extra = [self.buscar_servicio(c) for c in (codigos_extra or [])]

        for servicio in servicios_extra:
            cita.agregar_servicio(servicio)
        cita.estado = EstadoCita.ATENDIDA
        factura = Factura(codigo_factura, cita.fecha, cita.propietario, cita.mascota, cita.servicios)
        cita.factura = factura
        self._facturas.append(factura)
        return cita

    # ------------------------------------------------------------------ consultas
    def consultar_citas_por_fecha(self, fecha: str) -> list:
        fecha = val.formatear_fecha(val.parsear_fecha(fecha))
        return sorted((c for c in self._citas if c.fecha == fecha), key=lambda c: c.hora)

    def consultar_historial_mascota(self, nombre_mascota: str, cedula_propietario: str = None) -> list:
        nombre = val.texto_obligatorio(nombre_mascota, "nombre de la mascota")
        cedula = "" if cedula_propietario is None else str(cedula_propietario).strip()
        citas = [c for c in self._citas
                 if c.mascota.nombre.casefold() == nombre.casefold()
                 and (not cedula or c.propietario.cedula == cedula)]
        return sorted(citas, key=lambda c: (val.parsear_fecha(c.fecha), c.hora))
