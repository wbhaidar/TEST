import pprint
import sys
import time
import logging
import pickle
from genie.testbed import load 


from genie.utils.diff import Diff
from genie.libs.ops.interface.ios.interface import Interface

from pyats.log.utils import banner


#from genie.utils import Dq

# Enable Logging
#logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s %(message)s')
logging.basicConfig(filename='/tmp/test_change_logging', level=logging.INFO, format='%(asctime)s %(message)s')
log = logging.getLogger(__name__)

############### TEST 1
log.info(banner("Loading TestBed Specification"))
print(banner("Loadng TestBed File"))
testbed = load('/taf/etc/2_4_testbed.yml')
print(banner("Successfully Loaded testbed '{}'\n".format(testbed.name)))
log.info(banner("\nPASS: Successfully loaded testbed '{}'\n".format(testbed.name)))


# Get the Device we are interested in
ios1 = testbed.devices['ios1']
ios1.connect(via='vty', log_stdout=False)

##f = open('/dev/null', 'w')
##sys.sterr = f

##ios1.connectionmgr.log.setLevel(logging.CRITICAL)
##ios1.log_user(enable=False)

##########################
########### INTERFACE COMPARE SECTION
print()
print()
print()
log.info(banner("Loading INTERFACE current state"))
print(banner("Loading INTERFACE current state"))
c_ios1_int = Interface(ios1)
c_ios1_int.learn()


filename1 = '/tmp/previous_ios1_interfaces'
infile1 = open(filename1, 'rb')
p_ios1_int = pickle.load(infile1)
#pprint.pprint(p_ios1_int.info)

log.info(banner("Comparing INTERFACE state to baseline"))
print(banner("Comparing INTERFACE state to baseline"))
diff1 = Diff(p_ios1_int.info, c_ios1_int.info, exclude=['accounting','counters', 'rate', 'maker'])
diff1.findDiff()

diff1_str = str(diff1)

if diff1_str:
    print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
    print('XXXX      DETECTED  STATE  CHANGE      XXXXX')
    print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
    print()
    print(diff1)
    log.info(banner("FAIL: INTERFACE STATE CHANGE DETECTED '{}'\n".format(testbed.name)))
    print(banner("FAIL: INTERFACE STATE CHANGE DETECTED '{}'\n".format(testbed.name)))
else:
    log.info(banner("PASS: NO INTERFACE STATE CHANGE DETECTED '{}'\n".format(testbed.name)))
    print(banner("PASS: NO INTERFACE STATE CHANGE DETECTED '{}'\n".format(testbed.name)))
infile1.close()

########## END OF INTERFACE COMPARE SECTION




######### OSPF COMPARE SECTION

filename2 = '/tmp/previous_ios1_ospf'
infile2 = open(filename2, 'rb')
p_ios1_ospf = pickle.load(infile2)

print()
print()
print()
log.info(banner("Loading OSPF current state "))
print(banner("Loading OSPF current state "))

c_ios1_ospf = ios1.learn('ospf')

log.info(banner("Comparing OSPF state to baseline"))
print(banner("Comparing OSPF state to baseline"))
ospf_diff1 = Diff(p_ios1_ospf.info, c_ios1_ospf.info, exclude=['dead_timer', 'checksum','area_scope_lsa_cksum_sum', 'spf_runs_count', 'cksum', 'hello_timer', 'seq_num', 'age'])
ospf_diff1.findDiff()
ospf_diff1_str = str(ospf_diff1)

if ospf_diff1_str:
    print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
    print('XXXX      DETECTED  STATE  CHANGE      XXXXX')
    print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
    print()
    print(ospf_diff1)
    print()
    print()
    log.info(banner("FAIL: OSPF CHANGE DETECTED '{}'\n".format(testbed.name)))
    print(banner("FAIL: OSPF CHANGE DETECTED '{}'\n".format(testbed.name)))
else:
    log.info(banner("PASS: NO OSPF CHANGE DETECTED '{}'\n".format(testbed.name)))
    print(banner("PASS: NO OSPF CHANGE DETECTED '{}'\n".format(testbed.name)))

infile2.close()






ios1.connect(log_stdout=False)

print()
print()
log.info(banner("Starting Connectivity Tests"))
print(banner("Starting Connectivity Tests"))

destinations = ['2.2.2.2', '10.0.0.2', '10.0.1.2', '10.0.1.2']
import re

#ios1.ping(addr='4.4.4.4')
all_up = True
for i in destinations:
    ios1_ping1 = ios1.execute('ping ip {} repeat 3 timeout 1'.format(i))
    match = re.search(r'Success rate is (\d+) percent', ios1_ping1)
    print('Ping {:20}  Success rate {}%'.format(i, match.group(1)))
    if int(match.group(1)) < 100:
        all_up = False

if all_up == True:
    log.info(banner("PASS: Connectivity Tests '{}'\n".format(testbed.name)))
    print(banner("PASS: Connectivity Tests '{}'\n".format(testbed.name)))
else:
    log.info(banner("FAIL: Connectivity Tests '{}'\n".format(testbed.name)))
    print(banner("FAIL: Connectivity Tests '{}'\n".format(testbed.name)))

