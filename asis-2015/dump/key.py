import hashlib
key = raw_input('Please enter the access key: ').strip()
if len(key) == 38:
    key_ar = key.split('-')
    if len(key_ar) == 5:
        if int(key_ar[0].encode('hex'), 16) ==  58559604012647:
            if int(key_ar[1].encode('hex'), 16) == 27697077611219024:
                if int(key_ar[2].encode('hex'), 16) == 28839576914310229:
                    if int(key_ar[3].encode('hex'), 16) == 14469853439423811:
                        if int(key_ar[4].encode('hex'), 16) == 21189029315236706:
                            print key[18] + key[-2] + chr(ord(key[26]) - 1) + key[-2] + '{' + hashlib.md5(key).hexdigest() + '}'
                        else:
                            print 'You access key is not correct! Banned!!'
                    else:
                        print 'You access key is not correct! Banned!!'
                else:                    
					print 'You access key is not correct! Banned!!'  
        else:
            print 'You access key is not correct! Banned!!'
    else:
        print 'You access key is not correct! Banned!!'
else:
    print 'You access key is not correct! Banned!!'
