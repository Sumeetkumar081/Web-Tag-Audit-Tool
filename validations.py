#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  9 09:39:04 2018

@author: sumkumar
"""
from common import time
import re
import http.client as httplib
from datetime import datetime
flag=0

################# Below code block starts defining the Omniture XML body
xml='''<?xml version="1.0" encoding="UTF-8"?><request>
     <scXmlVer>1.0</scXmlVer>
     <reportSuiteID></reportSuiteID> 
     <visitorID>169</visitorID> 
     <ipAddress>192.168.234.11</ipAddress> 
     <user_agent>python_audit</user_agent>
     '''

################# This will fetch the last Omniture request from console #############  
def getSentData(browser):
    browser=browser
    time.sleep(2)
    #sentData = browser.execute_script("return (paLogStore.filter(item => item.publisher === 'Adobe Analytics').filter(item => item.eventType === 'load')[(paLogStore.filter(item => item.publisher === 'Adobe Analytics').filter(item => item.eventType === 'load')).length-1].sentData)")
    sentData = browser.execute_script("return (paLogStore.filter(function(item){ return item.publisher === 'Adobe Analytics'; }).filter(function(item) { return item.eventType === 'load'; })[paLogStore.filter(function(item){ return item.publisher === 'Adobe Analytics'; }).filter(function(item) { return item.eventType === 'load'; }).length-1].sentData)")
    browser.execute_script('console.log("{}")'.format(str(sentData)))
    return sentData

def validate(browser,big_dict,desired_cap,domain,wks):
        sentData = getSentData(browser)
        #print(sentData)
        #print(big_dict)
        browser_original=browser
        page_list_array=big_dict.get(sentData.get('pageName'))
        xml_local=''
        omn_req=''
        list1=''
        request_vars=[]
        mandatory_vars=[]
        date=datetime.now().strftime("%Y-%m-%d")
        hour=datetime.now().strftime("%H")
        browser=desired_cap.get('os')+' '+desired_cap.get('os_version')+' '+desired_cap.get('browser')+' '+desired_cap.get('browser_version')
        #length=len(wks.col_values(1))
        for page_list in page_list_array:
            mandatory_vars.append(page_list[0])
            for k,v in sentData.items():
                request_vars.append(k)
                if page_list[0].lower()==k.lower():
                    omn_req +="<{}>'{}' ~~ {} '{}'</{}>".format(k,v,page_list[1],page_list[2],k)
                    if page_list[1]=='Equals' :
                        v=str(v)
                        if page_list[2].lower()!=v.lower():
                            list1 +='| {} mismatch'.format(k)
                            gsheet_values=[date,hour,browser,domain,sentData.get('pageName'),'{} mismatch'.format(k),v,'{} {}'.format(page_list[1],page_list[2]),'FAILED',browser_original.session_id]
# =============================================================================
#                             print(gsheet_values)
#                             import sys
#                             sys.exit()
# =============================================================================
                            wks.insert_row(gsheet_values, index=2, value_input_option='RAW')
                    elif page_list[1]=='Regex' :
                         regex=r'{}'.format(page_list[2])
# =============================================================================
#                          print(regex)
#                          print(v)
                         v=str(v)
# =============================================================================
                         if not (re.match(regex,v)): 
                             list1 +='| {} mismatch'.format(k)
                             gsheet_values=[date,hour,browser,domain,sentData.get('pageName'),'{} mismatch'.format(k),v,'{} {}'.format(page_list[1],page_list[2]),'FAILED',browser_original.session_id]
                             wks.insert_row(gsheet_values, index=2, value_input_option='RAW')
                            
        #set operations : https://www.geeksforgeeks.org/python-set-operations-union-intersection-difference-symmetric-difference/           
        missing_vars_list=list(set(mandatory_vars) - set(request_vars))
        for missing_vars in missing_vars_list:
            list1 +='| {} is missing'.format(missing_vars)
            gsheet_values=[date,hour,browser,domain,sentData.get('pageName'),'{} is missing'.format(missing_vars),'','','FAILED',browser_original.session_id]
            wks.insert_row(gsheet_values, index=2, value_input_option='RAW')
            
        omn_req+='<list1>{}</list1>'.format(list1)
        xml_local=xml+'{} </request>'.format(omn_req)
        #print(xml_local)
        print(list1)
        if list1=='':
            global flag
            flag= flag+1
            print (flag)
            
        
# =============================================================================
#         import sys
#         sys.exit()
# =============================================================================
        try:
            conn = httplib.HTTPConnection("reportSuiteID.112.2o7.net")
            conn.request("POST", "/b/ss//6",xml_local )
            print('xml sent')
        except:
            pass