#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests,re,argparse
bucket=[]
cookies=''
ap = argparse.ArgumentParser()
ap.add_argument("-u", "--url", required=True,help="Please enter target Url start with http or https")
ap.add_argument("-c", "--cookie", required=False,help="Paste ur cookie values for authentication purpose")
args = vars(ap.parse_args())
target=args['url']
if args['cookie']:
   cookies=args['cookie']
def remove_duplicate(x):
  return list(dict.fromkeys(x))
try:
   html=requests.get(target,timeout=10,headers={'cookie':cookies}).content
   regjs=r"(?<=src=['\"])[a-zA-Z0-9_\.\-\:\/]+\.js"
   regs3=r"[a-zA-Z\-_0-9.]+\.s3\.?(?:[a-zA-Z\-_0-9]+)?\.amazonaws\.com|(?<!\.)s3\.?(?:[a-zA-Z\-_0-9]+)?\.amazonaws\.com\/[a-zA-Z\-_0-9.]+"
   js=re.findall(regjs,html)
   s3=re.findall(regs3,html)
   bucket=bucket+s3
   print("Please  Wait")
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
          except Exception as y:
                 print(y)
                 pass
          s3=re.findall(regs3,jsfile)
          if s3:
             bucket=bucket+s3
except Exception as x:
       print(x)
       pass
if len(bucket)==0:
   print("Bucket Not Found")
for b in remove_duplicate(bucket):
    print(b)
