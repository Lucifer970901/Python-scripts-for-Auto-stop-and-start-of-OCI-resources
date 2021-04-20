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
#ocid_id = 'ocid1.mysqldbsystem.oc1.iad.aaaaaaaa4vvwcfw5ptioqinzjprxn2heqmo6n4c2sq7qqb3ohcl7vwefmc7a'
# Staring Loops to execute Autostart Script
 ################ DB system #########################################
print("     ####### Executing DB System AutoStop Script #######")
db_client = oci.mysql.DbSystemClient(config)

#mysqldb = db_client.get_db_system(ocid_id).data
#print(mysqldb)
#db_client.start_db_system(ocid_id)
db_systems = db_client.list_db_systems(compartment_id,lifecycle_state='ACTIVE').data #
if len(db_systems)>0:
    for db_system in db_systems:
        mysqldb = db_client.list_db_systems(compartment_id)
        #print("The DB System Name is:",db_system.display_name)
        #print(db_system)
        if ('Dev' in db_system.freeform_tags and db_system.freeform_tags['Dev'] == 'Yes')or('Test' in db_system.freeform_tags and db_system.freeform_tags['Test'] == 'Yes'):
            if len(mysqldb.data)>0:
                for db in mysqldb.data:
                    print("The DB System Name is:",db.display_name )
                    db_client.stop_db_system(db.id,stop_db_system_details=oci.mysql.models.StopDbSystemDetails(
        shutdown_type="SLOW"))
                    print("\n")
            else:
                print("No Databases stopped in compartment:",db_system.display_name)
                print("\n")
        else:
            print("Skipping the DB System:",db_system.display_name )
            print("\n")

else:
    print("No DB systems running in compartment")
    print("     ####### Completed DB System AutoStop Script #######")
    print("\n")

       ################ DB SYSTEMS  ###########################################
print("\n life cycle state of the DB systems in the compartment")
db_systems = db_client.list_db_systems(compartment_id)
for db in db_systems.data:
    print (db.display_name, ' : ',db.lifecycle_state)
print(".........................................................................................................")
print("................................. The Program Ends Here  ................................................")
print(".........................................................................................................")
print("\n")
