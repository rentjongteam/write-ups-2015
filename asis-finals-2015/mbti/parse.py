import pyshark

cap = pyshark.FileCapture("mbti.pcap")
for i in cap:
    if 'ssl' in i:
        if 'app_data' in dir(i.ssl):
            data = i.ssl.app_data.replace(':', '').decode('hex')    
            print "APP DATA ", i.ip.src, len(data)    
