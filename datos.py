"""
PROYECTO BOOTSTRAP
Estimación de la incertidumbre del caudal del río Malacatos
Universidad Nacional de Loja
Ingeniería Ambiental
"""

#================================================
# DATOS GENERALES DEL PROYECTO
#================================================

# Ancho del río (m)
B=5.60 

# Número de intervalos
n=7

# Longitud del tramo (m)
L=8.55

# Factor de corrección adoptado 
k=0.80

#================================================
# PROFUNDIDADES
#================================================

# Sección A (m)
profundidades_A=[
    0.20,
    0.18,
    0.53,
    0.30,
    0.105,
    0.21,
    0.25,
    0.09
]

# Sección B
profundidades_B=[
    0.191,
    0.463,
    0.55,
    0.33,
    0.22,
    0.15,
    0.15,
    0.09
]

#================================================
# TIEMPOS DEL FLOTADOR (s)
#================================================

tiempos=[
    5.58,
    5.67,
    5.61,
    5.64,
    5.58
]
