import kicks3

s3=kicks3.finds3(['https://app.geniebelt.com'])
if s3[0]!='Bucket not found':
   print(kicks3.scan_s3(s3))
else:
    print(s3[0])