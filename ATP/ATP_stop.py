import time
import oci
import os
import json
from pandas.io.json import json_normalize
import pandas as pd
from oci import config

# Tenancy & User details for Authentication ( Change as needed)
tenancy_id = 'ocid1.tenancy.oc1..aaaaxxxxxxxxxxxxxxxxxxxxxrlxgfbwjuulnavxqehvv3crknt7ewhlpa' # Tenancy & Root compartment OCID
compartment_id = 'ocid1.compartment.ocxxxxxxxxxxxxxxxxxxxxmneywbzvecjbg5pew2b7clgnm53zwyvgdutdiwvq' #  compartment OCID
userocid = 'ocid1.user.oc1..aaaaaaaaxtciqxxxxxxxxxxxxxxxxxxxxxxxgq2w56bxold73lstsmaeq' # User OCID
home_region = 'us-ashburn-1' # Home Region
key_file = '<path key file>' # Prvate file for User Authentication
fingerprint = '63:cd:da:65:17xxxxxxxxxxxxxxxxx4:f3:59:77:37:44' # Finger print of the public key added in user tokens

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

# Staring Loops to execute AutoStop Script
 ################ ABD INSTANCES #########################################
print("     ####### Executing ADB AutoStop Script #######")
adw = oci.database.DatabaseClient(config)
adw_df = adw.list_autonomous_databases(compartment_id,lifecycle_state='AVAILABLE' )
if len(adw_df.data)>0:
    print("         Number of Running ADB Instances: ",len(adw_df.data))
    for adwins in adw_df.data:
        if ('Dev' in adwins.freeform_tags and adwins.freeform_tags['Dev'] == 'Yes')or('Test' in adwins.freeform_tags and adwins.freeform_tags['Test'] == 'Yes'):
            adw.stop_autonomous_database(adwins.id)
            print("             Stoping ADB Instance",adwins.db_name)

        else:
            print("             Skipping ADB Instance",adwins.db_name)

else:
    print("         ####### NO ADB INSTANCES TO Stop #######")
print("     ####### Completed ADB AutoStop Script #######")
print("\n")
        ################ ABD INSTANCES #########################################
print("\n")
print(".........................................................................................................")
print("................................. The Program Ends Here  ................................................")
print(".........................................................................................................")
print("\n")
