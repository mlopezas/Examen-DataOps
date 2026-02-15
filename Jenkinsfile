pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                // Descarga el código de GitHub
                checkout scm 
            }
        }
        stage('Limpieza') {
            steps {
                sh 'docker rm -f contenedor-etl || true'
            }
        }
        stage('Construir Imagen') {
            steps {
                sh 'docker build -t imagen-dataops:latest .'
            }
        }
        stage('Ejecutar ETL') {
            steps {
                // Conexión al host de Windows para llegar al SQL Server
                sh 'docker run --name contenedor-etl --add-host=host.docker.internal:host-gateway imagen-dataops:latest'
            }
        }
    }
    post {
        success {
            echo '🚀 ¡DataOps completado con éxito!'
        }
    }
}