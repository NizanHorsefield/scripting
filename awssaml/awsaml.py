#!/usr/bin/env python3
"""
awsaml.py v1.0

Based on the script from
https://blogs.aws.amazon.com/security/post/Tx1LDN0UBGJJ26Q/How-to-Implement-Federated-API-and-CLI-Access-Using-SAML-2-0-and-AD-FS#postCommentsTx1LDN0UBGJJ26Q
Changes were made to
- use python3 to get rid of unicode annoyances
- use separate config and credentials files as aws cli does by default
- report cleanly a failed authentication

Requires boto, beautifulsoup4, requests, and requests_ntlm:- 

    pip3 install boto requests beautifulsoup4 requests_ntlm

Boto docs: https://kite.com/docs/python/boto.sts.connection.STSConnection.assume_role_with_saml


Still to do:
 - create profile with name of AWS account alias aws  --profile 445189663936 iam list-account-aliases
 - perhaps lo
 - https://unix.stackexchange.com/questions/1800/how-to-specify-a-custom-autocomplete-for-specific-commands
 - switch to this profile via aws_switch with appropriate env vars
   i.e. AWS_PROFILE http://docs.aws.amazon.com/cli/latest/userguide/cli-multiple-profiles.html
    http://docs.aws.amazon.com/cli/latest/userguide/cli-environment.html
 - save the token expiry time to a var in the config
"""

import sys
import boto.sts
import boto.s3
import requests
import getpass
import configparser
import base64
import os
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from os.path import expanduser
from requests_ntlm import HttpNtlmAuth

##########################################################################
# Variables

# region: The default AWS region that this script will connect
# to for all API calls
region = 'eu-west-1'

# output format: The AWS CLI output format that will be configured in the
# saml profile (affects subsequent CLI calls)
outputformat = 'json'

# aws_configfile and aws_credentialsfile: The files where this script will store the temp
# credentials under the saml profile
aws_home = expanduser("~") + '/.aws'
aws_credentialsfile = aws_home + '/credentials'
aws_configfile = aws_home + '/config'
aws_tfvarsfile = aws_home + '/exportawsvars.sh'

if not os.path.exists(aws_home):
    os.makedirs(aws_home)

# SSL certificate verification: Whether or not strict certificate
# verification is done, False should only be used for dev/test
sslverification = True

# fully qualified domain name of your adfs
fqdn = 'federation.reedelsevier.com'

# idpentryurl: The initial URL that starts the authentication process.
idpentryurl = 'https://'+fqdn+'/adfs/ls/IdpInitiatedSignOn.aspx?loginToRp=urn:amazon:webservices'

# END: Variables
##########################################################################

# Get the federated credentials from the user

region = input("Region: ")      # Don't default to a specific region

username = input("Username: ") #if not os.environ['ELS_AD'] else os.environ['ELS_AD']

password = getpass.getpass(prompt="Password: ")

# Initiate session handler
session = requests.Session()

# Programatically get the SAML assertion
# Set up the NTLM authentication handler by using the provided credential
session.auth = HttpNtlmAuth(username, password, session)

