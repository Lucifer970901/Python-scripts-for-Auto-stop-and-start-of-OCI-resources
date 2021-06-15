Pre requisites:

installation in oracle linux
1.install python packages:
 sudo yum install -y python3
2.install OCI cli packages:
 sudo yum install python36-oci-cli

3.fetch the OCID (from tenancy, users and compartments and provide them in the script configuration)

4.create the public key file pem format and add the API key and generate the fingerprint.
# Private key generation
 
$ mkdir ~/.oci
$ openssl genrsa -out ~/.oci/oci_api_key.pem 2048
$ chmod go-rwx ~/.oci/oci_api_key.pem
 
# Public key generation
$ openssl rsa -pubout -in ~/.oci/oci_api_key.pem -out ~/.oci/oci_api_key_public.pem
 
# Fingerprint generation
$ openssl rsa -pubout -outform DER -in ~/.oci/oci_api_key.pem | openssl md5 -c
