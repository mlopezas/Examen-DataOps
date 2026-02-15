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
                // Modificado: Agregamos el volumen -v para mapear tu carpeta local
                // Nota: Usamos barras / para la ruta de Windows en Docker
                sh '''
                    docker run --name contenedor-etl \
                    --add-host=host.docker.internal:host-gateway \
                    -v "C:/Users/Maikol_Lopez/Desktop/Examen_DataOps:/app/output" \
                    imagen-dataops:latest
                '''
            }
        }
    }
    
    post {
        success {
            echo '🚀 ¡DataOps completado con éxito! El Excel debería estar en tu carpeta local.'
            // Buscamos el excel en la carpeta output para mostrarlo en Jenkins también
            archiveArtifacts artifacts: '*.xlsx', allowEmptyArchive: true, fingerprint: true
        }
        failure {
            echo '❌ Hubo un error en el pipeline.'
        }
    }
}