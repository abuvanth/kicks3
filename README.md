# kicks3
S3 bucket finder from html,js and bucket misconfiguration testing tool

pip install awscli

aws configure


# Installation


pip install kick-s3


# OR

git clone https://github.com/abuvanth/kicks3.git

cd kicks3

pip install -r requirements.txt

## Usage

# single target

python kicks3.py -u http://target

# list of target 

python kicks3.py -u http://target -l sitelist.txt

# authenticated page


python kicks3.py -u http://target -c 'cookievalues'



# subdomains

python kicks3.py -u target.com -s 1


# Use kicks3 as a module
```
import kicks3

bucketurllist=kicks3.finds3('target.com')
bucketlist=kicks3.get_bucket_name(bucketurllist)
scan_result=kicks3.scan_s3(bucketlist)

for result in scan_result:

    print(result)#bucketname(testname),listable_for_unauth_users(true or false),listable_auth_users(true or false),writable(true or false)
```

# buckets from textfile

```
import kicks3
blist=open('s3.buckets.txt','r').readlines()
result=kicks3.scan_s3(blist)
```
# Scan for subdomains 
```
bucketurllist=kicks3.finds3(['target.com'],sub=1,cookies='valueofyoursitescookie') #cookies for authenticated pages,
bucketlist=kicks3.get_bucket_name(bucketurllist)
scan_result=kicks3.scan_s3(bucketlist)

for result in scan_result:

    print(result)#bucketname(testname),listable_for_unauth_users(true or false),listable_auth_users(true or false),writable(true or false)
```

## results are stored in s3out.txt file.


Note: sub and cookies are optional parameters of finds3 function
