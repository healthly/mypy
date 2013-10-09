#!/usr/bin/env python
#encoding=utf-8
from urllib2 import build_opener,HTTPCookieProcessor
from sys import argv
from gzip import GzipFile
from StringIO import StringIO

def Decompress(compressed_webcode):#解压函数
	#clen=float(len(compressed_webcode))
	fo=StringIO(compressed_webcode)
	gzip=GzipFile(fileobj=fo)
	try:
		webcode=gzip.read()
	except:
		webcode=compressed_webcode
	return webcode
	#dlen=len(webcode)
	#return "compress rate:%f"%(clen/dlen*100)

def GetWebcode(url):#获取经过压缩的网页源码
	opener=build_opener(HTTPCookieProcessor())
	opener.addheaders=[("Accept-Language","zh-CN"),
			("Accept-Encoding","gzip, deflate"),
			#告知服务器发送经gzip压缩过的网页源码
			("User-Agent","Mozilla/4.0 (compatible; "+
			"MSIE 6.0; Windows NT 5.1; SV1)")]
	return opener.open(url).read()

if __name__=="__main__":
	url=argv[1]
	print Decompress(GetWebcode(url))
