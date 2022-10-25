import os, subprocess, time, boto3, re, dotenv

dotenv.load_dotenv()

# !!!! OUT OF SCOPE !!!! (I SWEAR I WILL EAT YOUR LEGS) !!!! OUT OF SCOPE !!!! #
REGION = os.getenv('REGION')
ENDPOINT = os.getenv('ENDPOINT')
ACCESS_ID = os.getenv('ACCESS_ID')
SECRET_KEY = os.getenv('SECRET_KEY')
BUCKET = os.getenv('BUCKET')
# !!!! OUT OF SCOPE !!!! (I SWEAR I WILL EAT YOUR LEGS) !!!! OUT OF SCOPE !!!! #

# Initiate Global Client Session
client = boto3.session.Session().client('s3', 
                                        region_name=REGION, 
                                        endpoint_url=ENDPOINT, 
                                        aws_access_key_id=ACCESS_ID, 
                                        aws_secret_access_key=SECRET_KEY)

def listFiles(BUCKET):
    '''
        listFiles function for returning file names within an s3 bucket file based on BUCKET variable.
    '''
    try:
        bucket = client.list_objects(Bucket=BUCKET)
        for file in bucket['Contents']:
            print(file['Key'])
        return(0)
    except:
        return(1)
    
def getFile(BUCKET, KEY):
    '''
        getFile function for getting files and downloading them based on BUCKET and KEY variables.
    '''
    try:
        client.download_file(Bucket=BUCKET, Key=KEY, Filename=KEY)
        return(0)
    except:
        return(1)

def initialize(kargs):
    '''
        initialize bashrc and init defaults
    '''
    return(kargs)

def firewall(kargs):
    return(kargs)

def configureService(kargs):
    '''
        configureService function for getting a hardened config and deploying it
    '''
    apache  = {'CONFIG': 'apache2.conf', 'PATH': '/etc/apache2/', 'RESTART': 'service apache2.service restart'}
    sshd    = {'CONFIG': 'sshd_config', 'PATH': '/etc/ssh/', 'RESTART': 'service sshd.service restart'}
    
    services = [apache, sshd]
    if (len(kargs) > 0):
        for service in services:
            try:
                # Parse Out Dangerous Characters To Avoid Quirky Eval Possibilities
                input = re.sub(r'[^a-zA-Z]', '', kargs[0])
                if (eval(input) == service) or (input == 'all'):
                    if (getFile(BUCKET, service['CONFIG']) == 0):
                        process = subprocess.run('sudo cp ' + service['CONFIG'] + ' ' + service['PATH'], shell=True, capture_output=True, text=True)
                        print(process.stdout)
                        process = subprocess.run(service['RESTART'], shell=True, capture_output=True, text=True)
                        print(process.stdout)
                    else:
                        print('A Configuration File GET Failure Occurred - KEY: ' + service['CONFIG'])
            except NameError:
                break
    return

def backupLog(kargs):
    # /var/log/auth.log Authentication Logs
    # /var/log/kern.log Kernal Logs
    # /var/log/cron.log Cron Job Logs
    # /var/log/httpd/ Apache Logs
    # /var/log/nginx/ Nginx Logs
    # /var/log/apt/ Package Logs
    return(kargs)

if __name__ == '__main__':
    functions = [firewall, backupLog, configureService]
    commands = dict({x.__qualname__: x for x in functions})
    try:
        while(True):
            os.system('cls')
            cmd = input('>> ')
            args = cmd.split(' ')
            if (len(args) > 0):
                if (commands.get(args[0])):
                    output = commands.get(args[0])(args[1::])
                    print(output if output != None else '')
                    time.sleep(3)
    except KeyboardInterrupt:
        print('\nExiting s3nse...')
        exit()

'''
sudo iptables -F
sudo iptables -X
sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT
sudo iptables -A INPUT -j DROP


aliasing history -cw as a method to save the history logs
'''
