import time
import oci
import os
import json
from pandas.io.json import json_normalize
import pandas as pd
from oci import config

# Tenancy & User details for Authentication ( Change as needed)
compartment_id = 'ocid1.tenancy.oc1..aaaaaaaaltyukd6jrlxgfbwjuulnavxqehvv3crknt7ewhlpa' # Tenancy & Root compartment OCID
userocid = 'ocid1.user.oc1..aaaaaaaaxtciqwuwtey5qunm27pns4gq2w56bxold73lstsmaeq' # User OCID
home_region = 'us-ashburn-1' # Home Region
key_file = '/home/opc/oci_api_key.pem' # Prvate file for User Authentication
fingerprint = '63:cd:da:68:a4:f3:59:77:37:44' # Finger print of the public key added in user tokens

# Compartments to Exclude
ex_comps = ['admincompartment']
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
    "tenancy": compartment_id,
    "region": home_region,
    "compartment_id": compartment_id }

# Creating connection to Tenancy
identity = oci.identity.IdentityClient(config)

# Gathering Compartments
base_comps = []
all_comps = []
first_level_comps = oci.pagination.list_call_get_all_results(identity.list_compartments,compartment_id)
for c in first_level_comps.data:
    if (c.name not in ex_comps and c.lifecycle_state=='ACTIVE'):
        base_comps.append(c)
root = identity.get_compartment(compartment_id)
all_comps.append(root.data)
all_comps.extend(base_comps)
while len(base_comps) > 0:
    target = base_comps.pop(0)
    child_comps = oci.pagination.list_call_get_all_results(identity.list_compartments,target.id)
    base_comps.extend(child_comps.data)
    all_comps.extend(child_comps.data)
act_comps =[]
for compartment in all_comps:
    if compartment.lifecycle_state=='ACTIVE':
        act_comps.append(compartment)

# Gathering Subscribed regions
reg =["us-ashburn-1","ap-hyderabad-1"]
#region = identity.list_region_subscriptions(compartment_id)
#for r in region.data:
#    reg.append(r.region_name)
#print(reg)

# Staring Loops to execute AutoStop Script
for x in act_comps:
    print("Current compartment is:",x.name)
    print("\n")
    for y in range(0,len(reg)):
        print("     Current Region is:",reg[y])
        print("\n")
        config = {
                "user": userocid,
                "key_file": key_file,
                "fingerprint": fingerprint,
                "tenancy": compartment_id,
                "region": reg[y],
                "compartment_id": x.id}

        ################ COMPUTE INSTANCES ####################################
        print("     ####### Executing Compute Instance AutoStart Script #######")
        compute = oci.core.ComputeClient(config)
        df = compute.list_instances(x.id,lifecycle_state='STOPPED')
        if len(df.data)>0:
            print("         Number of Running Compute Instances: ",len(df.data))
            for ins in df.data:
                if ('Dev' in ins.freeform_tags and ins.freeform_tags['Dev'] == 'Yes') or ('Test' in ins.freeform_tags and ins.freeform_tags['Test'] == 'Yes'):
                    compute.instance_action(ins.id,"START")
                    print("             Starting Compute Instance",ins.display_name)
                else:
                    print("             Skipping Compute Instance",ins.display_name)


        else:
            print("         ####### NO COMPUTE INSTANCES TO START #######")
        print("     ####### Completed Compute Instance AutoStart Script #######")
        print("\n")
        ################ COMPUTE INSTANCES #####################################
