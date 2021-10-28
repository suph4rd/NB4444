
pipeline {
    agent {
        label 'test_Develop'
        }
    stages {
        stage("Build") {
            steps {
                sh 'docker-compose -f docker-compose-test.yml up --build'
            }
        }
    }
}