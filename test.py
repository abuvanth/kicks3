import kicks3
blist=open('s3.buckets.txt','r').readlines()
result=kicks3.scan_s3(blist)
