#!/usr/bin/env python
#coding=utf-8
import re
from datetime import datetime
from pymongo import Connection
from datetime import timedelta
from pymongo.errors import ConnectionFailure
_utcnow = datetime.utcnow()

def insertR(dbC, collect, data):
	dbC[collect].insert(data, save=True)


def countIP_URL(logList):
	_ip = {}
	_url = {}
	_ipp = []
	_urll = []
	for n in logList:
		_ipp.append(n.get('ip'))
		_urll.append(n.get('url'))
	for m in _ipp:
		if _ipp.count(m) > 1:
			_ip[m] = _ipp.count(m)
	ip = sorted(_ip.items(), key=lambda _ip:_ip[1], reverse=True)
	print "-----Nginx access IP NUMS in 10 seconds-------"
	for k in ip:
		if k[1] > 30:
			print k[0],':',k[1]
	for i in _urll:
		if _urll.count(i) > 1:
			_url[i] = _urll.count(i)
	url = sorted(_url.items(), key=lambda _url:_url[1], reverse=True)
	print "-----Nginx access url NUMs in 10 seconds-------"
	for j in url:
		if j[1] > 20:
			print j[0],':',j[1]
			
	
	
def getWebLog(host,port,dbname,times):
	''' host: mongodb hostname
		port: mongodb port
		dbname: mongodb database names
		times: times before now to get logs from mongodb,eg:-10
	'''
	try:
		_c1 = Connection(host, port)
	except ConnectionFailure, e:
		sys.stderr.write("Could not connect to MongoDB: %s" % e)
		sys.exit(1)
	dbC = _c1[dbname]
	assert dbC.connection == _c1
	end = _utcnow
	amin = timedelta(seconds=times)
	#amin = timedelta(minutes=-1)
	start = end + amin
	_r1 = dbC.access.find({'time': {'$gte': start, '$lt': end}})
	return _r1
	
	
	
def getLogItems(weblog,*args):
	'''
	get web log items from mongodb
	'''
	_logD = {}
	logIn = []
	logOut = []
	for i in weblog:
		s = ur'192\.168\.10\.'
		if re.match(s,i.get(u'remotehost')):
			if u'path' in i.keys():
				_url1 = i.get(u'host') + i.get(u'path')
				_logD = {u'ip':i['xforwardedhost'],u'url':_url1,u'time':i['time'],u'from':u'192.168.10.111'}
				if len(args):
					for j in args:
						_logD[j] = i.get(j)
					
				logIn.append(_logD)
			else:
				_url1 = i.get(u'host')
				_logD = {u'ip':i['xforwardedhost'],u'url':_url1,u'time':i['time'],u'from':u'192.168.10.111'}
				if len(args):
					for j in args:
						_logD[j] = i.get(j)
				logIn.append(_logD)
		else:
			if u'path' in i.keys():
				_url1 = i.get(u'host') + i.get(u'path')
				_logD = {u'ip':i['remotehost'],u'url':_url1,u'time':i['time']}
				if len(args):
					for j in args:
						_logD[j] = i.get(j)
				logOut.append(_logD)
			else:
				_url1 = i.get(u'host')
				_logD = {u'ip':i['remotehost'],u'url':_url1,u'time':i['time']}
				if len(args):
					for j in args:
						_logD[j] = i.get(j)
				logOut.append(_logD)
	return (logIn,logOut)
		
def main():
	i = getWeblog('localhost',27017,'nginx111',-10)
	m = getLogItems(i,u'method',u'referer',u'code',u'size',u'agent')[1]
	countIP_URL(logOut)
	#c1 = u'nginx111'
	#insertR(dbC, c1, logIn)
	

if __name__ == "__main__":
	main()