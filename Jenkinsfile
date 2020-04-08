pipeline {
    agent {
        dockerfile {
            dir 'SDN_Test_Network_GNS3'
        }
    }
    options {
          ansiColor('xterm')
    }

    stages {
        stage('build gns3') {
            steps {
                sh 'ansible-playbook /taf/scripts/1_topology_setup.yml -i /gns3/etc/1_3_hosts'
            }
        }
    }
}