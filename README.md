# Sistema de Gestion de Citas Veterinarias

Proyecto desarrollado para la asignatura de Programacion II (Universidad de Santander - UDES). Corresponde al Parcial 2, enfocado en el diseno e implementacion de un sistema de informacion para clinicas veterinarias utilizando Programacion Orientada a Objetos (POO) y una arquitectura modular por capas.

---

## 1. Descripcion del Proyecto

La aplicacion permite administrar la infraestructura de multiples clinicas veterinarias, incluyendo la gestion de veterinarios, catalogos de servicios, propietarios, mascotas, agendamiento de citas, atencion clinica con adicion de servicios y facturacion.

### Funcionalidades Principales
1. Registrar clinica.
2. Registrar veterinarios y catalogo de servicios por clinica.
3. Registrar propietarios y sus mascotas.
4. Programar citas con control automatico de cruce de agenda.
5. Cancelar citas programadas.
6. Atender citas, agregar servicios adicionales y expedir facturas.
7. Consultar citas por fecha y estado.
8. Consultar el historial completo de citas de una mascota.

---

## 2. Reglas de Negocio Implementadas

- Estados de Cita: Programada, Cancelada y Atendida. Al crearse, inicia en estado Programada.
- Restriccion de Horarios: Un veterinario o una mascota no pueden tener dos citas en la misma fecha y hora.
- Transiciones de Estado: Solo se pueden cancelar o atender citas que esten en estado Programada. Las citas canceladas o atendidas conservan su historial y no se pueden modificar.
- Calculo de Factura: Suma la tarifa del servicio inicial mas los servicios adicionales agregados durante la atencion.
- Unicidad: Validacion de no duplicidad para el NIT de clinicas, cedulas de propietarios por clinica y codigos de servicio por clinica.
- Tolerancia a Fallos: Captura transparente de excepciones informando el motivo del rechazo en la interfaz grafica sin detener la aplicacion.

---

## 3. Arquitectura del Sistema

El software sigue una arquitectura orientada a objetos dividida en tres capas:

```text
├── Capa Presentacion (codigo.ipynb - Gradio UI + Clase Presentacion)
│   ├── Capa Logica de Negocio (Clases: Clinica, Cita, Propietario, Mascota, Veterinario, Servicio, Factura, EstadoCita)
│   │   └── Capa Almacenamiento (Colecciones en memoria dentro de cada entidad)
```

---

## 4. Estructura del Repositorio

```text
.
├── codigo.ipynb                # Codigo fuente completo (Backend POO + Interfaz Gradio)
└── README.md                   # Documentacion principal del repositorio
```

---

## 5. Diagramas UML del Diseno

- Diagramas UML (Pendiente de subir en un proximo commit)

---

## 6. Requisitos e Instalacion

### Instalacion de dependencias
```bash
pip install gradio
```

### Ejecucion de la aplicacion
Ejecutar todas las celdas del notebook `codigo.ipynb`. Se iniciara el servidor local de Gradio y la aplicacion estara disponible en http://127.0.0.1:7860.

---

## 7. Sustentacion en Video

El video explicativo del diseno, recorrido del codigo y ejecucion en vivo de los casos de prueba se encuentra disponible en el siguiente enlace:

- Enlace al video: (Pendiente)

---

## 8. Autor

- Erick Santiago Rincon Rojas  
  Codigo de estudiante: 01251151002  
  Estudiante de Ingenieria en Ciencias de la Computacion e Inteligencia Artificial  
  Universidad de Santander (UDES)  
  Bucaramanga, Santander, Colombia
