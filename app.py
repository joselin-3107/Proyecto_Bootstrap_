"""
Aplicación Web - Proyecto Bootstrap

Estimación de la incertidumbre del caudal
del río Malacatos mediante Bootstrap.

Universidad Nacional de Loja
Ingeniería Ambiental
"""

# =====================================================
# IMPORTACIONES
# =====================================================

from shiny import App, ui, render
import matplotlib.pyplot as plt
import pandas as pd
import sys
import os
import numpy as np

# Permite importar los módulos de la carpeta Codigo

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CODIGO_DIR = os.path.join(BASE_DIR, "..", "Codigo")

sys.path.append(CODIGO_DIR)

from reporte import generar_reporte_pdf

# =====================================================
# MÓDULOS DEL PROYECTO
# =====================================================

from datos import *

from integracion import (
    regla_trapecio,
    calcular_tiempo_promedio,
    calcular_velocidad_superficial,
    calcular_velocidad_media,
    calcular_caudal
)

from bootstrap import simulacion_bootstrap

from estadistica import (
    calcular_media,
    calcular_desviacion,
    calcular_intervalo_confianza,
    calcular_sesgo
)

from graficos import prueba_normalidad

# =====================================================
# CÁLCULOS HIDRÁULICOS
# =====================================================

# Área de cada sección
area_A = regla_trapecio(profundidades_A)
area_B = regla_trapecio(profundidades_B)

# Área promedio
area_promedio = (area_A + area_B) / 2

# Tiempo promedio
tiempo_promedio = calcular_tiempo_promedio(tiempos)

# Velocidad superficial
velocidad_superficial = calcular_velocidad_superficial(
    L,
    tiempo_promedio
)

# Velocidad media
velocidad_media = calcular_velocidad_media(
    velocidad_superficial,
    k
)

# Caudal original
caudal_original = calcular_caudal(
    area_promedio,
    velocidad_media
)

# =====================================================
# SIMULACIÓN BOOTSTRAP
# =====================================================

""""
caudales = simulacion_bootstrap(
    tiempos,
    area_promedio,
    L,
    k,
    2000
)
"""


# =====================================================
# INTERFAZ DE LA APLICACIÓN
# =====================================================

