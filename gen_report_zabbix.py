#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import ConfigParser
import genpdf
import genhtml
import genmail
import time

if len(sys.argv) < 2 or len(sys.argv) > 3:
    option = 'help'
else:
    if sys.argv[1].startswith('--'):
        option = sys.argv[1][2:]
    else:
        option = 'help'

# fetch sys.argv[1] but without the first two characters
if option == 'version':   
    print 'Version 0.1'
    sys.exit()
elif option == 'config':
    config_file=sys.argv[2]
else:
# Other unknown options, such as "--help"
    print '''
    This program can generate and send report of Zabbix via email with PDF.
    
    Options include:
    --config filename : Send email report according to options in config file
    --version : Prints the version number
    --help : Display this help
    
    Written in Python 2.7, by Eric.Qian'''
    sys.exit()

cf = ConfigParser.ConfigParser()
cf.read(config_file)

# cf.sections: [zabbix], [email]...
# cf.options("zabbix"): [zabbix_url, report_template...]
# cf.items("email"):  [('smtp_server', 'smtp.163.com'), ('smtp_user', 'blcu0804@163.com'), ...]
# cf.get=[string], cf.getint=int...
# cf.set("zabbix", "zabbix_url", "http://www.baidu.com/")  
# cf.write(open(config_file, "w")) 

zabbix_url = cf.get("zabbix", "zabbix_url")
report_template = cf.get("zabbix", "report_template")

smtp_server=cf.get("email","smtp_server")
smtp_user=cf.get("email","smtp_user")
smtp_pass=cf.get("email","smtp_pass")
from_add=cf.get("email","from_add")
to_add=cf.get("email","to_add").split(',')
subject=cf.get("email","subject")
htmlText=cf.get("email","htmlText")
att_name=cf.get("email","att_name")

current_time=time.localtime()

htmlfile_name = att_name+time.strftime("%Y%m%d%H%M%S",current_time)+r'.html'
pdffile_name = att_name+time.strftime("%Y%m%d%H%M%S",current_time)+r'.pdf'

genhtml.genhtml(report_template, htmlfile_name, zabbix_url)
genpdf.genpdf(htmlfile_name, pdffile_name)

authInfo={}
authInfo['server'] = smtp_server
authInfo['user'] = smtp_user
authInfo['password'] = smtp_pass

genmail.sendEmail(authInfo, from_add, to_add, subject, '', htmlText, pdffile_name)