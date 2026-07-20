"""
Funciones para calcular el área y el caudal
"""

from datos import *

def calcular_delta_x():
    """
    Calcula la distancia entre cada punto de medición.
    """
    return B/n

def regla_trapecio(profundidades):
    """
    Calcula el área utilizando la Regla del Trapecio.
    """

    delta_x= calcular_delta_x()

    suma = profundidades[0]/2
    for profundidad in profundidades[1:-1]:
        suma += profundidad

    suma += profundidades[-1]/2

    area = delta_x * suma

    return area 

def calcular_tiempo_promedio(tiempos):
    """
    Calcula el tiempo promedio de los recorridos del flotador.
    """
    return sum(tiempos) / len(tiempos)

def calcular_velocidad_superficial(L, tiempo_promedio):
    """
    Calcula la velocidad superficial.
    """
    return L / tiempo_promedio

def calcular_velocidad_media(velocidad_superficial, k):
    """
    Calcula la velocidad media utilizando el factor de corrección.
    """
    return velocidad_superficial * k

def calcular_caudal(area, velocidad_media):
    """
    Calcula el caudal del río.
    """
    return area * velocidad_media