app_ui = ui.page_fluid(

    # -----------------------------------------
    # Encabezado
    # -----------------------------------------


    ui.h1(
        "Estimación de la Incertidumbre del Caudal mediante Bootstrap",
        style="text-algin:center;"
    ),

    ui.h4(
        "Río Malacatos - Universidad Nacional de Loja",
        style="text-align:center; color:gray;"
    ),

    ui.hr(),

    ui.h5(
    "Carrera de Ingeniería Ambiental"
    ),

    ui.h6(
    "Proyecto Bootstrap - Estimación de la incertidumbre del caudal"
    ),

    ui.p(
        """
        Aplicación desarrollada para estimar el caudal del río
        mediante integración numérica y simulación Bootstrap.
        """
    ),

    ui.hr(),

    # -----------------------------------------
    # Menú principal
    # -----------------------------------------

    ui.navset_tab(

        # =====================================
        # INICIO
        # =====================================

        ui.nav_panel(

            "🏠 Inicio",

            ui.card(

                ui.card_header("Descripción del proyecto"),

                ui.p(
                    """
                    El presente proyecto tiene como finalidad estimar el caudal del río
                    Malacatos mediante técnicas de integración numérica y evaluar la
                    incertidumbre asociada a dicha estimación utilizando el método
                    Bootstrap. Para ello, se emplean las profundidades medidas en dos
                    secciones transversales del río y los tiempos registrados durante
                    las mediciones con flotador superficial.

                    La aplicación calcula el área hidráulica mediante la Regla del
                    Trapecio, determina la velocidad media del flujo y obtiene el
                    caudal del río. Posteriormente, aplica miles de simulaciones
                    Bootstrap para cuantificar la variabilidad de los resultados y
                    calcular indicadores estadísticos como la media Bootstrap, el
                    sesgo, el error estándar, el intervalo de confianza del 95 % y
                    la prueba de normalidad de Shapiro-Wilk.

                    Además, incorpora herramientas para la visualización gráfica de
                    los resultados, la exportación de datos en formato CSV y la
                    generación automática de reportes técnicos en formato PDF,
                    facilitando el análisis e interpretación de la incertidumbre
                    en estudios hidrológicos.
                    """
                ),

                ui.br(),

                ui.h5("Objetivo General"),

                ui.p(
                    """
                    Desarrollar una aplicación interactiva en Python que permita
                    calcular el caudal del río Malacatos a partir de mediciones
                    hidráulicas de campo y estimar la incertidumbre asociada mediante
                    el método Bootstrap, integrando herramientas de análisis
                    estadístico, visualización gráfica y generación automática de
                    reportes técnicos para facilitar la interpretación y presentación
                    de los resultados obtenidos.
                    """
                )

            )

        ),

        # =====================================
        # DATOS HIDRÁULICOS
        # =====================================

        ui.nav_panel(

            "🌊 Datos Hidráulicos",

            ui.input_numeric(
                "longitud",
                "Longitud del tramo L (m):",
                value=L,
                min=0
            ),

            ui.input_numeric(
                "coeficiente",
                "Coeficiente k:",
                value=k,
                min=0,
                max=1,
                step=0.01
            ),

            ui.layout_columns(

                ui.input_numeric(
                    "t1",
                    "Tiempo 1 (s):",
                    value=tiempos[0]
                ),

                ui.input_numeric(
                    "t2",
                    "Tiempo 2 (s):",
                    value=tiempos[1]
                ),

                ui.input_numeric(
                    "t3",
                    "Tiempo 3 (s):",
                    value=tiempos[2]
                ),
                ui.input_numeric(
                    "t4",
                    "Tiempo 4 (s):",
                    value=tiempos[3]
                ),

                ui.input_numeric(
                    "t5",
                    "Tiempo 5 (s):",
                    value=tiempos[4]
                )
            ),

            ui.hr(),

            ui.output_ui("panel_hidraulico")

        ),

        # =====================================
        # BOOTSTRAP
        # =====================================

        ui.nav_panel(

            "📊 Bootstrap",

            ui.input_select(

                "n_boot",

                "Número de simulaciones Bootstrap:",

                choices=[
                    "500",
                    "1000",
                    "2000",
                    "5000",
                    "10000",
                ],

                selected="2000"

            ),

            ui.br(),

            ui.download_button(
                "descargar_pdf",
                "📄 Descargar reporte PDF"
            ),

            ui.br(),

            ui.output_ui("panel_bootstrap"),

            ui.hr(),

            ui.h4("Conclusión de la prueba de normalidad"),

            ui.output_text_verbatim("conclusion")

        ),

        # =====================================
        # GRÁFICOS
        # =====================================

        ui.nav_panel(

            "📈 Gráficos",

            ui.output_plot("histograma"),

            ui.br(),

            ui.output_plot("qqplot")

        ),

        # =====================================
        # TABLA
        # =====================================

        ui.nav_panel(

            "📋 Simulaciones",

            ui.download_button(
                "descargar_csv",
                "📥 Descargar simulaciones CSV"
        ),

        ui.br(),
        ui.br(),

            ui.output_table("tabla")

        ),

        # =====================================
        # ACERCA
        # =====================================

        ui.nav_panel(

            "ℹ Acerca",

            ui.markdown("""

## Proyecto Bootstrap

**Universidad Nacional de Loja**

Carrera de Ingeniería Ambiental

Autor:
Joselin Anai Ulloa Zhanay

Año:
2026

---

Proyecto desarrollado para estimar la incertidumbre del caudal del río Malacatos mediante el método Bootstrap.

**Lenguaje:** Python

**Framework:** Shiny para Python

""")

        )

    )

)


# =====================================================
# SERVIDOR
# =====================================================

