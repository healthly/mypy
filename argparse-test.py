#!/usr/bin/env python
#coding=utf-8
import re
from datetime import datetime
from pymongo import Connection
from datetime import timedelta
from pymongo.errors import ConnectionFailure


import argparse
parser = argparse.ArgumentParser(description='analy nginx log from mongodb')

parser.add_argument('-H', dest="dbhost" , help="mongodb's ip or hostname")
#parser.add_argument('-N', dest="dbname", type=int)

args = parser.parseargs()