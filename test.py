import kicks3
blist=open('s3_bucket_pub.csv','r').readlines()
b_list=[]
for i in blist:
    print(i)
    b_list.append(i.split(',')[3])
print(b_list)
#result=kicks3.scan_s3(blist)
