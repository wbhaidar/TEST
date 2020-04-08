# SDN Virtual Test Network

Objective To establish a virtual test platform that is representative of DCN (Data CEntre) and SNSL (firewall) environments that will be leveraged as a platform to conduct automated testing of changes for the UAT (Unsegmented Asset Treatment) migrations

The build pipeline is triggered upon a push or pull request to the main branch which effectively cycles through a Jenkins pipeline that does the following 
1. Build Stage 1 - Establish a GNS3 Topology on the Cloud Lab GNS3 VM. The GNS3 topology (nodes, node types, network links) are all defined in a YAML based file. An ansible playbook provisions the required topology by northbound API calls to the GNS3 server. Subsequent to the nodes being created an initial configuration is applied by telnet connection to the presented console port of the nodes. 
2. Baseline Test Stage 2 - This stage will run a python script that is based on PYATS modules that ‘learns’ the state of the network. Currently, this script learns the state of the interfaces and OSPF and performs a number of ping tests. The results are saved to a file. 
3. Deploy Proposed Changes Stage This stage will launch another ansible playbook that modifies the configuration on the GNS3 topology. 
4. Test change - Stage 4 This stage will re-run the python test script to learn the state of the network and compare the results with the previous state. Any differences are highlighted.

## Setup Instructions

### Pre Requisite GNS3 VM Server 
*  Install GNS3 VM Server. 
* Makwe sure that your GNS3 VM is using nested virtualisation (in VirtualBox: Settings / System / Processor -> Enable NEsted VT/AMD-V) - If your GUI doesn't allow you to set this, you can use the cli: vboxmanage modifyvm "GNS3 VM" --nested-hw-virt on - 
* Make sure your GNS3 VM's network interface has promiscuous mode enabled (in VirtualBox: Settings / Network / Advanced -> Allow All) - Import your images (e.g. IOS) into GNS3 - In GNS3 Console: File -> Import appliance - Point it at the foler containing your image files - you might need to download the startup_config image - to do so, click 'download'. - Update /stage1_and_3/gns3_build/inventory/gns3_vars.yml with IP location of GNS3 Server (stage1)

### Topology
- Update GNS3 Topology and Network Links in etc/1_gns3_vars.yml
- YAML Files
    - update etc/1_3_hosts with node characteristics IP details (stage1 & Stage 3)
    - update etc/2_4_testbed.yaml with IP and node details (stage 2 & 4)

### Build Docker Container

- Build the Test Automation Framework (TAF) container - This builds a container called "taf" that has python, ansible, and all the required modules. -  ./build.sh


## Run Instructions

### Run Scripts from mounted volume / Command Line

Note, run all "docker run" command from the root of the git repo, as the present working directory is passed through to the container, and mapped to /taf. e.g. cd /Users/whiteajo/Documents/GitHub/UAT-Automation/SDN_Test_Network_GNS3

    * Stage 1 (Lab setup) - docker run -ti --rm -v ${PWD}/taf:/taf -v ${PWD}/working:/tmp --workdir /taf/ taf ansible-playbook scripts/1_topology_setup.yml -i etc/1_3_hosts

    * Stage 2 (Baseline test) - docker run -ti --rm -v ${PWD}/taf:/taf -v ${PWD}/working:/tmp --workdir /taf/ taf python3 scripts/2_test_baseline_topology.py

    * Stage 3 (Apply Config change) - docker run -ti --rm -v ${PWD}/taf:/taf -v ${PWD}/working:/tmp --workdir /taf/ taf ansible-playbook scripts/3_topology_change_config.yml -i etc/1_3_hosts

    * Stage 4 (Post-changetest) - docker run -ti --rm -v ${PWD}/taf:/taf -v ${PWD}/working:/tmp --workdir /taf taf python3 scripts/4_test_changed_topology.py

    * Cleanup - docker run -ti --rm -v ${PWD}/taf:/taf --workdir /taf taf ansible-playbook scripts/10_topology_teardown.yml -i /taf/etc/1_3_hosts


### Run scripts embedded in container / Used for Jenkins
    * Stage 1 - docker run --rm -t taf ansible-playbook /taf/scripts/1_topology_setup.yml -i /gns3/etc/1_3_hosts

    * Stage 2 -  docker run --rm -t taf python3 /taf/scripts/2_test_baseline_topology.py

    * Stage 3 -  docker run --rm -t taf ansible-playbook /taf/scripts/3_topology_change_config.yml -i /gns3/etc/1_3_hosts

    * Stage 4 -  docker run --rm -t taf python3 /taf/scripts/4_test_changed_topology.py

    * Cleanup -  docker run --rm -t taf ansible-playbook /taf/scripts/10_topology_teardown.yml -i /taf/etc/1_3_hosts
