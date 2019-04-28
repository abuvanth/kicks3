#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests,re,argparse,urllib
import os 
import json
import boto3
import colorama
import sublist3r
from colorama import init, Fore, Back, Style
init(autoreset=True)
content="test file from kick-s3 tool"
cookies=''
ap = argparse.ArgumentParser()
ap.add_argument("-u", "--url", required=True,help="Please enter target Url start with http or https")
ap.add_argument("-c", "--cookie", required=False,help="Paste ur cookie values for authentication purpose")
ap.add_argument("-l", "--list", required=False,help="list of sites for testing Eg. sitelist.txt")
ap.add_argument("-s", "--subdomain", required=False,help=" True or False")
args = vars(ap.parse_args())
def check_listings (url,bucket):
        s3=boto3.client('s3')
	try:
		session = requests.Session()
		headers = {"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Upgrade-Insecure-Requests":"1","User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0","Connection":"close","Accept-Language":"en-US,en;q=0.5","Accept-Encoding":"gzip, deflate"}
		response = session.get("http://"+url+"", headers=headers)
		if "<ListBucketResult xmlns" in response.content:
			write_listable (url)
			print (Fore.GREEN +"[*] S3 Bucket Lists Files for unathenticated users [*]")
			return True
                if s3.list_objects(Bucket=bucket):
                   print (Fore.GREEN +"[*] S3 Bucket Lists Files for all aws athenticated users [*]")
                   return True
		if response.status_code == 403:
			return True
	except Exception,e:
		print (Fore.RED +"[*] Directory Listings ... Access Denied [*]")
		#print str(e)
		pass

def check_upload (bucket,url):
	try:
		s3=boto3.resource('s3')
                obj=s3.Object(bucket, 'poc.txt').put(Body=content)
                s3.ObjectAcl(bucket,'poc.txt').put(ACL='public-read')
		write_uploadable(bucket,url)
	except Exception,e:
		#print str(e)
		print (Fore.RED +"[*] No POC Uploaded... Access Denied [*]")
		pass

def write_listable (url):
	print (Fore.GREEN +"[*] Directory Listings Enabled [*]")

def write_uploadable (bucket,url):
	print (Fore.RED + "[*] POC Uploaded! [*]"+'- '+url+'/poc.txt')

def scan_s3(f):
	for line in f:
            url=line.replace('\/','/') #if json escape
            if 'amazonaws.com/' in url:
                b_name=url.split('/')[1]
            else:
                b_name=url.split('.s3')[0]
            print(Fore.YELLOW +"[*] Bucket: "+b_name+" [*]")
	    if check_listings (url,b_name) == True:
               check_upload(b_name,url)

def remove_duplicate(x):
    return list(dict.fromkeys(x))	       
sitelist=[]
targeturl=args['url']
sitelist=sitelist+[targeturl]
if args['cookie']:
   cookies=args['cookie']
if args['list']:
   sitelist=sitelist+open(args['list'],'r').readlines()

for targetsite in sitelist:      
    try:
        if args['subdomain']:
           print('Enumerating Subdomains')
           subdomains = sublist3r.main(targetsite, 40, targetsite+'_subdomains.txt', ports= None, silent=True, verbose= False, enable_bruteforce= False, engines=None)
           targetsite=[targetsite]
           targetsite=targetsite+subdomains
        else:
           targetsite=[targetsite]
        for target in targetsite:
            if not target.startswith('http'):
               target='http://'+target.strip()
            bucket=[]
            html=requests.get(target,headers={'cookie':cookies}).content
            html=urllib.unquote(html)
            regjs=r"(?<=src=['\"])[a-zA-Z0-9_\.\-\:\/]+\.js"
            regs3=r"[a-zA-Z\-_0-9.]+\.s3\.?(?:[a-zA-Z\-_0-9.]+)?\.amazonaws\.com|(?<!\.)s3\.?(?:[a-zA-Z\-_0-9.]+)?\.amazonaws\.com\\?\/[a-zA-Z\-_0-9.]+"
            js=re.findall(regjs,html)
            s3=re.findall(regs3,html)
            bucket=bucket+s3
            print(Fore.BLUE +"Target : "+target+' scanning and testing')
            if len(js)>0:
               for i  in js:
                  if i.startswith('//'):
                     jsurl=i.replace('//','http://')
                  elif i.startswith('http'):
                       jsurl=i
                  else:
                       jsurl=target+'/'+i
                  try:
                      jsfile=requests.get(jsurl,timeout=10,headers={'cookie':cookies}).content
                      s3=re.findall(regs3,jsfile)
                  except Exception as y:
                         #print(y)
                         pass
                  if s3:
                     bucket=bucket+s3
            if len(bucket)==0:
               print("Bucket Not Found")
               pass
            else:
                scan_s3(remove_duplicate(bucket))
    except Exception as x:
           #print(x)
           pass

