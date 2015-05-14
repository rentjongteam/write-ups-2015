from hashlib import md5

words = (open("/Volumes/exia/Pentest/tools/Dictionaries/hashkiller.com.dic", 'r')).readlines()
realm="this page for admin only, go out now!"
method_uri="GET:/login.php"
nonce="554aed8c0b2d8"
response="ab134aafc79ad5a930920c7e5d2a7dcf"
opaque="d073cc4342291e6270746b4675498022"
qop="auth"
nc="0000001d"
cnonce="5fdeab67ece1fb54" 
user="factoreal"
hash2= md5(method_uri).hexdigest()

for pwd in words:
    hash1 =md5("%s:%s:%s"%(user,realm,pwd.strip())).hexdigest()
    result =md5("%s:%s:%s:%s:%s:%s"%(hash1,nonce,nc,cnonce,qop,hash2)).hexdigest()
    if result==response:
		print "cracked: "+ user+":"+pwd
		exit(0)
    else:
		print 'Tested hash value: %s' %result
