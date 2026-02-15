# CAMBIO IMPORTANTE: Usamos 'bullseye' (Debian 11) en lugar de 'buster'
FROM python:3.9-slim-bullseye

WORKDIR /app

# 1. Instalar herramientas básicas y dependencias del sistema
# Usamos una sola línea para evitar errores de capa
RUN apt-get update && apt-get install -y --no-install-recommends \
    gnupg2 \
    curl \
    ca-certificates \
    apt-transport-https \
    unixodbc-dev \
    libpq-dev

# 2. Agregar las llaves de Microsoft (Específicas para Debian 11)
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list

# 3. Actualizar repositorios e instalar el Driver ODBC 17
RUN apt-get update
RUN ACCEPT_EULA=Y apt-get install -y msodbcsql17

# 4. Copiar archivos y dependencias
COPY . .
# Instalamos librerías Python (Pandas, SQLAlchemy, etc.) directo
RUN pip install pandas sqlalchemy pyodbc psycopg2-binary

# 5. Ejecutar script
CMD ["python", "etl.py"]