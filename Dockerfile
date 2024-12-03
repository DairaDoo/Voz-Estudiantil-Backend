# Usa una imagen base de Python
FROM python:3.9-slim

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia los archivos del proyecto a la imagen del contenedor
COPY . /app

# Instala las dependencias necesarias
RUN pip install --no-cache-dir -r requirements.txt

# Establece variables de entorno necesarias
ENV FLASK_APP=run.py
ENV FLASK_ENV=development

# Expone el puerto 5000 (por defecto de Flask)
EXPOSE 5000

# Ejecuta la aplicación Flask
CMD ["flask", "run", "--host=0.0.0.0"]
