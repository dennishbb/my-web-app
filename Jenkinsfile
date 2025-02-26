pipeline {
    agent any

    environment {
        FLASK_SERVER = "192.168.0.102"  // Your Flask server IP
        SSH_CREDENTIALS = "flask-server-ssh"  // Jenkins SSH Credentials ID
        APP_DIR = "/var/www/my-web-app"
    }

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/your-username/my-web-app.git'
            }
        }

        stage('Build') {
            steps {
                sh 'echo "Building Flask Application..."'
            }
        }

        stage('Deploy to Flask Server') {
            steps {
                script {
                    sshagent(credentials: [SSH_CREDENTIALS]) {
                        sh """
                        ssh -o StrictHostKeyChecking=no root@$FLASK_SERVER <<EOF
                        echo "Connecting to Flask server..."
                        cd $APP_DIR
                        
                        # Ensure a clean git pull
                        git reset --hard origin/main  # Discards local changes
                        git pull origin main  # Pull latest code

                        # Set correct permissions
                        sudo chown -R www-data:www-data $APP_DIR
                        sudo chmod -R 755 $APP_DIR

                        # Activate virtual environment and install dependencies
                        source venv/bin/activate
                        pip install -r requirements.txt

                        # Restart Gunicorn and Nginx
                        sudo systemctl restart flask_app
                        sudo systemctl restart nginx
                        
                        echo "Deployment completed!"
                        exit
                        EOF
                        """
                    }
                }
            }
        }
    }
}