def server(input, output, session):

    from shiny import reactive

    @reactive.calc
    def resultados():
    
        tiempos_usuario = [
    
            input.t1(),
    
            input.t2(),
    
            input.t3(),

            input.t4(),

            input.t5()
    
        ]
    
        area_A = regla_trapecio(profundidades_A)
    
        area_B = regla_trapecio(profundidades_B)
    
        area_promedio = (area_A + area_B) / 2
    
        tiempo_promedio = calcular_tiempo_promedio(
            tiempos_usuario
        )
    
        velocidad_superficial = calcular_velocidad_superficial(
    
            input.longitud(),
    
            tiempo_promedio
    
        )
    
        velocidad_media = calcular_velocidad_media(
    
            velocidad_superficial,
    
            input.coeficiente()
    
        )
    
        caudal = calcular_caudal(
    
            area_promedio,
    
            velocidad_media
    
        )
    
        return {
    
            "area_A": area_A,
    
            "area_B": area_B,
    
            "area_promedio": area_promedio,
    
            "tiempo": tiempo_promedio,
    
            "velocidad_superficial": velocidad_superficial,
    
            "velocidad_media": velocidad_media,
    
            "caudal": caudal,
    
            "tiempos": tiempos_usuario
    
        }

    @reactive.calc
    def caudales():

        r = resultados()

        return simulacion_bootstrap(

            r["tiempos"],

            r["area_promedio"],

            input.longitud(),

            input.coeficiente(),

            int(input.n_boot())

        )

    @reactive.calc
    def estadisticas():

        datos = caudales()

        r = resultados()

        media = calcular_media(datos)

        error = calcular_desviacion(datos)

        sesgo = calcular_sesgo(
            datos,
            r["caudal"]
        )

        ic_inf, ic_sup = calcular_intervalo_confianza(
            datos
        )

        _, p = prueba_normalidad(
            datos
        )

        return {

            "media": media,

            "error": error,

            "sesgo": sesgo,

            "ic_inf": ic_inf,

            "ic_sup": ic_sup,

            "p": p

        }


    # ---------------------------------------------
    # PANEL HIDRÁULICO
    # ---------------------------------------------

    @output
    @render.ui
    def panel_hidraulico():

        r = resultados()

        return ui.layout_columns(

            ui.value_box(
                "Área Sección A",
                f"{r['area_A']:.4f} m²",
                theme="bg-primary"
            ),

            ui.value_box(
                "Área Sección B",
                f"{r['area_B']:.4f} m²",
                theme="bg-info"
            ),

            ui.value_box(
                "Área Promedio",
                f"{r['area_promedio']:.4f} m²",
                theme="bg-success"
            ),

            ui.value_box(
                "Velocidad Media",
                f"{r['velocidad_media']:.3f} m/s",
                theme="bg-warning"
            ),

            ui.value_box(
                "Caudal",
                f"{r['caudal']:.3f} m³/s",
                theme="bg-danger"
            )

        )

    # ---------------------------------------------
    # PANEL BOOTSTRAP
    # ---------------------------------------------

    @output
    @render.ui
    def panel_bootstrap():

        e = estadisticas()

        return ui.layout_columns(

            ui.value_box(
                "Media Bootstrap",
                f"{e['media']:.4f} m³/s",
                theme="bg-success"
            ),

            ui.value_box(
                "Error estándar",
                f"{e['error']:.6f}",
                theme="bg-info"
            ),

            ui.value_box(
                "Sesgo",
                f"{e['sesgo']:.6f}",
                theme="bg-warning"
            ),

            ui.value_box(
                "IC 95%",
                f"{e['ic_inf']:.4f} - {e['ic_sup']:.4f}",
                theme="bg-primary"
            ),

            ui.value_box(
                "Valor p",
                f"{e['p']:.5f}",
                theme="bg-danger"
            )

        )


    @render.download(
        filename="Reporte_Bootstrap_Malacatos.pdf"
    )
    def descargar_pdf():

        from tempfile import NamedTemporaryFile

        r = resultados()

        e = estadisticas()

        if e['p'] >= 0.05:

            conclusion = (
                "La prueba de Shapiro-Wilk no rechaza la hipótesis de normalidad "
                "(p ≥ 0.05). La distribución Bootstrap puede considerarse "
                "aproximadamente normal y las estimaciones obtenidas son consistentes."
            )

        else:

            conclusion = (
                "La prueba de Shapiro-Wilk rechaza la hipótesis de normalidad "
                "(p < 0.05). Sin embargo, el histograma y el gráfico Q-Q muestran "
                "el comportamiento de la distribución Bootstrap, por lo que la "
                "estimación del caudal y de su incertidumbre sigue siendo válida."
            )

        archivo = NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        )

        r = resultados()

        e = estadisticas()

        generar_reporte_pdf(

            archivo.name,

            r['area_A'],

            r['area_B'],

            r['area_promedio'],

            r['tiempo'],

            r['velocidad_superficial'],

            r['velocidad_media'],

            r['caudal'],

            e['media'],

            e["sesgo"],

            e["error"],

            e["ic_inf"],

            e["ic_sup"],

            e["p"],

            int(input.n_boot()),

            conclusion

        )

        with open(archivo.name, "rb") as pdf:

            yield pdf.read()


    # ---------------------------------------------
    # CONCLUSIÓN AUTOMÁTICA
    # ---------------------------------------------

    @output
    @render.text
    def conclusion():

        estadistico, p = prueba_normalidad(
            caudales()
        )

        if p >= 0.05:

            conclusion = (
                "La prueba de Shapiro-Wilk no rechaza la hipótesis de normalidad "
                "(p ≥ 0.05). Esto indica que la distribución de los caudales obtenidos "
                "mediante Bootstrap puede considerarse aproximadamente normal. En "
                "consecuencia, la media, el error estándar y el intervalo de confianza "
                "constituyen estimaciones confiables de la incertidumbre asociada al "
                "caudal del río Malacatos."
            )

        else:

            conclusion = (
                "La prueba de Shapiro-Wilk rechaza la hipótesis de normalidad "
                "(p < 0.05), lo que indica que la distribución Bootstrap presenta "
                "desviaciones respecto a una distribución normal. Sin embargo, debido "
                "al elevado número de simulaciones realizadas, la estimación del caudal "
                "y de su incertidumbre continúa siendo estadísticamente válida. "
                "La interpretación de los resultados debe complementarse con el "
                "histograma y el gráfico Q-Q, los cuales permiten evaluar visualmente "
                "el comportamiento de la distribución de los caudales simulados."
            )

        return conclusion 

    # ---------------------------------------------
    # HISTOGRAMA
    # ---------------------------------------------

    @output
    @render.plot
    def histograma():

        datos = caudales()

        media = calcular_media(datos)

        desviacion = calcular_desviacion(datos)

        plt.figure(figsize=(8,5))

        plt.hist(
            datos,
            bins=30,
            density=True,
            edgecolor="black",
            label="Bootstrap"
        )

        x = np.linspace(
            min(datos),
            max(datos),
            200
        )

        from scipy.stats import norm

        y = norm.pdf(
            x,
            media,
            desviacion
        )

        plt.plot(
            x,
            y,
            linewidth=2,
            label="Distribución normal"
        )

        plt.title("Distribución Bootstrap del Caudal")

        plt.xlabel("Caudal (m³/s)")

        plt.ylabel("Densidad")

        plt.legend()

        plt.grid(True)

        plt.tight_layout()

        return plt.gcf()

    # ---------------------------------------------
    # GRÁFICO QQ
    # ---------------------------------------------

    @output
    @render.plot
    def qqplot():

        from scipy import stats

        plt.figure(figsize=(6,6))

        stats.probplot(
            caudales(),
            dist="norm",
            plot=plt
        )

        plt.title("Gráfico Q-Q")

        plt.grid(True)

        plt.tight_layout()

        return plt.gcf()

    # ---------------------------------------------
    # TABLA
    # ---------------------------------------------

    @output
    @render.table
    def tabla():

        datos = pd.DataFrame({

            "Simulacion": range(1, len(caudales())+1),

            "Caudal (m³/s)": [round(c,6) for c in caudales()]

        })

        return datos

    # ---------------------------------------------
    # DESCARGAR CSV
    # ---------------------------------------------

    @render.download(
        filename="simulaciones_bootstrap.csv"
    )
    def descargar_csv():

        datos = pd.DataFrame({

            "Simulacion": range(
                1,
                len(caudales())+1
            ),

            "Caudal (m³/s)": [
                round(c,6)
                for c in caudales()
            ]

        })

        yield datos.to_csv(index=False)


# =====================================================
# APLICACIÓN
# =====================================================

app = App(
    app_ui,
    server
)

