#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  1 15:38:07 2018

@author: sumkumar
"""

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
from datetime import datetime
#https://github.com/dancingcactus/python-omniture/issues/59
import omniture
import sys
import schedule
from slackclient import SlackClient
from gsheet import gc



def useless_sleep():
    time.sleep(2) #to be removed on production
    
    
#################getting Omniture data for current day
def Omnituredata():
    analytics = omniture.authenticate('', '')
    suite = analytics.suites['']
    query = suite.report \
        .element('listvar1',disable_validation=True) \
        .metric('instances',disable_validation=True) \
        .range(start = '2018-05-03', stop = "2018-05-06") \
        .run()
    return query

x = True
def job(query):
    query=query
    global x
    
    try:
        query.dataframe
    except ValueError:
        l = False
    else:
        l = True
        
    if l == True:
        x = False
        print(query.dataframe)
        sc = SlackClient('')
        #sc.api_call('chat.postMessage',channel='#boomdata-alerts',text=tabulate(query.dataframe, tablefmt='grid'))
        sc.api_call('chat.postMessage',channel='#boomdata-alerts',text=repr(query.dataframe))
        #sys.exit()

def postOmnitureData():
    global x
    schedule.clear() 
    query=Omnituredata()   
    schedule.every(10).seconds.do(job,query)

    while x:
        schedule.run_pending()
        time.sleep(1)
    

################# visit the page in a headless version of firefox
#options = Options()
start_time=datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

def test_runner(desired_cap_list,big_dict,target_url_list,wks,bs_local):
    #while q.empty() is False:
                
        for elem in desired_cap_list:
            desired_cap=elem
            print('Browser : {} ,Version :{}'.format(elem['browser'],elem['browser_version']))
            #options.add_argument("--headless")
            

            browser= webdriver.Remote(command_executor='http://hub.browserstack.com:80/wd/hub',desired_capabilities=desired_cap)
            import navigation
            import validations
            for target_url in target_url_list: 
                target_url=target_url[0]
                
                
                navigation.homepageNavigate(target_url,browser)
                validations.validate(browser,big_dict,desired_cap,target_url.replace('pwa', ''),wks)
                
                domain=target_url.replace('pwa', '')
                
                
                navigation.hsrNavigate(domain,browser)
                validations.validate(browser,big_dict,desired_cap,domain,wks)
                
                navigation.hisNavigate(domain,browser)
                validations.validate(browser,big_dict,desired_cap,domain,wks)
                
                
            browser.quit()
            
        
         #stop the Local instance
        bs_local.stop()    
        
        
        from validations import flag
        
        wks_local = gc.open("BoomAudit").worksheet('PWA Browsers & POSa')
        length_browsers=len(wks_local.col_values(1))-2
        
        #wks_local = gc.open("BoomAudit").worksheet('PWA POSa')
        length_posa=len(wks_local.col_values(6))-1
        
        wks = gc.open("BoomAudit").worksheet('PWA Logs')
        passed_num=length_browsers*length_posa*3
        
        print('flag: {}, passed_num : {}'.format(flag,passed_num))
        if flag==passed_num:
            date=datetime.now().strftime("%Y-%m-%d")
            hour=datetime.now().strftime("%H")
            browser_version_os=''
            sites=''
            for elem in desired_cap_list:
                browser_version_os+='Browser: {} Version: {} OS: {} ,'.format(elem['browser'],elem['browser_version'],elem['os'])
            for target_url in target_url_list: 
                sites+='{},'.format(target_url[0])
            gsheet_values=[date,hour,browser_version_os,sites,'All Pages','Yay! All Good' ,'','','PASSED',browser.session_id]
            wks.insert_row(gsheet_values, index=2, value_input_option='RAW')
    # =============================================================================
    #         driver.quit()
    #         time.sleep(15)
    # =============================================================================
        #browser.quit()    
        #q.task_done()
