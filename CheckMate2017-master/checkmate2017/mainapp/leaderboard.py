import urllib2

def pingservers():
    iplist={}
    ob={}
    for ip in iplist:
        req = urllib2.Request("http://"+ip+":8000/pingme")
        ob[i]=(urllib2.urlopen(req).read())
    return(ob)

    
