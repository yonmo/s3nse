#!/usr/bin/env python3

import os, boto3, dotenv, sys

from botocore.exceptions import ClientError

# !!!! OUT OF SCOPE !!!! (I SWEAR I WILL EAT YOUR LEGS) !!!! OUT OF SCOPE !!!! #

class s3nse:
    def __init__(self):
        dotenv.load_dotenv()
        environment_keys = ['REGION', 'ENDPOINT', 'ACCESS_ID', 'SECRET_KEY', 'BUCKET']
        self.configuration = tuple(os.getenv(x) for x in environment_keys)
        self.session = boto3.session.Session()
        self.configure()
        pass

    def configure(self):
        try:
            
            self.session = self.session.client('s3', 
                region_name = self.configuration[0],
                endpoint_url = self.configuration[1],
                aws_access_key_id = self.configuration[2],
                aws_secret_access_key = self.configuration[3])

        except IndexError as err:
            print(err)
            self.terminate()
        pass

    def terminate(self):
        print('\nExiting s3nse...')
        exit()

# !!!! OUT OF SCOPE !!!! (I SWEAR I WILL EAT YOUR LEGS) !!!! OUT OF SCOPE !!!! #

def listFiles(kargs):
    '''
        listFiles function for returning file names within an s3 bucket file based on BUCKET variable.
    '''

    try:

        if kargs != None:
            BUCKET = kargs[0]

        client = s3nse().session
        bucket = client.list_objects(Bucket=BUCKET)
        for file in bucket['Contents']:
            print(file['Key'])

    except ClientError as err:
        print(err)
        raise(ClientError)

    except IndexError as err:
        print(err)
        raise(IndexError)
    
def pullFiles(kargs):
    '''
        getFiles function for downloading files based on BUCKET and KEY variables.
    '''
   
    try:

        if kargs != None:
            BUCKET = kargs[0]
            KEY = kargs[1]

        client = s3nse().session
        client.download_file(Bucket=BUCKET, Key=KEY, Filename=KEY)

    except ClientError as err:
        print(err)
        raise(ClientError)

    except IndexError as err:
        print(err)
        raise(IndexError)

def pushFiles(kargs):
    '''
        pushFiles function for uploading files based on BUCKET and KEY variables.
    '''

    try:

        if kargs != None:
            print(kargs)
            BUCKET = kargs[0]
            FILENAME = kargs[1]

        client = s3nse().session
        client.upload_file(Filename=FILENAME, Bucket=BUCKET, Key=FILENAME)

    except ClientError as err:
        print(err)
        raise(ClientError)

    except IndexError as err:
        print(err)
        raise(IndexError)

def delFiles(kargs):
    '''
        delFiles function for deleting files based on BUCKET and KEY variables
    '''

    try:

        if kargs != None:
            BUCKET = kargs[0]
            KEY = kargs[1]

        client = s3nse().session
        client.delete_object(Bucket=BUCKET, Key=KEY)
        
    except ClientError as err:
        print(err)
        raise(ClientError)

    except IndexError as err:
        print(err)
        raise(IndexError)

if __name__ == '__main__':
    functions = [listFiles, pullFiles, pushFiles, delFiles]
    commands = dict({x.__qualname__: x for x in functions})
    try:
        args = sys.argv[1::]
        if (len(args) > 0):
            if (commands.get(args[0])):
                    output = commands.get(args[0])(args[1::] if len(args) > 1 else None)
                    print(output if output != None else '')
    
    except IndexError:
        print('\nIncorrect number of arguments specified.')
        s3nse.terminate()
    
    except ClientError:
        print('\nClient error in the s3nse module.')    
        s3nse.terminate()
    
    except KeyboardInterrupt:
        s3nse.terminate()