# Opens the initial AD FS URL and follows all of the HTTP302 redirects
# The adfs server I am using this script against returns me a form, not ntlm auth, so we cheat here giving it a
# browser header so it gives us the NTLM auth we wanted.
headers = {'User-Agent': 'Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}
response = session.get(idpentryurl, verify=sslverification, headers=headers)

# Debug the response if needed
# print(response)

# Exits if the authentication failed
if response.status_code != 200:
    print('Authentication failed!')
    sys.exit(1)

# Overwrite and delete the credential variables, just for safety
username = '##############################################'
password = '##############################################'
del username
del password

# Decode the response and extract the SAML assertion
soup = BeautifulSoup(response.text, "html.parser")
assertion = ''

# Look for the SAMLResponse attribute of the input tag (determined by
# analyzing the debug print lines above)
for inputtag in soup.find_all('input'):
    if inputtag.get('name') == 'SAMLResponse':
        # print(inputtag.get('value'))
        assertion = inputtag.get('value')

# Parse the returned assertion and extract the authorized roles
awsroles = []
root = ET.fromstring(base64.b64decode(assertion))

for saml2attribute in root.iter('{urn:oasis:names:tc:SAML:2.0:assertion}Attribute'):
    if saml2attribute.get('Name') == 'https://aws.amazon.com/SAML/Attributes/Role':
        for saml2attributevalue in saml2attribute.iter('{urn:oasis:names:tc:SAML:2.0:assertion}AttributeValue'):
            awsroles.append(saml2attributevalue.text)

# Note the format of the attribute value should be role_arn,principal_arn
# but lots of blogs list it as principal_arn,role_arn so let's reverse
# them if needed
for awsrole in awsroles:
    chunks = awsrole.split(',')
    if'saml-provider' in chunks[0]:
        newawsrole = chunks[1] + ',' + chunks[0]
        index = awsroles.index(awsrole)
        awsroles.insert(index, newawsrole)
        awsroles.remove(awsrole)

# If I have more than one role, ask the user which one they want,
# otherwise just proceed
print("")
if len(awsroles) > 1:
    i = 0
    print("Please choose the role you would like to assume:")
    for awsrole in awsroles:
        print ('[', i, ']: ', awsrole.split(',')[0])
        i += 1

    # Ensure input is a valid selection from the list
    while True:
        selectedroleindex = int(input("Selection: "))
        if (int(selectedroleindex) < 0) or (int(selectedroleindex) > int(len(awsroles) - 1)):
            print('You selected an invalid role index, please try again')
            continue
        else:
            role_arn = awsroles[int(selectedroleindex)].split(',')[0]
            principal_arn = awsroles[int(selectedroleindex)].split(',')[1]
            config_profile = principal_arn.split(':')[4] + "-" + role_arn.split('/')[1]
            break

else:
    role_arn = awsroles[0].split(',')[0]
    principal_arn = awsroles[0].split(',')[1]
    config_profile = principal_arn.split(':')[4] + "-" + role_arn.split('/')[1]

# Use the assertion to get an AWS STS token using Assume Role with SAML
conn = boto.sts.connect_to_region(region, anon=True)
token = conn.assume_role_with_saml(role_arn, principal_arn, assertion)

# Read in the existing config file
config = configparser.RawConfigParser()
# config = ConfigParser.RawConfigParser()
config.read(aws_configfile)

# Put the credentials into a specific profile instead of clobbering
# the default credentials
if not config.has_section("profile " + config_profile):
    config.add_section("profile " + config_profile)

    config.set("profile " + config_profile, 'output', outputformat)
    config.set("profile " + config_profile, 'region', region)

# Write the updated config file
with open(aws_configfile, 'w+') as configfile:
    config.write(configfile)
    configfile.close()

# Write the AWS STS token into the AWS credentials file
# Read in the existing config file
config = configparser.RawConfigParser()
# config = ConfigParser.RawConfigParser()
config.read(aws_credentialsfile)

# Put the credentials into a specific profile instead of clobbering
# the default credentials
if not config.has_section(config_profile):
    config.add_section(config_profile)

config.set(config_profile, 'aws_access_key_id', token.credentials.access_key)
config.set(config_profile, 'aws_secret_access_key', token.credentials.secret_key)
config.set(config_profile, 'aws_session_token', token.credentials.session_token)
config.set(config_profile, 'aws_session_token_expiration', token.credentials.expiration)

# Write the updated config file
with open(aws_credentialsfile, 'w+') as credentialsfile:
    config.write(credentialsfile)
    credentialsfile.close()

with open(aws_tfvarsfile, 'w+') as tfvarsfile:
    tfvarsfile.write("#!/bin/sh\n")
    tfvarsfile.write("export AWS_ACCESS_KEY_ID=\"" + token.credentials.access_key + "\"\n")
    tfvarsfile.write("export AWS_SECRET_ACCESS_KEY=\"" + token.credentials.secret_key + "\"\n")
    tfvarsfile.write("export AWS_SESSION_TOKEN=\"" + token.credentials.session_token + "\"\n")
    tfvarsfile.write("export AWS_DEFAULT_REGION=\"" + region + "\"\n")
    tfvarsfile.write("export TF_VAR_ACCESS_KEY=\"" + token.credentials.access_key + "\"\n")
    tfvarsfile.write("export TF_VAR_SECRET_KEY=\"" + token.credentials.secret_key + "\"\n")
    tfvarsfile.close()
 
# Give the user some basic info as to what has just happened
print('\n\n--------------------------------------------------------------------------------\n')
print('Your new access key pair has been stored in your AWS configuration files under the profile:\n\n\t' + format(config_profile) + '\n')
print('This will expire in 1 hour (' + token.credentials.expiration + ', after which you may safely rerun this script to refresh your access key pair.\n')
#print('\n')
print('To use this credential call the AWS CLI with the --profile option ')
print('(e.g. aws --profile {0} ec2 describe-instances).'.format(config_profile) + '\n')
#print('\n')
print('A script to assign these variables has been created. Simply run it as follows to have the correct variables in your environment:-', end='')
print('\n')
print('\tsource ' + aws_home + '/exportawsvars.sh')
print('\n--------------------------------------------------------------------------------\n\n')
