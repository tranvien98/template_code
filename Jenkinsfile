pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials') // Replace with your Jenkins credentials ID for Docker Hub
        DOCKER_IMAGE = 'viendev9z/fastapi-templates'     // Replace with your Docker Hub repository
    }

    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    def buildTag = "${DOCKER_IMAGE}:0.${env.BUILD_NUMBER}"
                    sh "docker build -t ${buildTag} ."
                    env.IMAGE_TAG = buildTag // Pass the tag to subsequent stages
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', DOCKERHUB_CREDENTIALS) {
                        sh "docker push ${env.IMAGE_TAG}"
                    }
                }
            }
        }

        stage('Deploy with Docker Compose') {
            steps {
                script {
                    sh """
                    export IMAGE_TAG=${env.IMAGE_TAG}
                    docker-compose -f docker-compose.yml down
                    docker-compose -f docker-compose.yml up -d
                    """
                }
            }
        }
    }

    post {
        success {
            echo 'Build and deployment successful!'
        }
        failure {
            echo 'Build or deployment failed!'
        }
    }
}
