import time
import oci
import os
import json
from pandas.io.json import json_normalize
import pandas as pd
from oci import config

#import config as cfg
tenancy_id = 'ocid1.tenancy.oc1..aaaaxxxxxxxxxxxxxxxxxxxxxrlxgfbwjuulnavxqehvv3crknt7ewhlpa' # Tenancy & Root compartment OCID
compartment_id = 'ocid1.compartment.ocxxxxxxxxxxxxxxxxxxxxmneywbzvecjbg5pew2b7clgnm53zwyvgdutdiwvq' #  compartment OCID
userocid = 'ocid1.user.oc1..aaaaaaaaxtciqxxxxxxxxxxxxxxxxxxxxxxxgq2w56bxold73lstsmaeq' # User OCID
home_region = 'us-ashburn-1' # Home Region
key_file = '<path key file>' # Prvate file for User Authentication
fingerprint = '63:cd:da:65:17xxxxxxxxxxxxxxxxx4:f3:59:77:37:44' # Finger print of the public key added in user tokens
# Config for Home Region Connection
config = {
    "user": userocid,
    "key_file": key_file,
    "fingerprint": fingerprint,
    "tenancy": tenancy_id,
    "region": home_region,
    "compartment_id": compartment_id }



compartment_id = config["tenancy"]
print("\n")
print(".........................................................................................................")
print("................................. The Program Starts Here................................................")
print(".........................................................................................................")
print("\n")


# Creating connection to Tenancy
identity = oci.identity.IdentityClient(config)

# Staring Loops to execute Autostart Script
 ################ ABD INSTANCES #########################################
print("     ####### Executing Instance AutoStart Script #######")
instance = oci.core.ComputeClient(config)
instance_df = instance.list_instances(compartment_id,lifecycle_state='STOPPED' )
if len(instance_df.data)>0:
    print("         Number of stopped Compute Instances: ",len(instance_df.data))
    for instanceins in instance_df.data:
        if ('Dev' in instanceins.freeform_tags and instanceins.freeform_tags['Dev'] == 'Yes')or('Test' in instanceins.freeform_tags and instanceins.freeform_tags['Test'] == 'Yes'):
            instance.instance_action(instanceins.id,action = 'START')
            print("             Starting Compute Instance",instanceins.display_name)
            #print ("list all the running instances:\n",instance.list_instances(compartment_id,lifecycle_state='RUNNING' ))
        else:
            print("             Skipping Compute Instance",instanceins.display_name)

else:
    print("         ####### NO Compute INSTANCES TO START #######")
print("     ####### Completed Compute AutoStart Script #######")
print("\n")
        ################ Compute INSTANCES #########################################
print("\n")
instance_df = instance.list_instances(compartment_id)
print("list of compute instances with their status:")
for instanceins in instance_df.data:
    print (instanceins.display_name, ' : ',instanceins.lifecycle_state)
#print ("list all the running instances:\n",instance.list_instances(compartment_id,lifecycle_state='RUNNING' )and(('Dev' in instanceins.freeform_tags and instanceins.freeform_tags['Dev'] == 'Yes')or('Test' in instanceins.freeform_tags and instanceins.freeform_tags['Test'] == 'Yes')))
print(".........................................................................................................")
print("................................. The Program Ends Here  ................................................")
print(".........................................................................................................")
print("\n")
