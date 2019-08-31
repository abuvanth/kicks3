# kicks3

S3 bucket finder from html,js and bucket misconfiguration testing tool.

Currently this tool check three testcases

1. Object listing for Unauthenticated users

2. Object listing for Authenticated users

3. Public writable for all aws users

pip install awscli

aws configure

### get your aws keys from aws console

# Installation

pip install kick-s3


# OR

git clone https://github.com/abuvanth/kicks3.git

cd kicks3

python setup.py install

## Usage


##demo
[![asciicast](https://asciinema.org/a/265305.svg)](https://asciinema.org/a/265305)



# single target

 kicks3.py -u http://target
 
 this will looking for s3 buckets in html and javascript files.

# Single Bucket 

 kicks3.py -b bucketname
 
 test single bucket name

# Bucket list

 kicks3.py -bl bucketnamelist.txt

# list of websites 

 kicks3.py -u http://target -l sitelist.txt

# authenticated page

 kicks3.py -u http://target -c 'cookievalues'

# subdomains

 kicks3.py -u target.com -s 1


# Use kicks3 as a module
```
import kicks3

bucketurllist=kicks3.finds3('target.com')
bucketlist=kicks3.get_bucket_name(bucketurllist)
scan_result=kicks3.scan_s3(bucketlist)

for result in scan_result:

    print(result)#bucketname(testname),listable_for_unauth_users(true or false),listable_auth_users(true or false),writable(true or false)
```

# buckets from text file

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
