# En los endpoints no debemos escribir consultas SQL directamente. Las consultas SQL deben estar
# en los modelos, donde se maneja la comunicación con la base de datos.
# En los rutas solo debemos manejar la lógica para recibir los datos,
# validarlos, y si es necesario, procesarlos antes de enviarlos a la base de datos.
# Los modelos son los encargados de realizar las consultas a la base de datos y devolver los resultados