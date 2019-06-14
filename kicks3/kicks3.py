#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests,re,argparse,urllib
import os 
import json
import boto3
import colorama
import kickdomain
from colorama import init, Fore, Back, Style
init(autoreset=True)
def check_listings (url,bucket):
        s3=boto3.client('s3')
	try:
		session = requests.Session()
		headers = {"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Upgrade-Insecure-Requests":"1","User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0","Connection":"close","Accept-Language":"en-US,en;q=0.5","Accept-Encoding":"gzip, deflate"}
		response = session.get("http://"+url+"", headers=headers)
		if "<ListBucketResult xmlns" in response.content:
			unauth=True
                if s3.list_objects(Bucket=bucket):
                   auth=True
	except Exception,e:
		#print str(e)
		return (False,False)
        return (unauth, auth)

def check_upload (bucket,url):
        content="test file from kick-s3 tool"
	try:		   
            s3=boto3.resource('s3')
            s3.Object(bucket, 'poc.txt').put(Body=content)
            s3.ObjectAcl(bucket,'poc.txt').put(ACL='public-read')
	    return True
	except Exception,e:		
               return False
def scan_s3(f):
        result=[]
	for line in f:
            url=line.replace('\/','/') #if json escape
            if 'amazonaws.com/' in url:
                b_name=url.split('/')[1]
            else:
                b_name=url.split('.s3')[0]
	    listing=check_listings (url,b_name)
            upload=check_upload(b_name,url)
            result=result+[(b_name,listing[0],listing[1],upload)]
        return result

def remove_duplicate(x):
    return list(dict.fromkeys(x))	       

def finds3(sitelist,cookies='',sub=0):
    bucket=[]
    for targetsite in sitelist:      
        try:
            if sub:
               print('Enumerating Subdomains')
               subdomains = kickdomain.getSubdomains(targetsite)
               targetsite=[targetsite]
               targetsite=targetsite+subdomains
            else:
               targetsite=[targetsite]
            for target in targetsite:
                if not target.startswith('http'):
                   target='http://'+target.strip()
                html=''
                try:
                  html=requests.get(target,headers={'cookie':cookies},timeout=10).content
                except:
                   pass
                html=urllib.unquote(html)
                regjs=r"(?<=src=['\"])[a-zA-Z0-9_\.\-\:\/]+\.js"
                regs3=r"[a-zA-Z\-_0-9.]+\.s3\.?(?:[a-zA-Z\-_0-9.]+)?\.amazonaws\.com|(?<!\.)s3\.?(?:[a-zA-Z\-_0-9.]+)?\.amazonaws\.com\\?\/[a-zA-Z\-_0-9.]+"
                js=re.findall(regjs,html)
                s3=re.findall(regs3,html)
                bucket=bucket+s3
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
                   return ['Bucket not found']
                else:
                    bucket=bucket+s3
        except Exception as x:
               pass
    return remove_duplicate(bucket)
if __name__=='__main__':
   ap = argparse.ArgumentParser()
   ap.add_argument("-u", "--url", required=True,help="Please enter target Url start with http or https")
   ap.add_argument("-c", "--cookie", required=False,help="Paste ur cookie values for authentication purpose")
   ap.add_argument("-l", "--list", required=False,help="list of sites for testing Eg. sitelist.txt")
   ap.add_argument("-s", "--subdomain", required=False,help=" True or False")
   args = vars(ap.parse_args())
   sitelist=[]
   cookies=''
   targeturl=args['url']
   sitelist=sitelist+[targeturl]
   if args['cookie']:
      cookies=args['cookie']
   if args['list']:
      sitelist=sitelist+open(args['list'],'r').readlines()
   s3=finds3(sitelist,cookies,sub=args['subdomain'])
   if len(s3)!=0:
       results=scan_s3(s3)
       for i in results:
           print("Bucket name: "+i[0])
           if i[1]:
              print (Fore.GREEN +"[*] S3 Bucket Lists Files for unauthenticated users [*]")
           if i[2]:
              print (Fore.GREEN +"[*] S3 Bucket Lists Files for all aws authenticated users [*]")
           else:
    	        print (Fore.RED +"[*] Directory Listings ... Access Denied [*]")
           if i[3]:
              print (Fore.GREEN +"[*] File uploaded Successfully [*]")
           else:
              print (Fore.RED +"[*] File  Not Upload ... Access Denied [*]")


