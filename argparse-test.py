#!/usr/bin/env python
#coding=utf-8
import re
from datetime import datetime
from pymongo import Connection
from datetime import timedelta
from pymongo.errors import ConnectionFailure


import argparse
parser = argparse.ArgumentParser(description='analy nginx log from mongodb')

parser.add_argument('-H', dest="dbhost", default='localhost', help="mongodb's ip or hostname")
parser.add_argument('-N', dest="dbname", default='nginx111', help="mongodb's dbname")
parser.add_argument('--ipurlnums', dest="ipurlnums", action='store_true', help="output ip and urls")
parser.add_argument('--int', dest='types', action='append_const', const=int)
#parser.add_argument('-N', dest="dbname", type=int)

args = parser.parse_args()