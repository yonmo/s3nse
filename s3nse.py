#!/usr/bin/env python3

import os, boto3, dotenv, sys

dotenv.load_dotenv()

# !!!! OUT OF SCOPE !!!! (I SWEAR I WILL EAT YOUR LEGS) !!!! OUT OF SCOPE !!!! #
REGION = os.getenv('REGION')
ENDPOINT = os.getenv('ENDPOINT')
ACCESS_ID = os.getenv('ACCESS_ID')
SECRET_KEY = os.getenv('SECRET_KEY')
BUCKET = os.getenv('BUCKET')
# !!!! OUT OF SCOPE !!!! (I SWEAR I WILL EAT YOUR LEGS) !!!! OUT OF SCOPE !!!! #

client = boto3.session.Session().client('s3', 
                                    region_name=REGION, 
                                    endpoint_url=ENDPOINT, 
                                    aws_access_key_id=ACCESS_ID, 
                                    aws_secret_access_key=SECRET_KEY)

def listFiles(kargs):
    '''
        listFiles function for returning file names within an s3 bucket file based on BUCKET variable.
    '''
    if kargs != None:
        BUCKET = kargs[0]
    try:
        bucket = client.list_objects(Bucket=BUCKET)
        for file in bucket['Contents']:
            print(file['Key'])
        return(0)
    except:
        return(1)
    
def pullFiles(kargs):
    '''
        getFiles function for downloading files based on BUCKET and KEY variables.
    '''
    if kargs != None:
        BUCKET = kargs[0]
        KEY = kargs[1]
    try:
        client.download_file(Bucket=BUCKET, Key=KEY, Filename=KEY)
        return(0)
    except:
        return(1)

def pushFiles(kargs):
    '''
        pushFiles function for uploading files based on BUCKET and KEY variables.
    '''
    if kargs != None:
        BUCKET = kargs[0]
        KEY = kargs[1]
    try:
        client.download_file(Bucket=BUCKET, Key=KEY, Filename=KEY)
        return(0)
    except:
        return(1)

if __name__ == '__main__':
    functions = [listFiles, pullFiles, pushFiles]
    commands = dict({x.__qualname__: x for x in functions})
    try:
        args = sys.argv[1::]
        if (len(args) > 0):
            if (commands.get(args[0])):
                    output = commands.get(args[0])(args[1::] if len(args) > 1 else None)
                    print(output if output != None else '')
    except KeyboardInterrupt:
        print('\nExiting s3nse...')
        exit()