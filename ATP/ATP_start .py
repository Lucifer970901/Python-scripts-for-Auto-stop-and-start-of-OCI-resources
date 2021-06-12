import time
import oci
import os
import json
from pandas.io.json import json_normalize
import pandas as pd
from oci import config

# Tenancy & User details for Authentication ( Change as needed)
compartment_id = 'ocid1.tenancy.oc1..xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' # Tenancy & Root compartment OCID
userocid = '' # User OCID
home_region = 'us-ashburn-1' # Home Region
key_file = '/home/opc/Scripts/keys/oci_api_key.pem' # Prvate file for User Authentication
fingerprint = '' # Finger print of the public key added in user tokens

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
print("     ####### Executing ADB AutoStart Script #######")
adw = oci.database.DatabaseClient(config)
adw_df = adw.list_autonomous_databases(compartment_id,lifecycle_state='STOPPED' )
if len(adw_df.data)>0:
    print("         Number of Running ADB Instances: ",len(adw_df.data))
    for adwins in adw_df.data:
        if ('Dev' in adwins.freeform_tags and adwins.freeform_tags['Dev'] == 'Yes')or('Test' in adwins.freeform_tags and adwins.freeform_tags['Test'] == 'Yes'):
            adw.start_autonomous_database(adwins.id)
            print("             Starting ADB Instance",adwins.db_name)

        else:
            print("             Skipping ADB Instance",adwins.db_name)

else:
    print("         ####### NO ADB INSTANCES TO START #######")
print("     ####### Completed ADB AutoStart Script #######")
print("\n")
        ################ ABD INSTANCES #########################################
print("\n")
print(".........................................................................................................")
print("................................. The Program Ends Here  ................................................")
print(".........................................................................................................")
print("\n")
