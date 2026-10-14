# Sistema de Gestión de Citas Veterinarias

Proyecto desarrollado para la asignatura de Programación II (Universidad de Santander - UDES). Corresponde al Parcial 2, enfocado en el diseño e implementación de un sistema de información para clínicas veterinarias utilizando Programación Orientada a Objetos (POO) y una arquitectura modular en capas.

---

## 1. Descripción del Proyecto

La aplicación permite administrar la infraestructura de múltiples clínicas veterinarias, incluyendo la gestión de veterinarios, catálogos de servicios, propietarios, mascotas, agendamiento de citas, atención clínica con adición de servicios y facturación.

### Funcionalidades Principales
1. Registrar clínicas.
2. Registrar veterinarios y catálogo de servicios por clínica.
3. Registrar propietarios y sus mascotas.
4. Programar citas con control automático de cruce de agenda.
5. Cancelar citas programadas.
6. Atender citas, agregar servicios adicionales y expedir facturas.
7. Consultar citas por fecha y estado.
8. Consultar el historial completo de citas de una mascota.

---

## 2. Reglas de Negocio Implementadas

- **Estados de Cita:** Programada, Cancelada y Atendida. Al crearse, inicia en estado `Programada`.
- **Restricción de Horarios:** Un veterinario o una mascota no pueden tener dos citas en la misma fecha y hora.
- **Transiciones de Estado:** Solo se pueden cancelar o atender citas que estén en estado `Programada`. Las citas canceladas o atendidas conservan su historial.
- **Cálculo de Factura:** Suma la tarifa del servicio inicial más los servicios adicionales agregados durante la atención.
- **Unicidad:** Validación de no duplicidad para el NIT de clínicas, cédulas de propietarios por clínica y códigos de servicio por clínica.
- **Tolerancia a Fallos:** Captura de excepciones personalizadas informando el motivo del rechazo en la interfaz gráfica sin detener la ejecución.

---

## 3. Arquitectura y Estructura del Repositorio

El software sigue una arquitectura orientada a objetos dividida explícitamente por capas y módulos:

```text
.
├── main.py                     # Punto de entrada principal de la aplicación
├── requirements.txt           # Dependencias del proyecto
├── README.md                   # Documentación principal
│
├── datos/                      # Capa de Datos y Persistencia
│   ├── datos_ejemplo.py        # Carga automática de datos de prueba
│   └── repositorio_clinicas.py # Repositorio de almacenamiento en memoria
│
├── diagramas/                  # Documentación UML
│   └── diagramas.md            # Diagramas PlantUML (Dominio, Clases, Objetos, Secuencia)
│
├── presentacion/               # Capa de Presentación
│   ├── interfaz.py             # Definición de la interfaz gráfica (Gradio)
│   └── presentacion.py         # Lógica de interacción con el usuario
│
└── reglas/                     # Capa de Lógica y Reglas de Negocio
    ├── clinica.py              # Gestión central de la clínica
    ├── entidades.py            # Modelos (Propietario, Mascota, Veterinario, Servicio, Cita, Factura)
    ├── estado_cita.py          # Enumeración de estados de la cita
    ├── excepciones.py          # Excepciones personalizadas del dominio
    └── validaciones.py         # Validaciones de reglas de negocio
```

---

## 4. Diagramas UML

El diseño estructural, de comportamiento e interacción del sistema se encuentra documentado y visualizado en la carpeta de diagramas:

👉 **[Ver Diagramas UML completos (PlantUML)](diagramas/diagramas.md)**

Incluye:
- **Diseño Estructural:** Diagramas de Dominio, Clases por Capas y Objetos.
- **Diseño de Comportamiento:** Diagrama Estructurado (*Atender Cita*).
- **Diseño de Interacción:** Diagramas de Secuencia (*Programar Cita*, *Cancelar Cita*, *Atender Cita y Generar Factura*).

---

## 5. Requisitos e Instalación

### Requisitos previos
- Python 3.10 o superior

### Instalación de dependencias
```bash
pip install -r requirements.txt
```

### Ejecución de la aplicación
```bash
python main.py
```
El servidor local se iniciará y la aplicación estará disponible en la consola/navegador a través de la interfaz de Gradio en `http://127.0.0.1:7860`.

---

## 6. Sustentación en Video

El video explicativo del diseño, recorrido del código y ejecución en vivo de los casos de prueba se encuentra disponible en el siguiente enlace:

- **Enlace al video:** *(Pendiente)*

---

## 7. Autor

- **Erick Santiago Rincón Rojas**  
  Código de estudiante: `01251151002`  
  Estudiante de Ingeniería en Ciencias de la Computación e Inteligencia Artificial  
  Universidad de Santander (UDES)  
  Bucaramanga, Santander, Colombia
