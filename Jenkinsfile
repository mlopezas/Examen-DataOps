pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
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
                // Ejecutamos y nos aseguramos de que el contenedor genere el archivo
                sh 'docker run --name contenedor-etl --add-host=host.docker.internal:host-gateway imagen-dataops:latest'
            }
        }
    }
    
    // SOLO UN BLOQUE POST PARA TODO
    post {
        success {
            echo '🚀 ¡DataOps completado con éxito!'
            // Esto cumple con el punto 4: Generar el artefacto (Excel)
            // Asegúrate de que tu script de Python genere un archivo .xlsx
            archiveArtifacts artifacts: '*.xlsx', allowEmptyArchive: true, fingerprint: true
        }
        failure {
            echo '❌ Hubo un error en el pipeline.'
        }
    }
}