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
# logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(message)s')


logging.basicConfig(filename='test_baseline_logging', level=logging.INFO, format='%(asctime)s %(message)s')
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

#ios2 = testbed.devices['ios2']

# New Dict
intf={}

# Connect and run commands using Genie Parsers which will return a dictionary. Place output in a dictionary
#for device in [ios1, ios2]
#    device.connect(via = 'vty')
#    intf[device] = device.parse('show interfaces')


ios1.connect(via='vty')
#ios2.connect(via='vty')


############  INTERFACE STATE TO A FILE
print()
print()
print()
log.info(banner("Learning INTERFACE current state"))
print(banner("Learning INTERFACE current state"))
log.info(banner("Saving Interface State to a file"))

ios1_interface = Interface(ios1)
ios1_interface.learn()

filename = '/tmp/previous_ios1_interfaces'
outfile1 = open(filename, 'wb')

pickle.dump(ios1_interface, outfile1)
outfile1.close()
log.info(banner("\nPASS: Successfully saved Interface State'{}'\n".format(testbed.name)))
print(banner("\nPASS: Successfully saved Interface State'{}'\n".format(testbed.name)))
##############


######### OSPF STATE TO A FILE
print()
print()
print()
log.info(banner("Learning OSPF State from current Network"))
print(banner("Learning OSPF State from current Network"))
ios1_ospf = ios1.learn('ospf')

filename2 = '/tmp/previous_ios1_ospf'
outfile2 = open(filename2, 'wb')
pickle.dump(ios1_ospf, outfile2)
outfile2.close()

log.info(banner("\nPASS: Successfully saved OSPF State'{}'\n".format(testbed.name)))
print(banner("\nPASS: Successfully saved OSPF State'{}'\n".format(testbed.name)))
#########





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

