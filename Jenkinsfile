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
        sh 'python3 -m pip install --upgrade pip'
        sh 'python3 -m pip install -r requirements.txt'
      }
    }

    stage('Lint') {
      steps {
        sh 'python3 -m flake8 app.py tests'
      }
    }

    stage('Test') {
      steps {
        sh 'python3 -m pytest --cov=app --cov-fail-under=80 --junitxml=test-results.xml'
      }
    }

    stage('Docker Test') {
      steps {
        sh 'docker build --target test -t aceest-gym:test .'
        sh 'docker run --rm aceest-gym:test'
      }
    }

    stage('Docker Runtime Build') {
      steps {
        sh 'docker build --target runtime -t aceest-gym:jenkins .'
      }
    }

    stage('Docker Run Smoke Test') {
      steps {
        sh 'docker run -d --name aceest-smoke -p 5002:5000 aceest-gym:jenkins'
        sh 'sleep 5'
        sh 'curl -f http://localhost:5002/'
      }
    }
  }

  post {
    always {
      junit 'test-results.xml'
      sh 'docker rm -f aceest-smoke || true'
    }
  }
}
