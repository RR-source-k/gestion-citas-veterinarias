"""Capa de presentación: interfaz gráfica con Gradio."""
import gradio as gr

from datos.datos_ejemplo import NIT_HUELLITAS, NIT_PATITAS


def construir_interfaz(presentacion) -> gr.Blocks:
    with gr.Blocks(title="Gestión de Citas Veterinarias") as app:
        gr.Markdown("# 🐾 Sistema de Gestión de Citas Veterinarias")

        # ------------------------------------------------------------ precarga
        with gr.Accordion("⚡ Autocompletar campos con ejemplos de prueba", open=True):
            gr.Markdown("Haz clic en un botón para **rellenar automáticamente los formularios** de las pestañas (Propietario, Mascota y Cita) sin registrarlos todavía:")
            with gr.Row():
                btn_fill_huellitas = gr.Button("Rellenar Clínica Huellitas")
                btn_fill_patitas = gr.Button("Rellenar Clínica Patitas Felices")
            with gr.Row():
                btn_fill_cita1 = gr.Button("Rellenar Datos Cita 1 (CIT-001 / Laura / Rocky)")
                btn_fill_cita2 = gr.Button("Rellenar Datos Cita 2 (CIT-002 / Camila / Copito)")
                btn_fill_cita3 = gr.Button("Rellenar Datos Cita 3 (CIT-003 / Andrés / Luna)")
            btn_reiniciar = gr.Button("Reiniciar sistema (borra datos registrados)", variant="stop")
            out_precarga = gr.Textbox(label="Estado del sistema / Mensajes", lines=2)

        btn_reiniciar.click(fn=presentacion.reiniciar, inputs=None, outputs=out_precarga)

        with gr.Tabs():
            # -------------------------------------------------------- 1. clínica
            with gr.Tab("1. Registrar Clínica"):
                nit_reg = gr.Textbox(label="NIT (ej. 901456789-1)")
                nom_reg = gr.Textbox(label="Nombre de la Clínica")
                mun_reg = gr.Textbox(label="Municipio")
                dane_reg = gr.Textbox(label="Código DANE")
                dpto_reg = gr.Textbox(label="Departamento")
                dir_reg = gr.Textbox(label="Dirección")
                barrio_reg = gr.Textbox(label="Barrio")
                btn_reg = gr.Button("Registrar Clínica", variant="primary")
                out_reg = gr.Textbox(label="Resultado", lines=3)
                btn_reg.click(presentacion.registrar_clinica,
                              inputs=[nit_reg, nom_reg, mun_reg, dane_reg, dpto_reg, dir_reg, barrio_reg],
                              outputs=out_reg)

            # -------------------------------------------------------- 2. vet / servicio
            with gr.Tab("2. Registrar Vet / Servicio"):
                gr.Markdown("### Registrar Veterinario")
                nit_v = gr.Textbox(label="NIT Clínica")
                ced_v = gr.Textbox(label="Cédula Veterinario")
                nom_v = gr.Textbox(label="Nombre Completo")
                tp_v = gr.Textbox(label="Tarjeta Profesional")
                btn_v = gr.Button("Registrar Veterinario", variant="primary")
                out_v = gr.Textbox(label="Resultado", lines=3)
                btn_v.click(presentacion.registrar_veterinario, inputs=[nit_v, ced_v, nom_v, tp_v], outputs=out_v)

                gr.Markdown("---")
                gr.Markdown("### Registrar Servicio")
                nit_s = gr.Textbox(label="NIT Clínica")
                cod_s = gr.Textbox(label="Código Servicio (ej. CG, VAC)")
                nom_s = gr.Textbox(label="Nombre Servicio")
                tar_s = gr.Number(label="Tarifa ($)")
                btn_s = gr.Button("Registrar Servicio", variant="primary")
                out_s = gr.Textbox(label="Resultado", lines=3)
                btn_s.click(presentacion.registrar_servicio, inputs=[nit_s, cod_s, nom_s, tar_s], outputs=out_s)

            # -------------------------------------------------------- 3. propietario / mascota
            with gr.Tab("3. Registrar Propietario / Mascota"):
                gr.Markdown("### Registrar Propietario")
                nit_pr = gr.Textbox(label="NIT Clínica")
                ced_pr = gr.Textbox(label="Cédula Propietario")
                nom_pr = gr.Textbox(label="Nombre Propietario")
                tel_pr = gr.Textbox(label="Teléfono")
                mun_pr = gr.Textbox(label="Municipio de residencia")
                btn_pr = gr.Button("Registrar Propietario", variant="primary")
                out_pr = gr.Textbox(label="Resultado", lines=3)
                btn_pr.click(presentacion.registrar_propietario,
                             inputs=[nit_pr, ced_pr, nom_pr, tel_pr, mun_pr], outputs=out_pr)

                gr.Markdown("---")
                gr.Markdown("### Registrar Mascota")
                nit_m = gr.Textbox(label="NIT Clínica")
                ced_m = gr.Textbox(label="Cédula del Propietario")
                nom_m = gr.Textbox(label="Nombre Mascota")
                esp_m = gr.Textbox(label="Especie")
                raz_m = gr.Textbox(label="Raza")
                ani_m = gr.Number(label="Año aproximado de nacimiento", precision=0)
                pes_m = gr.Number(label="Peso (kg)")
                btn_m = gr.Button("Registrar Mascota", variant="primary")
                out_m = gr.Textbox(label="Resultado", lines=3)
                btn_m.click(presentacion.registrar_mascota,
                            inputs=[nit_m, ced_m, nom_m, esp_m, raz_m, ani_m, pes_m], outputs=out_m)

            # -------------------------------------------------------- 4. programar
            with gr.Tab("4. Programar Cita"):
                nit_p = gr.Textbox(label="NIT Clínica")
                cod_cit = gr.Textbox(label="Código Cita")
                ced_p = gr.Textbox(label="Cédula Propietario")
                nom_mp = gr.Textbox(label="Nombre Mascota")
                with gr.Row():
                    fec_p = gr.Textbox(label="Fecha (DD/MM/AAAA)")
                    hor_p = gr.Textbox(label="Hora (HH:MM, 24 horas)")
                with gr.Row():
                    vet_p = gr.Textbox(label="Cédula Veterinario")
                    ser_p = gr.Textbox(label="Código Servicio")
                btn_p = gr.Button("Programar Cita", variant="primary")
                out_p = gr.Textbox(label="Resultado", lines=4)
                btn_p.click(presentacion.programar_cita,
                            inputs=[nit_p, cod_cit, ced_p, nom_mp, fec_p, hor_p, vet_p, ser_p], outputs=out_p)

            # -------------------------------------------------------- 5. cancelar
            with gr.Tab("5. Cancelar Cita"):
                nit_c = gr.Textbox(label="NIT Clínica")
                cod_cit_c = gr.Textbox(label="Código Cita a Cancelar")
                fec_c = gr.Textbox(label="Fecha en que se cancela (DD/MM/AAAA)")
                btn_c = gr.Button("Cancelar Cita", variant="stop")
                out_c = gr.Textbox(label="Resultado", lines=4)
                btn_c.click(presentacion.cancelar_cita, inputs=[nit_c, cod_cit_c, fec_c], outputs=out_c)

            # -------------------------------------------------------- 6. atender
            with gr.Tab("6. Atender Cita / Facturar"):
                nit_a = gr.Textbox(label="NIT Clínica")
                cod_cit_a = gr.Textbox(label="Código Cita")
                cod_fac = gr.Textbox(label="Código Factura")
                ext_a = gr.Textbox(label="Servicios adicionales (códigos separados por coma)")
                btn_a = gr.Button("Atender y Facturar", variant="primary")
                out_a = gr.Textbox(label="Resultado", lines=12)
                btn_a.click(presentacion.atender_cita, inputs=[nit_a, cod_cit_a, cod_fac, ext_a], outputs=out_a)

            # -------------------------------------------------------- 7. consultas
            with gr.Tab("7. Consultas"):
                gr.Markdown("### Consultar Citas por Fecha")
                nit_q1 = gr.Textbox(label="NIT Clínica")
                fec_q1 = gr.Textbox(label="Fecha (DD/MM/AAAA)")
                btn_q1 = gr.Button("Consultar Citas", variant="primary")
                out_q1 = gr.Textbox(label="Resultado", lines=6)
                btn_q1.click(presentacion.consultar_citas_fecha, inputs=[nit_q1, fec_q1], outputs=out_q1)

                gr.Markdown("---")
                gr.Markdown("### Historial de Mascota")
                nit_q2 = gr.Textbox(label="NIT Clínica")
                nom_q2 = gr.Textbox(label="Nombre Mascota")
                ced_q2 = gr.Textbox(label="Cédula del propietario (opcional)")
                btn_q2 = gr.Button("Consultar Historial", variant="primary")
                out_q2 = gr.Textbox(label="Resultado", lines=6)
                btn_q2.click(presentacion.consultar_historial_mascota,
                             inputs=[nit_q2, nom_q2, ced_q2], outputs=out_q2)

            # -------------------------------------------------------- 8. casos de prueba
            with gr.Tab("8. Casos de prueba"):
                gr.Markdown("Cada botón **reinicia el sistema**, ejecuta automáticamente el caso completo "
                            "y muestra las respuestas esperadas.")
                with gr.Row():
                    botones_ejecutar = [gr.Button(f"Ejecutar caso {n}") for n in range(1, 6)]
                btn_todos = gr.Button("Ejecutar los 5 casos", variant="primary")
                out_casos = gr.Textbox(label="Resultado de la ejecución", lines=22, max_lines=60)
                for numero, boton in enumerate(botones_ejecutar, start=1):
                    boton.click(fn=lambda n=numero: presentacion.ejecutar_caso(n), inputs=None, outputs=out_casos)
                btn_todos.click(fn=presentacion.ejecutar_todos_los_casos, inputs=None, outputs=out_casos)

        # Configuración de los eventos de autocompletado simultáneo
        btn_fill_huellitas.click(
            fn=lambda: (
                NIT_HUELLITAS, "Clínica Veterinaria Huellitas", "San Gil", "68679", "Santander", "Calle 12 # 9-40", "Centro"
            ),
            inputs=None,
            outputs=[nit_reg, nom_reg, mun_reg, dane_reg, dpto_reg, dir_reg, barrio_reg]
        )

        btn_fill_patitas.click(
            fn=lambda: (
                NIT_PATITAS, "Clínica Veterinaria Patitas Felices", "Floridablanca", "68276", "Santander", "Carrera 27 # 30-15", "Cañaveral"
            ),
            inputs=None,
            outputs=[nit_reg, nom_reg, mun_reg, dane_reg, dpto_reg, dir_reg, barrio_reg]
        )

        # Rellena Propietario (Laura), Mascota (Rocky) y Cita (CIT-001) en un solo clic
        btn_fill_cita1.click(
            fn=lambda: (
                NIT_HUELLITAS, "1098765432", "Laura Méndez Plata", "3157894561", "Bucaramanga",
                NIT_HUELLITAS, "1098765432", "Rocky", "Perro", "Criolla", 2023, 18,
                NIT_HUELLITAS, "CIT-001", "1098765432", "Rocky", "10/11/2026", "09:00", "63512478", "CG"
            ),
            inputs=None,
            outputs=[
                nit_pr, ced_pr, nom_pr, tel_pr, mun_pr,
                nit_m, ced_m, nom_m, esp_m, raz_m, ani_m, pes_m,
                nit_p, cod_cit, ced_p, nom_mp, fec_p, hor_p, vet_p, ser_p
            ]
        )

        # Rellena Propietario (Camila), Mascota (Copito) y Cita (CIT-002) en un solo clic
        btn_fill_cita2.click(
            fn=lambda: (
                NIT_HUELLITAS, "1005678912", "Camila Duarte Serrano", "3204567812", "San Gil",
                NIT_HUELLITAS, "1005678912", "Copito", "Conejo", "Cabeza de león", 2025, 1.5,
                NIT_HUELLITAS, "CIT-002", "1005678912", "Copito", "10/11/2026", "10:00", "63512478", "DES"
            ),
            inputs=None,
            outputs=[
                nit_pr, ced_pr, nom_pr, tel_pr, mun_pr,
                nit_m, ced_m, nom_m, esp_m, raz_m, ani_m, pes_m,
                nit_p, cod_cit, ced_p, nom_mp, fec_p, hor_p, vet_p, ser_p
            ]
        )

        # Rellena Propietario (Andrés), Mascota (Luna) y Cita (CIT-003) en un solo clic
        btn_fill_cita3.click(
            fn=lambda: (
                NIT_PATITAS, "1102345678", "Andrés Rueda Ardila", "3016789023", "Piedecuesta",
                NIT_PATITAS, "1102345678", "Luna", "Gato", "Siamés", 2022, 4,
                NIT_PATITAS, "CIT-003", "1102345678", "Luna", "12/11/2026", "15:00", "13745821", "ECO"
            ),
            inputs=None,
            outputs=[
                nit_pr, ced_pr, nom_pr, tel_pr, mun_pr,
                nit_m, ced_m, nom_m, esp_m, raz_m, ani_m, pes_m,
                nit_p, cod_cit, ced_p, nom_mp, fec_p, hor_p, vet_p, ser_p
            ]
        )

    return app