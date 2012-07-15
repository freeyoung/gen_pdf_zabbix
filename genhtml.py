#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import time
import urllib
tab_nonhtml=ur'^!.*$'

def genhtml(template_name, htmlfile_name, zabbix_url):

    # Init_Session
    urllib.urlretrieve(zabbix_url,"/dev/null")
    
    f = open(template_name,"r")
    html_result=''
    
    for line in f:
        match = re.search(tab_nonhtml, line)
        if match:
            tab_result=match.group()
            html_result+=tab_process(tab_result, zabbix_url)
        else:
            html_result+=line
    f.close()
    
    f = open(htmlfile_name, "w")
    f.write(html_result)
    f.close()
    
    return

def tab_process(tab_result, zabbix_url):
    tab_strings=re.sub(ur'=','',tab_result).split(r'!')
    tab_type=tab_strings[1]
    
    # Type_Graph: '',graph,graph_id,width,stime
    
    if tab_type == 'graph':
        tab_graph_id=num_it(tab_strings[2])
        tab_graph_width=num_it(tab_strings[3])
        tab_graph_period=num_it(tab_strings[4])
        tab_graph_stime=tab_stime(tab_graph_period)
        tab_type_result=r'<br><img src="'+zabbix_url+r'chart2.php?graphid='+tab_graph_id+r'&width='+tab_graph_width+r'&period='+tab_graph_period+r'&stime='+tab_graph_stime+r'"><br>'+'\r\n'
    
    # Type_Notes: Do nothing, just some info in the templates
    
    if tab_type == 'notes':
        tab_type_result=''

    # Type_Another_Type: foo,bar,...
    # We may add more types to be processed here
    
    return tab_type_result
    
def num_it(strArg):
    num_result=re.sub('[a-z]','',strArg)
    return num_result
    
def tab_stime(period):
    stime = time.strftime("%Y%m%d%H%M%S",time.localtime(time.mktime(time.localtime())-int(period)))
    return stime