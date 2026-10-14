"""Capa de presentación: controlador que recibe los datos de la interfaz y devuelve mensajes."""
from datos.datos_ejemplo import DatosEjemplo, NIT_HUELLITAS, NIT_PATITAS
from datos.repositorio_clinicas import RepositorioClinicas
from reglas.clinica import Clinica
from reglas.excepciones import ReglaNegocioError


def _moneda(valor: float) -> str:
    return "$ " + f"{valor:,.0f}".replace(",", ".")


class Presentacion:
    TITULOS_CASOS = {
        1: "CASO 1 - Cita atendida con servicio adicional",
        2: "CASO 2 - Veterinario ocupado",
        3: "CASO 3 - Cita cancelada",
        4: "CASO 4 - Cancelación no permitida",
        5: "CASO 5 - Consultas",
    }

    DESCRIPCION_CASOS = {
        1: "Estado inicial: clínica Huellitas con la propietaria Laura Méndez Plata y su perro Rocky registrados.\n"
           "Pasos: programar CIT-001 (10/11/2026 09:00, Juliana Ortiz, CG) y atenderla con el servicio adicional "
           "VAC (factura FAC-001).",
        2: "Estado inicial: Huellitas con CIT-001 programada (Rocky, 10/11/2026 09:00, Juliana Ortiz) y la "
           "propietaria Camila Duarte Serrano con su conejo Copito registrados.\n"
           "Pasos: programar CIT-002 (DES) el 10/11/2026 a las 09:00 con Juliana (se rechaza) y luego a las 10:00.",
        3: "Estado inicial: clínica Patitas Felices con el propietario Andrés Rueda Ardila y su gata Luna "
           "registrados.\n"
           "Pasos: programar CIT-003 (ECO, 12/11/2026 15:00, Sergio Arenas) y cancelarla el 11/11/2026.",
        4: "Estado inicial: Huellitas con CIT-001 ya atendida (factura FAC-001 por $ 105.000).\n"
           "Paso: cancelar CIT-001 el 11/11/2026 (se rechaza).",
        5: "Estado inicial: Huellitas con CIT-001 atendida y CIT-002 programada; Patitas Felices con CIT-003 "
           "cancelada.\n"
           "Pasos: consultar las citas de Huellitas del 10/11/2026 y el historial de la gata Luna.",
    }

    def __init__(self):
        self._repositorio = RepositorioClinicas()
        self._datos_ejemplo = DatosEjemplo(self._repositorio)

    def iniciar_interfaz(self) -> None:
        from presentacion.interfaz import construir_interfaz
        construir_interfaz(self).launch()

    # ------------------------------------------------------------------ registros
    def registrar_clinica(self, nit, nombre, municipio, dane, dpto, direccion, barrio) -> str:
        try:
            clinica = Clinica(nit, nombre, municipio, dane, dpto, direccion, barrio)
            self._repositorio.registrar(clinica)
            return f"[ÉXITO] Clínica '{clinica.nombre}' registrada exitosamente."
        except ReglaNegocioError as error:
            return f"[RECHAZADO] {error}"

    def registrar_veterinario(self, nit, cedula, nombre, tarjeta) -> str:
        try:
            clinica = self._repositorio.buscar(nit)
            veterinario = clinica.registrar_veterinario(cedula, nombre, tarjeta)
            return f"[ÉXITO] Veterinario(a) {veterinario.nombre} registrado(a) en {clinica.nombre}."
        except ReglaNegocioError as error:
            return f"[RECHAZADO] {error}"

    def registrar_servicio(self, nit, codigo, nombre, tarifa) -> str:
        try:
            clinica = self._repositorio.buscar(nit)
            servicio = clinica.registrar_servicio(codigo, nombre, tarifa)
            return (f"[ÉXITO] Servicio {servicio.codigo} - {servicio.nombre} ({_moneda(servicio.tarifa)}) "
                    f"registrado en {clinica.nombre}.")
        except ReglaNegocioError as error:
            return f"[RECHAZADO] {error}"

    def registrar_propietario(self, nit, cedula, nombre, telefono, municipio) -> str:
        try:
            clinica = self._repositorio.buscar(nit)
            propietario = clinica.registrar_propietario(cedula, nombre, telefono, municipio)
            return f"[ÉXITO] Propietario(a) {propietario.nombre} registrado(a) en {clinica.nombre}."
        except ReglaNegocioError as error:
            return f"[RECHAZADO] {error}"

    def registrar_mascota(self, nit, ced_prop, nombre, especie, raza, anio, peso) -> str:
        try:
            clinica = self._repositorio.buscar(nit)
            mascota = clinica.registrar_mascota(ced_prop, nombre, especie, raza, anio, peso)
            propietario = clinica.buscar_propietario(ced_prop)
            return (f"[ÉXITO] Mascota '{mascota.nombre}' registrada para {propietario.nombre} "
                    f"({len(propietario.mascotas)} mascota(s) en total).")
        except ReglaNegocioError as error:
            return f"[RECHAZADO] {error}"

    # ------------------------------------------------------------------ citas
    def programar_cita(self, nit, cod_cita, ced_prop, nom_mascota, fecha, hora, ced_vet, cod_serv) -> str:
        try:
            clinica = self._repositorio.buscar(nit)
            cita = clinica.programar_cita(cod_cita, ced_prop, nom_mascota, fecha, hora, ced_vet, cod_serv)
            return (f"[ÉXITO] Cita {cita.codigo} programada para el {cita.fecha} a las {cita.hora}: "
                    f"{cita.mascota.nombre} con {cita.veterinario.nombre} "
                    f"({cita.servicios[0].nombre}, estado {cita.estado}).")
        except ReglaNegocioError as error:
            return f"[RECHAZADO] {error}"

    def cancelar_cita(self, nit, cod_cita, fecha_cancelacion) -> str:
        try:
            clinica = self._repositorio.buscar(nit)
            cita = clinica.cancelar_cita(cod_cita, fecha_cancelacion)
            return (f"[ÉXITO] Cita {cita.codigo} cancelada exitosamente. "
                    f"Se conserva en el historial con estado {cita.estado}.")
        except ReglaNegocioError as error:
            return f"[RECHAZADO] {error}"

    def atender_cita(self, nit, cod_cita, cod_fac, servs_extra_str) -> str:
        try:
            clinica = self._repositorio.buscar(nit)
            extras = [s.strip() for s in (servs_extra_str or "").split(",") if s.strip()]
            cita = clinica.atender_cita(cod_cita, cod_fac, extras)
            return f"[ÉXITO] Cita {cita.codigo} atendida.\n\n{self._detalle_factura(clinica, cita.factura)}"
        except ReglaNegocioError as error:
            return f"[RECHAZADO] {error}"

    # ------------------------------------------------------------------ consultas
    def consultar_citas_fecha(self, nit, fecha) -> str:
        try:
            clinica = self._repositorio.buscar(nit)
            citas = clinica.consultar_citas_por_fecha(fecha)
            if not citas:
                return f"No hay citas registradas en {clinica.nombre} para la fecha {fecha}."
            lineas = [f"--- Citas en {clinica.nombre} ({citas[0].fecha}) ---"]
            for c in citas:
                lineas.append(f"{c.codigo} | {c.hora} | Mascota: {c.mascota.nombre} | "
                              f"Propietario: {c.propietario.nombre} | Veterinario(a): {c.veterinario.nombre} | "
                              f"Estado: {c.estado}")
            return "\n".join(lineas)
        except ReglaNegocioError as error:
            return f"[RECHAZADO] {error}"

    def consultar_historial_mascota(self, nit, nom_mascota, ced_prop="") -> str:
        try:
            clinica = self._repositorio.buscar(nit)
            citas = clinica.consultar_historial_mascota(nom_mascota, ced_prop)
            if not citas:
                return f"No se encontró historial de citas para la mascota '{nom_mascota}'."
            lineas = [f"--- Historial de citas de '{nom_mascota}' en {clinica.nombre} ---"]
            for c in citas:
                servicios = ", ".join(s.nombre for s in c.servicios)
                lineas.append(f"{c.codigo} | {c.fecha} {c.hora} | Servicios: {servicios} | "
                              f"Veterinario(a): {c.veterinario.nombre} | Estado: {c.estado}")
            return "\n".join(lineas)
        except ReglaNegocioError as error:
            return f"[RECHAZADO] {error}"

    # ------------------------------------------------------------------ utilidades de la interfaz
    def reiniciar(self) -> str:
        self._repositorio.vaciar()
        return "[ÉXITO] Sistema reiniciado: se han eliminado todos los datos registrados."

    # ------------------------------------------------------------------ ejecución de casos de prueba
    def ejecutar_caso(self, numero) -> str:
        try:
            numero = int(numero)
            self._datos_ejemplo.cargar_caso(numero)
        except (TypeError, ValueError):
            return "[RECHAZADO] El número de caso debe ser un entero entre 1 y 5."
        except ReglaNegocioError as error:
            return f"[RECHAZADO] {error}"
        pasos = {
            1: self._pasos_caso_1,
            2: self._pasos_caso_2,
            3: self._pasos_caso_3,
            4: self._pasos_caso_4,
            5: self._pasos_caso_5,
        }[numero]()
        encabezado = [f"===== {self.TITULOS_CASOS[numero]} =====", self.DESCRIPCION_CASOS[numero]]
        return "\n".join(encabezado + pasos)

    def ejecutar_todos_los_casos(self) -> str:
        return "\n\n".join(self.ejecutar_caso(numero) for numero in range(1, 6))

    def _pasos_caso_1(self) -> list:
        return [
            self._paso("Programar CIT-001", self._programar_ejemplo("CIT-001")),
            self._paso("Atender CIT-001 con el servicio adicional VAC",
                       self.atender_cita(NIT_HUELLITAS, "CIT-001", "FAC-001", "VAC")),
        ]

    def _pasos_caso_2(self) -> list:
        return [
            self._paso("Programar CIT-002 a las 09:00 con Juliana Ortiz (ya tiene CIT-001)",
                       self._programar_ejemplo("CIT-002", hora="09:00")),
            self._paso("La propietaria acepta las 10:00 con la misma veterinaria",
                       self._programar_ejemplo("CIT-002")),
        ]

    def _pasos_caso_3(self) -> list:
        return [
            self._paso("Programar CIT-003", self._programar_ejemplo("CIT-003")),
            self._paso("Cancelar CIT-003 el 11/11/2026", self.cancelar_cita(NIT_PATITAS, "CIT-003", "11/11/2026")),
            self._paso("Historial de la gata Luna (la cita queda cancelada y sin factura)",
                       self.consultar_historial_mascota(NIT_PATITAS, "Luna", "1102345678")),
        ]

    def _pasos_caso_4(self) -> list:
        return [
            self._paso("Cancelar CIT-001 el 11/11/2026", self.cancelar_cita(NIT_HUELLITAS, "CIT-001", "11/11/2026")),
        ]

    def _pasos_caso_5(self) -> list:
        return [
            self._paso("Citas de Huellitas del 10/11/2026", self.consultar_citas_fecha(NIT_HUELLITAS, "10/11/2026")),
            self._paso("Historial de la gata Luna", self.consultar_historial_mascota(NIT_PATITAS, "Luna")),
        ]

    def _programar_ejemplo(self, codigo, hora=None) -> str:
        c = DatosEjemplo.CITAS[codigo]
        return self.programar_cita(c["nit"], codigo, c["cedula_propietario"], c["mascota"], c["fecha"],
                                   hora or c["hora"], c["cedula_veterinario"], c["servicio"])

    @staticmethod
    def _paso(titulo: str, resultado: str) -> str:
        return f"\n>> {titulo}\n{resultado}"

    @staticmethod
    def _detalle_factura(clinica, factura) -> str:
        propietario, mascota = factura.propietario, factura.mascota
        lineas = [
            f"=== FACTURA {factura.codigo} ===",
            f"Clínica: {clinica.nombre} (NIT {clinica.nit})",
            f"Fecha: {factura.fecha}",
            f"Propietario: {propietario.nombre} (C.C. {propietario.cedula}, tel. {propietario.telefono})",
            f"Mascota: {mascota.nombre} ({mascota.especie}, {mascota.raza})",
            "Servicios prestados:",
        ]
        for servicio in factura.servicios:
            lineas.append(f"  - {servicio.codigo} | {servicio.nombre}: {_moneda(servicio.tarifa)}")
        lineas.append(f"VALOR TOTAL: {_moneda(factura.valor_total)}")
        return "\n".join(lineas)