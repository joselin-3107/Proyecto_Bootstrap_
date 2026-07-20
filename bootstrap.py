"""
bootstrap.py

Funciones para aplicar el método Bootstrap
al cálculo del caudal.
"""

import random


def generar_muestra_bootstrap(datos):
    """
    Genera una muestra Bootstrap utilizando
    muestreo con reemplazo.
    """

    muestra = random.choices(
        datos,
        k=len(datos)
    )

    return muestra


def simulacion_bootstrap(
    tiempos,
    area,
    longitud,
    factor,
    numero_simulaciones
):
    """
    Ejecuta varias simulaciones Bootstrap
    y devuelve una lista con todos los caudales.
    """

    from integracion import (
        calcular_tiempo_promedio,
        calcular_velocidad_superficial,
        calcular_velocidad_media,
        calcular_caudal
    )

    lista_caudales = []

    for i in range(numero_simulaciones):

        muestra = generar_muestra_bootstrap(tiempos)

        tiempo = calcular_tiempo_promedio(muestra)

        velocidad_superficial = calcular_velocidad_superficial(
            longitud,
            tiempo
        )

        velocidad_media = calcular_velocidad_media(
            velocidad_superficial,
            factor
        )

        caudal = calcular_caudal(
            area,
            velocidad_media
        )

        lista_caudales.append(caudal)

    return lista_caudales

