pipeline {
  agent any
  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }
    stage('Install') {
      steps {
        sh 'python -m pip install --upgrade pip'
        sh 'pip install -r requirements.txt'
      }
    }
    stage('Lint') {
      steps {
        sh 'pip install flake8'
        sh 'flake8 .'
      }
    }
    stage('Test') {
      steps {
        sh 'pytest --cov=app --cov-fail-under=80'
      }
    }
    stage('Docker Build') {
      steps {
        sh 'docker build -t aceest-gym:jenkins .'
      }
    }
    stage('Docker Run smoke test') {
      steps {
        sh 'docker run -d --name aceest-smoke -p 5002:5000 aceest-gym:jenkins'
        sh 'sleep 5'
        sh 'curl -f http://localhost:5002/'
        sh 'docker stop aceest-smoke && docker rm aceest-smoke'
      }
    }
  }
  post {
    always {
      junit '**/test-results.xml'
    }
    failure {
      mail to: 'team@aceest.com', subject: "Jenkins: Build failed", body: "Build ${env.BUILD_URL} failed"
    }
  }
}
