pipeline {
    agent any

    environment {
        FLASK_SERVER = "192.168.0.102"  // Your Flask Server IP
        SSH_CREDENTIALS = "flask-server-ssh"  // Jenkins SSH Credentials ID
        APP_DIR = "/var/www/my-web-app"
    }

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/dennishbb/my-web-app.git'
            }
        }

        stage('Build') {
            steps {
                sh 'echo "Building Flask Application..."'
            }
        }

        stage('Deploy to Flask Server') {
            steps {
                sshagent(['flask-server-ssh']) {
                    sh """
                    ssh -o StrictHostKeyChecking=no root@$FLASK_SERVER <<EOF
                    cd $APP_DIR
                    git pull origin main
                    source venv/bin/activate
                    pip install -r requirements.txt
                    sudo systemctl restart flask_app
                    exit
                    EOF
                    """
                }
            }
        }
    }
}
