"""
estadistica.py

Funciones para analizar estadísticamente
los resultados obtenidos mediante Bootstrap.
"""

import statistics

from scipy.stats import (
    skew,
    kurtosis,
    shapiro
)

def calcular_media(caudales):
    """
    Calcula la media de todos los caudales Bootstrap.
    """

    return statistics.mean(caudales)


def calcular_desviacion(caudales):
    """
    Calcula la desviación estándar de los caudales Bootstrap.
    """

    return statistics.stdev(caudales)


def calcular_intervalo_confianza(caudales):
    """
    Calcula el intervalo de confianza del 95 %.
    """

    caudales_ordenados = sorted(caudales)

    n = len(caudales)

    indice_inferior = int(0.025 * n)
    indice_superior = int(0.975 * n)

    limite_inferior = caudales_ordenados[indice_inferior]
    limite_superior = caudales_ordenados[indice_superior]

    return limite_inferior, limite_superior


def calcular_sesgo(caudales, caudal_original):
    """
    Calcula el sesgo (Bias) Bootstrap.
    """

    media_bootstrap = statistics.mean (caudales)

    return media_bootstrap - caudal_original


def calcular_asimetria(caudales):
    """
    Calcula la asimetría de la distribución Bootstrap.
    """

    return skew(caudales)


def calcular_curtosis(caudales):
    """
    Calcula la curtosis de la distribución Bootstrap.
    """

    return kurtosis(caudales)


def prueba_normalidad(caudales):
    """
    Realiza la prueba de Shapiro-Wilk.
    """

    estadistico, p_valor = shapiro(caudales)

    return estadistico, p_valor