from sqlalchemy import Enum

# Define el Enum común para 'state', puse el Enum aquí para evitar escribir todo en cada modelo de la base de datos.
state_enum = Enum('pendiente', 'aprobado', 'rechazado', name='state_enum')
