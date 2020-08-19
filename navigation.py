#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  1 15:03:25 2018

@author: sumkumar
"""

from common import time
#from common import browser
from datetime import datetime,timedelta

################# This will set up the pwa cookie and palogstore cookie and reload the page  
 
def homepageNavigate(target_url,browser):
    browser=browser
    time.sleep(3)
    browser.get(target_url)
    time.sleep(5)
    #browser.execute_script("document.cookie = 'pwa=true; expires=Thu, 18 Dec 20150 12:00:00 UTC; domain=/';")
    browser.execute_script("document.cookie = 'pwa=true';")
    time.sleep(5)
    browser.execute_script("document.cookie = 'paLogStore=true';")
    time.sleep(5)
    #browser.execute_script("return (document.cookie);")
    target_url=target_url.replace('pwa', 'hotels')
    print()
    print(target_url)
    browser.get(target_url)
    

################# This will navigate the HSR  
def hsrNavigate(domain,browser):
    #sentData = getSentData()
    #print(sentData)
    #time.sleep(10)
    trip_start_date=(datetime.now() + timedelta(days=60)).strftime("%Y-%m-%d")
    trip_end_date=(datetime.now() + timedelta(days=61)).strftime("%Y-%m-%d")
    if((domain.find('.com'))<0 or (domain.find('wotif'))>=0 ):
        trip_start_date=(datetime.now() + timedelta(days=60)).strftime("%d/%m/%Y")
        trip_end_date=(datetime.now() + timedelta(days=61)).strftime("%d/%m/%Y")
    target_url='''{}Hotel-Search?adults=2&amenities=&destination=London%2C%20England%2C%20United%20Kingdom&endDate={}&latLong=51.507538%2C-0.127804&lodging=&price=&regionId=178279%20&selected=&sort=recommended&startDate={}&travelerDisplayText=1%20room%2C%202%20guests&x_pwa=1'''.format(domain,trip_end_date, trip_start_date)
    browser.get(target_url)
    
################# This will navigate the HSR  
def hisNavigate(domain,browser):
    #time.sleep(10)
    trip_start_date=(datetime.now() + timedelta(days=60)).strftime("%m/%d/%Y")
    trip_end_date=(datetime.now() + timedelta(days=61)).strftime("%m/%d/%Y")
    
    if((domain.find('.com'))<0 or (domain.find('wotif'))>=0 ):
        trip_start_date=(datetime.now() + timedelta(days=60)).strftime("%d/%m/%Y")
        trip_end_date=(datetime.now() + timedelta(days=61)).strftime("%d/%m/%Y")
    target_url='''{}The-Kensington-Hotel.h18561.Hotel-Information?chkin={}&chkout={}&regionId=178279&destination=London+%28and+vicinity%29%2C+England%2C+United+Kingdom&rm1=a2&x_pwa=1&top_dp=237&top_cur=USD&rfrr=HSR&pwa_ts=1525587549351'''.format(domain,trip_start_date,trip_end_date )
    browser.get(target_url)


        