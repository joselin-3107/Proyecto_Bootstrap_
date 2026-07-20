"""
graficos.py

Funciones para generar los gráficos
del proyecto Bootstrap.
"""

import matplotlib.pyplot as plt

from scipy import stats

def histograma_bootstrap(caudales):
    """
    Genera un histograma de los caudales Bootstrap.
    """

    plt.figure(figsize=(8,5))

    plt.hist(
        caudales,
        bins=30,
        edgecolor="black"
    )

    plt.title("Distribución Bootstrap del Caudal")

    plt.xlabel("Caudal (m³/s)")

    plt.ylabel("Frecuencia")

    plt.grid(True)

    plt.tight_layout()

    plt.savefig("../Imagenes/histograma.png", dpi=300)

    plt.close()


def grafico_qq(caudales):
    """
    Genera un gráfico Q-Q para comprobar
    la normalidad de los caudales Bootstrap.
    """

    plt.figure(figsize=(6,6))

    stats.probplot(
        caudales,
        dist="norm",
        plot=plt
    )

    plt.title("Gráfico Q-Q")

    plt.grid(True)

    plt.tight_layout()

    plt.savefig("../Imagenes/qq_plot.png", dpi=300)

    plt.close()


def prueba_normalidad(caudales):
    """
    Realiza la prueba de normalidad
    de Shapiro-Wilk.
    """

    estadistico, p_valor = stats.shapiro(caudales)

    return estadistico, p_valor


