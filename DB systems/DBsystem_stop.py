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

# Staring Loops to execute Autostart Script
 ################ ABD INSTANCES #########################################
print("     ####### Executing DB System AutoStop Script #######")

db_client = oci.database.DatabaseClient(config)

db_systems = db_client.list_db_systems(compartment_id).data

if len(db_systems)>0:
    for db_system in db_systems:
        #print("The DB System Name is:",db_system.display_name)
        #print(db_system)
        if ('Dev' in db_system.freeform_tags and db_system.freeform_tags['Dev'] == 'Yes')or('Test' in db_system.freeform_tags and db_system.freeform_tags['Test'] == 'Yes'):
            db_nodes = db_client.list_db_nodes(compartment_id,db_system_id=db_system.id,lifecycle_state='AVAILABLE').data
            if len(db_nodes)>0:
                for db_node in db_nodes:
                    #print(db_node)
                    #print(db_node.id)
                    print("The DB System Name is:",db_system.display_name )
                    print("     Stopping the Node:",db_node.hostname)
                    db_client.db_node_action(db_node.id,'STOP')
                    print("\n")
            else:
                print("No nodes running in DB System:",db_system.display_name)
                print("\n")
        else:
            print("Skipping the DB System:",db_system.display_name )
            print("\n")
else:
    print("No DB systems available in compartment")
    print("     ####### Completed DB System AutoStop Script #######")
    print("\n")
        ################ DB SYSTEMS  ###########################################
print("\n")
'''
db_system = db_client.list_db_systems(compartment_id)
print("list of DB systems with their status:")
for instanceins in db_system.data:
    print (db_system.display_name, ' : ',db_system.lifecycle_state)
'''
print(".........................................................................................................")
print("................................. The Program Ends Here  ................................................")
print(".........................................................................................................")
print("\n")
