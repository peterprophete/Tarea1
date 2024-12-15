pipeline {
    agent any

    stages {
        stage('Perform Preparation') {
            steps {
                script {
                    echo "Get Code"
                    sh '''
                        git clone https://github.com/manulis/unir-cp1.git
                        ls
                    '''
                }
            }
        }
        stage('Build') {
            steps {
                echo 'This is python no build needed'
                echo "ls -la unir-cp1"
            }
        }
        stage('Tests') {
            parallel {
                stage('Unit') {
                    steps {
                        catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                            sh '''
                                set -e
                                cd unir-cp1
                                if [ ! -d "test/unit" ]; then
                                    echo "Directory test/unit does not exist"
                                    exit 1
                                fi
                                export PYTHONPATH=.
                                pytest --junitxml=result-unit.xml test/unit
                            '''
                        }
                    }
                }
                stage('Rest') {
                    steps {
                        catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                            sh '''
                                set -e
                                cd unir-cp1
                                if [ ! -d "test/unit" ]; then
                                    echo "Directory test/unit does not exist"
                                    exit 1
                                fi
                                
                                # Verificar si el puerto 9090 está en uso y esperar a que esté libre
                                while lsof -i:9090 > /dev/null; do
                                    echo "Esperando a que el puerto 9090 esté libre..."
                                    sleep 2
                                done
                                
                                # Iniciar Flask y WireMock
                                export FLASK_APP=app/api.py
                                flask run &
                                java -jar /usr/local/bin/wiremock.jar --port 9090 --verbose --root-dir test/wiremock &
                                
                                # Esperar a que WireMock esté listo
                                until curl --silent --max-time 10 http://localhost:9090 > /dev/null; do
                                    echo "Esperando a que WireMock esté listo..."
                                    sleep 2
                                done
                                
                                echo "WireMock está listo, comenzando las pruebas"
                                pytest --junitxml=result-rest.xml test/rest
                            '''
                        }
                    }
                }
            }
        }
        stage('Result') {
            steps {
                junit "result*.xml"
            }
        }
    }

    post {
        always {
            echo "Cleaning workspace"
            deleteDir()
        }
    }
}
