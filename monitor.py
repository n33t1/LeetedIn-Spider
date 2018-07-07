import hashlib   

m2 = hashlib.md5()   
m2.update(src)   
print m2.hexdigest()   