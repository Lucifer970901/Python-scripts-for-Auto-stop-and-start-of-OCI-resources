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

# Staring Loops to execute AutoStop Script
 ################ ABD INSTANCES #########################################
print("     ####### Executing ADB AutoScaling Script #######")
adw = oci.database.DatabaseClient(config)
adw_df = adw.list_autonomous_databases(compartment_id,lifecycle_state='AVAILABLE' )
if len(adw_df.data)>0:
    print("         Number of Running ADB Instances: ",len(adw_df.data))
    for adwins in adw_df.data:
        if ('Prod' in adwins.freeform_tags and adwins.freeform_tags['Prod'] == 'yes'):
            cpu = int(adwins.freeform_tags['min_core_count'])
            #dbupdate = oci.database.models.UpdateDbSystemDetails()
            #dbupdate.cpu_core_count = 2
            adw.update_autonomous_database(adwins.id, oci.database.models.UpdateAutonomousDatabaseDetails(cpu_core_count=cpu))
            print("             Scaling ADB Instance",adwins.db_name)

        else:
            print("             Skipping ADB Instance",adwins.db_name)

else:
    print("         ####### NO ADB INSTANCES TO Scale #######")
print("     ####### Completed ADB AutoScale Script #######")
print("\n")
        ################ ABD INSTANCES #########################################
print("\n")
