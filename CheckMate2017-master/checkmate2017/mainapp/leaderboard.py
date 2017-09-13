import urllib, requests, sys

def pingservers():
    iplist=['127.0.0.1','127.0.0.1']
    ob=[]
    i=0
    for ip in iplist:

    	urlx='http://'+ip+':8000/pingme'
    	client=requests.session()
    	client.get(urlx)
    	csrftoken=client.cookies['csrf']

    	datax={
    	"z":"okay",
    	"csrfmiddlewaretoken":csrftoken,
    	}

    	r = client.post(urlx, data=datax, headers=dict(Referer=urlx))
    	print(r)
