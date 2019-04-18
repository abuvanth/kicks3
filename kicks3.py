import requests,re,argparse
bucket=[]
ap = argparse.ArgumentParser()
ap.add_argument("-u", "--url", required=True,help="Please enter Url start with http or https")
args = vars(ap.parse_args())
target=args['url']
def remove_duplicate(x):
  return list(dict.fromkeys(x))
try:
   html=requests.get(target,timeout=10).content
   findjs=r"(?<=src=['\"])[a-zA-Z0-9_\.\-\:\/]+\.js"
   js=re.findall(findjs,html)
   s3=re.findall(r"[a-zA-Z\-_0-9]+\.s3\.?(?:[a-zA-Z\-_0-9]+)?\.amazonaws\.com",html)
   print("Please  Wait")
   #print(s3)
   if len(js)>0:
      for i  in js:
          if i.startswith('/'):
             jsurl=i.replace('//','http://')
             print(jsurl)
          elif i.startswith('http'):
               jsurl=i
          else:
               jsurl=target+'/'+i
          jsfile=requests.get(jsurl,timeout=10).content
          s3=re.findall(r"[a-zA-Z\-_0-9]+\.s3\.?(?:[a-zA-Z\-_0-9]+)?\.amazonaws\.com",jsfile)
          if s3:
             bucket=bucket+s3
except Exception as x:
       print x
       pass
for b in remove_duplicate(bucket):
    print(b)
