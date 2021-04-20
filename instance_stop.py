import time
import oci
import os
import json
from pandas.io.json import json_normalize
import pandas as pd
from oci import config

# Tenancy & User details for Authentication ( Change as needed)
tenancy_id = 'ocid1.tenancy.oc1..aaaaaaaalylrk6bjiuxqryukd6jrlxgfbwjuulnavxqehvv3crknt7ewhlpa' # Tenancy & Root compartment OCID
compartment_id = 'ocid1.compartment.oc1..aaaaaaaaukottugsmj5vmneywbzvecjbg5pew2b7clgnm53zwyvgdutdiwvq' #  compartment OCID
userocid = 'ocid1.user.oc1..aaaaaaaaxtciqwuwtcvf37ef3oey5qunm27pns4gq2w56bxold73lstsmaeq' # User OCID
home_region = 'us-ashburn-1' # Home Region
key_file = 'C:/Users/megn/.oci/oci_api_key.pem' # Prvate file for User Authentication
fingerprint = '63:cd:da:65:17:8c:50:7e:b0:68:a4:f3:59:77:37:44' # Finger print of the public key added in user tokens

ex_comps = ['ManagedCompartmentForPaaS']
print("\n")
print(".........................................................................................................")
print("................................. The Program Starts Here................................................")
print(".........................................................................................................")
print("\n")
# Config for Home Region Connection
config = {
    "user": userocid,
    "key_file": key_file,
    "fingerprint": fingerprint,
    "tenancy": tenancy_id,
    "region": home_region,
    "compartment_id": compartment_id }

# Creating connection to Tenancy
identity = oci.identity.IdentityClient(config)

# Staring Loops to execute Autostart Script
 ################ ABD INSTANCES #########################################
print("     ####### Executing Instance AutoStop Script #######")
instance = oci.core.ComputeClient(config)
instance_df = instance.list_instances(compartment_id,lifecycle_state='RUNNING')
if len(instance_df.data)>0:
    print("         Number of Running Compute Instances: ",len(instance_df.data))
    for instanceins in instance_df.data:
        if ('Dev' in instanceins.freeform_tags and instanceins.freeform_tags['Dev'] == 'Yes')or('Test' in instanceins.freeform_tags and instanceins.freeform_tags['Test'] == 'Yes'):
            instance.instance_action(instanceins.id, action = 'SOFTSTOP')
            print("             Stopping Compute Instance: ",instanceins.display_name)
        else:
            print("             Skipping Compute Instance",instanceins.display_name)

else:
    print("         ####### NO Compute INSTANCES TO STOP #######")
print("     ####### Completed Compute AutoStop Script #######")
print("\n")
        ################ ABD INSTANCES #########################################
print("\n")
instance_df = instance.list_instances(compartment_id)
print("list of compute instances with their status:")
for instanceins in instance_df.data:
    print (instanceins.display_name, ' : ',instanceins.lifecycle_state)

#for instanceins in instance1_df.data:
#    print (instanceins.display_name, ':',instanceins.lifecycle_state)
print(".........................................................................................................")
print("................................. The Program Ends Here  ................................................")
print(".........................................................................................................")
print("\n")
