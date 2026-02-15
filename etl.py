import pandas as pd
from sqlalchemy import create_engine
import urllib.parse 

# --- CONFIGURACIÓN ---
# 1. ORIGEN (NUBE - POSTGRESQL)
PG_HOST = 'mgg.vps.webdock.cloud'
PG_DB = 'dmc'
PG_USER = 'usr_ro_dmc_rrhh_estudiantes'
PG_PASS_RAW = 'fZp!jHt0j6%89^B4I*L*29bz4b^'
PG_PORT = '5432'

# 2. DESTINO (LOCAL - SQL SERVER)
SQL_SERVER = 'host.docker.internal'
SQL_DB = 'BD_DataOps'
SQL_USER = 'User_DataOps'
SQL_PASS = 'Sql_2026_Secure'

def run_etl():
    print("--- 🚀 INICIANDO ETL (VERSIÓN CORREGIDA) ---")
    
    try:
        # A. CONEXIÓN A POSTGRES
        print("[1/4] Conectando a Nube...")
        pg_pass_encoded = urllib.parse.quote_plus(PG_PASS_RAW)
        url_pg = f"postgresql+psycopg2://{PG_USER}:{pg_pass_encoded}@{PG_HOST}:{PG_PORT}/{PG_DB}"
        engine_pg = create_engine(url_pg)
        
        # Leer empleados
        query = "SELECT empleado_id, num_documento, nom_empleado, ape_empleado, mnt_salario FROM rrhh.Empleado"
        df_empleados = pd.read_sql(query, engine_pg)
        print(f"   ✅ {len(df_empleados)} empleados descargados.")

        # B. LECTURA CSV
        print("[2/4] Leyendo CSV local...")
        df_comisiones = pd.read_csv('ComisionEmpleados_V1_202602.csv', sep=';')
        
        # Renombramos la columna 'Comisión' para evitar problemas con la tilde
        df_comisiones.rename(columns={'Comisión': 'MontoComision'}, inplace=True)
        
        # C. TRANSFORMACIÓN (CRUCE POR ID)
        print("[3/4] Cruzando datos por ID de Empleado...")
        
        # JOIN usando 'empleado_id' que existe en ambos lados
        df_final = pd.merge(df_empleados, df_comisiones, on='empleado_id', how='inner')
        
        # Calcular Sueldo Total
        df_final['SueldoTotal'] = df_final['mnt_salario'] + df_final['MontoComision']
        
        # D. CARGA SQL SERVER
        print(f"[4/4] Guardando {len(df_final)} registros en SQL Server Local...")
        
        driver = 'ODBC Driver 17 for SQL Server'
        connection_string = f'DRIVER={{{driver}}};SERVER={SQL_SERVER};DATABASE={SQL_DB};UID={SQL_USER};PWD={SQL_PASS}'
        params = urllib.parse.quote_plus(connection_string)
        engine_sql = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")
        
        # Guardamos columnas limpias
        columnas_finales = ['empleado_id', 'nom_empleado', 'ape_empleado', 'num_documento', 'mnt_salario', 'MontoComision', 'SueldoTotal']
        df_final[columnas_finales].to_sql('ReportePagos_2026', engine_sql, if_exists='replace', index=False)
        
        print("🎉 ¡EXITO! Proceso terminado correctamente.")
        
    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    run_etl()