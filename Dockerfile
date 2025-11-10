# Imagen base
FROM python:3.11-slim

# Evita que Python guarde archivos .pyc
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Crea directorio de trabajo
WORKDIR /app

# Copia requirements y los instala
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copia todo el proyecto al contenedor
COPY . /app/

# Expone el puerto
EXPOSE 8000

# Comando por defecto (para desarrollo)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
