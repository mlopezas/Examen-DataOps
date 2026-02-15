# CAMBIO IMPORTANTE: Usamos 'bullseye' (Debian 11) en lugar de 'buster'
FROM python:3.9-slim-bullseye

WORKDIR /app

# 1. Instalar herramientas básicas y dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    gnupg2 \
    curl \
    ca-certificates \
    apt-transport-https \
    unixodbc-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 2. Agregar las llaves de Microsoft (Específicas para Debian 11)
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list

# 3. Actualizar repositorios e instalar el Driver ODBC 17
RUN apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql17

# 4. Crear carpeta para el Excel (Donde se mapeará tu carpeta de Windows)
RUN mkdir -p /app/output

# 5. Copiar archivos
COPY . .

# 6. Instalamos librerías Python (Agregamos openpyxl para el Excel)
RUN pip install --no-cache-dir pandas sqlalchemy pyodbc psycopg2-binary openpyxl

# 7. Ejecutar script (Asegúrate de que tu archivo se llame etl.py)
CMD ["python", "etl.py"]