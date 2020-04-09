
### Run scripts embedded in container / Used for Jenkins
    * Stage 1 - docker run --rm -t taf ansible-playbook /taf/scripts/1_topology_setup.yml -i /gns3/etc/1_3_hosts

    * Stage 2 -  docker run --rm -t taf python3 /taf/scripts/2_test_baseline_topology.py

    * Stage 3 -  docker run --rm -t taf ansible-playbook /taf/scripts/3_topology_change_config.yml -i /gns3/etc/1_3_hosts

    * Stage 4 -  docker run --rm -t taf python3 /taf/scripts/4_test_changed_topology.py

    * Cleanup -  docker run --rm -t taf ansible-playbook /taf/scripts/10_topology_teardown.yml -i /taf/etc/1_3_hosts
