import time
import cx_Oracle
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
key_file = '~/.oci/oci_api_key.pem' # Prvate file for User Authentication
fingerprint = '09:fd:0f:58:f5:d3:d0:c4:7d:f8:6a:a6:de:19:c2:fd' # Finger print of the public key added in user tokens

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
#ocid_id = 'ocid1.mysqldbsystem.oc1.iad.aaaaaaaa4vvwcfw5ptioqinzjprxn2heqmo6n4c2sq7qqb3ohcl7vwefmc7a'
# Staring Loops to execute Autostart Script
 ################ DB system #########################################
print("     ####### Executing DB System AutoStart Script #######")
db_client = oci.database.DatabaseClient(config)
db_systems = db_client.list_db_systems(compartment_id,lifecycle_state='AVAILABLE').data
if len(db_systems)>0:
    for db_system in db_systems:
        #print("The DB System Name is:",db_system.display_name)
        #print(db_system)

        if ('Dev' in db_system.freeform_tags and db_system.freeform_tags['Dev'] == 'Yes')or('Test' in db_system.freeform_tags and db_system.freeform_tags['Test'] == 'Yes'):
            db_nodes = db_client.list_db_nodes(compartment_id,db_system_id=db_system.id,lifecycle_state='STOPPED').data
            if len(db_nodes)>0:
                for db_node in db_nodes:
                    #print(db_node)
                    #print(db_node.id)
                    print("The DB System Name is:",db_system.display_name )
                    print("     Starting the Node:",db_node.hostname)
                    db_client.db_node_action(db_node.id,'START')
                    print("\n")
            else:
                print("No nodes stopped in DB System:",db_system.display_name)
                print("\n")
        else:
            print("Skipping the DB System:",db_system.display_name )
            print("\n")

else:
    print("No DB systems stopped in compartment")
    print("     ####### Completed DB System AutoStart Script #######")
    print("\n")
        ################ DB SYSTEMS  ###########################################
print("\n")

time.sleep (240)

for i in range(0,1):
    while True:
        try:
            #create connection
            conn = cx_Oracle.connect(user="scott", password= "WelCome##123", dsn="129.213.146.152/vmdb.publicsubnet.dockerk8svcn.oraclevcn.com")
            print(conn.version)
            print ("connection successful")
            conn.close()
            break
        except:
            continue
        break
   # print ("oops! connection unsuccessful") 



# Staring Loops to execute Autostart Script
 ################ ABD INSTANCES #########################################
print("     ####### Executing Instance AutoStart Script #######")
instance = oci.core.ComputeClient(config)
instance_df = instance.list_instances(compartment_id,lifecycle_state='STOPPED')
if len(instance_df.data)>0:
    print("         Number of Running Compute Instances: ",len(instance_df.data))
    for instanceins in instance_df.data:
        if ('Dev' in instanceins.freeform_tags and instanceins.freeform_tags['Dev'] == 'Yes')or('Test' in instanceins.freeform_tags and instanceins.freeform_tags['Test'] == 'Yes'):
            instance.instance_action(instanceins.id, action = 'START')
            print("             Startng Compute Instance: ",instanceins.display_name)
        else:
            print("             Skipping Compute Instance",instanceins.display_name)

else:
    print("         ####### NO Compute INSTANCES TO STOP #######")
print("     ####### Completed Compute AutoStart Script #######")
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