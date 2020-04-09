pipeline {
//     when {
//                branch '*/testbranch'
//    }
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
        stage ('Debug 1') {
            stesps {
                sh 'printenv'
            }
        }
//       stage('Build Topology') {   
//           steps {
//                sh 'ansible-playbook /taf/scripts/1_topology_setup.yml -i /taf/etc/1_3_hosts'
//            }
//        }


        stage('Test Baseline State') {
            steps {
                sh 'python3 /taf/scripts/2_test_baseline_topology.py'
            }
        }
        stage('Deploy Proposed Config') {
            steps {
                sh ' ansible-playbook /taf/scripts/3_topology_change_config.yml -i /taf/etc/1_3_hosts'
            }
        }
        stage('Test Change') {
            steps {
                sh 'python3 /taf/scripts/4_test_changed_topology.py'
            }
        }
    }
         post {
            success {
                 mail to: "wal_@hotmail.com", 
                 subject:"SUCCESS: ${currentBuild.fullDisplayName}", 
                 body: "Yay, we passed."
             }
             failure {
                 mail to: "wal_@hotmail.com", 
                 subject:"FAILURE: ${currentBuild.fullDisplayName}", 
                 body: "Boo, we failed."
            }
        }
    
}