"""Datos de los ejemplos de prueba del enunciado y su carga automática en el repositorio."""
from datos.repositorio_clinicas import RepositorioClinicas
from reglas.clinica import Clinica
from reglas.estado_cita import EstadoCita
from reglas.excepciones import DatoInvalidoError, RegistroNoEncontradoError

NIT_HUELLITAS = "901456789-1"
NIT_PATITAS = "900987654-3"


class DatosEjemplo:
    # nit -> (datos de la clínica, veterinarios, catálogo de servicios)
    CLINICAS = {
        NIT_HUELLITAS: {
            "datos": ("Clínica Veterinaria Huellitas", "San Gil", "68679", "Santander",
                      "Calle 12 # 9-40", "Centro"),
            "veterinarios": [
                ("63512478", "Juliana Ortiz Ramírez", "TP-18452"),
                ("91254863", "Mauricio Pinzón Gómez", "TP-20117"),
            ],
            "servicios": [
                ("CG", "Consulta general", 60000),
                ("VAC", "Vacunación", 45000),
                ("DES", "Desparasitación", 30000),
                ("PEL", "Baño y peluquería", 50000),
            ],
        },
        NIT_PATITAS: {
            "datos": ("Clínica Veterinaria Patitas Felices", "Floridablanca", "68276", "Santander",
                      "Carrera 27 # 30-15", "Cañaveral"),
            "veterinarios": [
                ("13745821", "Sergio Arenas Villamizar", "TP-15893"),
                ("37896542", "Diana Carolina Rey Moreno", "TP-22406"),
                ("1098654321", "Felipe Castellanos Díaz", "TP-31578"),
            ],
            "servicios": [
                ("CG", "Consulta general", 65000),
                ("VAC", "Vacunación", 48000),
                ("DES", "Desparasitación", 32000),
                ("ECO", "Ecografía", 120000),
            ],
        },
    }

    # Propietarios de los casos de prueba, con su mascota (nombre, especie, raza, año, peso).
    PROPIETARIOS = [
        {"nit": NIT_HUELLITAS, "cedula": "1098765432", "nombre": "Laura Méndez Plata",
         "telefono": "3157894561", "municipio": "Bucaramanga",
         "mascota": ("Rocky", "Perro", "Criolla", 2023, 18)},
        {"nit": NIT_HUELLITAS, "cedula": "1005678912", "nombre": "Camila Duarte Serrano",
         "telefono": "3204567812", "municipio": "San Gil",
         "mascota": ("Copito", "Conejo", "Cabeza de león", 2025, 1.5)},
        {"nit": NIT_PATITAS, "cedula": "1102345678", "nombre": "Andrés Rueda Ardila",
         "telefono": "3016789023", "municipio": "Piedecuesta",
         "mascota": ("Luna", "Gato", "Siamés", 2022, 4)},
    ]

    # Citas de los casos de prueba (con su atención o cancelación cuando aplica).
    CITAS = {
        "CIT-001": {"nit": NIT_HUELLITAS, "cedula_propietario": "1098765432", "mascota": "Rocky",
                    "fecha": "10/11/2026", "hora": "09:00", "cedula_veterinario": "63512478",
                    "servicio": "CG", "atencion": ("FAC-001", ["VAC"])},
        "CIT-002": {"nit": NIT_HUELLITAS, "cedula_propietario": "1005678912", "mascota": "Copito",
                    "fecha": "10/11/2026", "hora": "10:00", "cedula_veterinario": "63512478",
                    "servicio": "DES"},
        "CIT-003": {"nit": NIT_PATITAS, "cedula_propietario": "1102345678", "mascota": "Luna",
                    "fecha": "12/11/2026", "hora": "15:00", "cedula_veterinario": "13745821",
                    "servicio": "ECO", "cancelacion": "11/11/2026"},
    }

    def __init__(self, repositorio: RepositorioClinicas):
        self._repositorio = repositorio

    def cargar_clinica(self, nit: str) -> Clinica:
        if self._repositorio.existe(nit):
            return self._repositorio.buscar(nit)
        if nit not in self.CLINICAS:
            raise RegistroNoEncontradoError(f"No hay datos de ejemplo para la clínica con NIT {nit}.")
        ejemplo = self.CLINICAS[nit]
        clinica = Clinica(nit, *ejemplo["datos"])
        for cedula, nombre, tarjeta in ejemplo["veterinarios"]:
            clinica.registrar_veterinario(cedula, nombre, tarjeta)
        for codigo, nombre, tarifa in ejemplo["servicios"]:
            clinica.registrar_servicio(codigo, nombre, tarifa)
        self._repositorio.registrar(clinica)
        return clinica

    def cargar_propietario(self, cedula: str) -> None:
        ejemplo = next((p for p in self.PROPIETARIOS if p["cedula"] == cedula), None)
        if ejemplo is None:
            raise RegistroNoEncontradoError(f"No hay datos de ejemplo para el propietario con cédula {cedula}.")
        clinica = self.cargar_clinica(ejemplo["nit"])
        try:
            clinica.buscar_propietario(cedula)
        except RegistroNoEncontradoError:
            clinica.registrar_propietario(cedula, ejemplo["nombre"], ejemplo["telefono"], ejemplo["municipio"])
            nombre, especie, raza, anio, peso = ejemplo["mascota"]
            clinica.registrar_mascota(cedula, nombre, especie, raza, anio, peso)

    def cargar_cita(self, codigo: str) -> None:
        ejemplo = self._ejemplo_cita(codigo)
        self.cargar_propietario(ejemplo["cedula_propietario"])
        clinica = self._repositorio.buscar(ejemplo["nit"])
        try:
            clinica.buscar_cita(codigo)
        except RegistroNoEncontradoError:
            clinica.programar_cita(codigo, ejemplo["cedula_propietario"], ejemplo["mascota"],
                                   ejemplo["fecha"], ejemplo["hora"], ejemplo["cedula_veterinario"],
                                   ejemplo["servicio"])

    def cargar_atencion(self, codigo: str) -> None:
        ejemplo = self._ejemplo_cita(codigo)
        if "atencion" not in ejemplo:
            raise RegistroNoEncontradoError(f"La cita de ejemplo {codigo} no tiene una atención definida.")
        self.cargar_cita(codigo)
        clinica = self._repositorio.buscar(ejemplo["nit"])
        if clinica.buscar_cita(codigo).estado == EstadoCita.PROGRAMADA:
            codigo_factura, extras = ejemplo["atencion"]
            clinica.atender_cita(codigo, codigo_factura, extras)

    def cargar_cancelacion(self, codigo: str) -> None:
        ejemplo = self._ejemplo_cita(codigo)
        if "cancelacion" not in ejemplo:
            raise RegistroNoEncontradoError(f"La cita de ejemplo {codigo} no tiene una cancelación definida.")
        self.cargar_cita(codigo)
        clinica = self._repositorio.buscar(ejemplo["nit"])
        if clinica.buscar_cita(codigo).estado == EstadoCita.PROGRAMADA:
            clinica.cancelar_cita(codigo, ejemplo["cancelacion"])

    def cargar_caso(self, numero: int) -> None:
        """Reinicia el repositorio y deja el estado inicial del caso de prueba indicado (1 a 5)."""
        if numero not in (1, 2, 3, 4, 5):
            raise DatoInvalidoError("Los casos de prueba van del 1 al 5.")
        self._repositorio.vaciar()
        if numero == 1:
            self.cargar_propietario("1098765432")
        elif numero == 2:
            self.cargar_cita("CIT-001")
            self.cargar_propietario("1005678912")
        elif numero == 3:
            self.cargar_propietario("1102345678")
        elif numero == 4:
            self.cargar_atencion("CIT-001")
        else:
            self.cargar_atencion("CIT-001")
            self.cargar_cita("CIT-002")
            self.cargar_cancelacion("CIT-003")

    def _ejemplo_cita(self, codigo: str) -> dict:
        if codigo not in self.CITAS:
            raise RegistroNoEncontradoError(f"No hay datos de ejemplo para la cita {codigo}.")
        return self.CITAS[codigo]
