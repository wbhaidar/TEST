pipeline {
    agent {
        dockerfile {
            dir 'SDN_Test_Network_GNS3'
            args '-u root:root'
            args '-v taf:/taf'
            
        }
    }
    options {
          ansiColor('xterm')q
    }

    stages {
        stage ('Debug 1') {
            steps {
                sh 'printenv'
            }
        }
       stage('Build Topology') {   
                when { 
                    anyOf {
                        expression { env.BRANCH_NAME == 'testbranch' }
                        expression { env.BRANCH_NAME == 'createtopology'}
                    }
            }
           steps {
                sh 'ansible-playbook /taf/scripts/1_topology_setup.yml -i /taf/etc/1_3_hosts'
            }
        }
        stage('Test Baseline State') {
            when {
                expression { env.BRANCH_NAME == 'master' }
            }
            steps {
                sh 'python3 /taf/scripts/2_test_baseline_topology.py'
            }
        }
        stage('Deploy Proposed Config') {
            when {
                expression { env.BRANCH_NAME == 'testbranch' }
            }
            steps {
                sh ' ansible-playbook /taf/scripts/3_topology_change_config.yml -i /taf/etc/1_3_hosts'
            }
        }
        stage('Test Change') {
            when {
                expression { env.BRANCH_NAME == 'testbranch' }
            }        
            steps {
                sh 'python3 /taf/scripts/4_test_changed_topology.py'
            }
        }

         stage('Cleanup') {
            when {
                expression { env.BRANCH_NAME == 'cleanup' }
            }        
            steps {
                sh 'ansible-playbook /taf/scripts/10_topology_teardown.yml -i /taf/etc/1_3_hosts'
            }
        }
    }
         post {
            success {
                echo 'Yay. Success'
             }
             failure {
                echo 'Boohoo. We failed'
            }
        }
    
}
//                  You Can add the following in POST declaration
//                 mail to: "walid.haidar@cba.com.au", 
//                 subject:"SUCCESS: ${currentBuild.fullDisplayName}", 
//                 body: "Yay, we passed."