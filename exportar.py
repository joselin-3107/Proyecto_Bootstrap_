"""
exportar.py

Funciones para guardar resultados del proyecto.
"""

import pandas as pd


def guardar_csv(caudales, nombre_archivo):

    datos = pd.DataFrame({
        "Simulación": range(1, len(caudales)+1),
        "Caudal (m³/s)": caudales
    })

    datos.to_csv(
        nombre_archivo,
        index=False,
        encoding="utf-8"
    )

    print(f"\nArchivo '{nombre_archivo}' creado correctamente.")