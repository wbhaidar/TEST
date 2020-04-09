pipeline {
    agent {
        dockerfile {
            dir 'SDN_Test_Network_GNS3'
            args '-u root:root'
        }
    }
    options {
          ansiColor('xterm')
    }

    stages {
        stage ('intiial') {
            steps {
                sh 'whoami'
            }
        }
        stage ('initial2') {
            steps {
                sh ' ls -al /'
            }
        }
        stage('build gns3') {
            steps {
                sh 'ansible-playbook /taf/scripts/1_topology_setup.yml -i /taf/etc/1_3_hosts'
            }
        }
        post {
            success {
                echo 'Success'
            }
            failure {
                echo 'failed'
            }
        }
    }
}