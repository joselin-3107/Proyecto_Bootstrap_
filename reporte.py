"""
reporte.py

Generación automática del reporte PDF
del proyecto Bootstrap.
"""

# =====================================================
# IMPORTACIONES
# =====================================================

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image
)

from reportlab.lib.styles import getSampleStyleSheet

from reportlab.lib import colors

from reportlab.lib.units import cm

from reportlab.lib.enums import TA_CENTER

from reportlab.pdfbase.pdfmetrics import stringWidth

from datetime import datetime

from zoneinfo import ZoneInfo

import os


# =====================================================
# FUNCIÓN PRINCIPAL
# =====================================================

def generar_reporte_pdf(

    nombre_archivo,

    area_A,

    area_B,

    area_promedio,

    tiempo,

    velocidad_superficial,

    velocidad_media,

    caudal,

    media,

    sesgo,

    error,

    ic_inf,

    ic_sup,

    p_valor,

    numero_bootstrap,

    conclusion
):
    # =====================================================
    # CREAR DOCUMENTO
    # =====================================================

    documento = SimpleDocTemplate(

        nombre_archivo,

        rightMargin=2*cm,

        leftMargin=2*cm,

        topMargin=2*cm,

        bottomMargin=2*cm

    )

    estilos = getSampleStyleSheet()

    titulo = estilos["Title"]
    titulo.alignment = TA_CENTER

    subtitulo = estilos["Heading2"]
    subtitulo.alignment = TA_CENTER

    normal = estilos["BodyText"]

    elementos = []

        # =====================================================
    # PORTADA
    # =====================================================

    elementos.append(
        Paragraph(
            "UNIVERSIDAD NACIONAL DE LOJA",
            titulo
        )
    )

    elementos.append(
        Paragraph(
            "Carrera de Ingeniería Ambiental",
            subtitulo
        )
    )

    elementos.append(
        Spacer(1,0.5*cm)
    )

    elementos.append(
        Paragraph(
            "<b>Proyecto Bootstrap</b>",
            subtitulo
        )
    )

    elementos.append(
        Paragraph(
            "Estimación de la incertidumbre del caudal del río Malacatos mediante el método Bootstrap",
            normal
        )
    )

    elementos.append(
        Spacer(1,0.5*cm)
    )

    elementos.append(
        Paragraph(
            "<b>Autora:</b> Joselin Anai Ulloa Zhanay",
            normal
        )
    )

    fecha = datetime.now(
        Zoneinfo("America/Guayaquil")
    ).strftime("%d/%m/%Y %H:%M")

    elementos.append(
        Paragraph(
            f"<b>Fecha de generación:</b> {fecha}",
            normal
        )
    )

    elementos.append(
        Spacer(1,1*cm)
    )

    elementos.append(
        Paragraph(
            "<b>1. Resultados Hidráulicos</b>",
            subtitulo
        )
    )

    datos_hidraulicos = [

        ["Parámetro","Valor"],

        ["Área Sección A",f"{area_A:.4f} m²"],

        ["Área Sección B",f"{area_B:.4f} m²"],

        ["Área Promedio",f"{area_promedio:.4f} m²"],

        ["Tiempo promedio",f"{tiempo:.3f} s"],

        ["Velocidad superficial",f"{velocidad_superficial:.3f} m/s"],

        ["Velocidad media",f"{velocidad_media:.3f} m/s"],

        ["Caudal",f"{caudal:.3f} m³/s"]

    ]

    tabla1 = Table(datos_hidraulicos)

    tabla1.setStyle(TableStyle([

        ("BACKGROUND",(0,0),(-1,0),colors.darkblue),

        ("TEXTCOLOR",(0,0),(-1,0),colors.white),

        ("GRID",(0,0),(-1,-1),1,colors.black),

        ("BACKGROUND",(0,1),(-1,-1),colors.beige),

        ("ALIGN",(0,0),(-1,-1),"CENTER")

    ]))

    elementos.append(tabla1)

    elementos.append(Spacer(1,0.6*cm))

        # =====================================================
    # RESULTADOS BOOTSTRAP
    # =====================================================

    elementos.append(
        Paragraph(
            "<b>2. Resultados Bootstrap</b>",
            subtitulo
        )
    )

    datos_bootstrap = [

        ["Estadístico", "Valor"],

        ["Número de simulaciones", str(numero_bootstrap)],

        ["Media Bootstrap", f"{media:.4f} m³/s"],

        ["Sesgo", f"{sesgo:.6f}"],

        ["Error estándar", f"{error:.6f}"],

        ["IC 95%", f"{ic_inf:.4f} - {ic_sup:.4f}"],

        ["Valor p", f"{p_valor:.5f}"]

    ]

    tabla2 = Table(datos_bootstrap)

    tabla2.setStyle(TableStyle([

        ("BACKGROUND", (0,0), (-1,0), colors.darkgreen),

        ("TEXTCOLOR", (0,0), (-1,0), colors.white),

        ("GRID", (0,0), (-1,-1), 1, colors.black),

        ("BACKGROUND", (0,1), (-1,-1), colors.whitesmoke),

        ("ALIGN", (0,0), (-1,-1), "CENTER")

    ]))

    elementos.append(tabla2)

    elementos.append(Spacer(1,0.8*cm))

        # =====================================================
    # CONCLUSIÓN
    # =====================================================

    elementos.append(
        Paragraph(
            "<b>3. Conclusión</b>",
            subtitulo
        )
    )

    elementos.append(
        Paragraph(
            conclusion,
            normal
        )
    )

    elementos.append(
        Spacer(1,0.8*cm)
    )

        # =====================================================
    # PIE DEL REPORTE
    # =====================================================

    elementos.append(
        Paragraph(
            "<hr/>",
            normal
        )
    )

    elementos.append(
        Paragraph(
            "Proyecto desarrollado en Python utilizando Shiny, Bootstrap, SciPy y ReportLab.",
            normal
        )
    )

    # =====================================================
    # GENERAR PDF
    # =====================================================

    documento.build(elementos)