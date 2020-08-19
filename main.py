    #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 22 12:51:22 2018

@author: sumkumar
"""
import fast_selenium
from common import postOmnitureData
#postOmnitureData()
import gsheet 
from common import start_time
from common import datetime
from common import test_runner
from browserstack.local import Local



#creates an instance of Local
bs_local = Local()

#replace <browserstack-accesskey> with your key. You can also set an environment variable - "BROWSERSTACK_ACCESS_KEY".
bs_local_args = { "key": "", "forcelocal": "true" }

#starts the Local instance with the required arguments
bs_local.start(**bs_local_args)

#check if BrowserStack local instance is running
print (bs_local.isRunning())

big_dict=gsheet.big_dict
gc=gsheet.gc
wks = gc.open("BoomAudit").worksheet('PWA Logs')

#print(big_dict)
desired_cap_list=[]

browser_list_array=big_dict.get('browsers')
for browser_list in browser_list_array:
    desired_cap_list.append({
    'browser': browser_list[0],
     'browser_version': browser_list[1],
     'os': browser_list[2],
     'os_version': browser_list[3],
     'resolution': '1024x768',
     'browserstack.user':'boomdata1',
     'browserstack.key':'WqSrT5NKGWyznbKc6gZz',
     #'browserstack.local':'true',
     'name':'BoomAudit',
     'acceptSslCerts':True
    })

posa_list=big_dict.get('posa')
print(big_dict) 
# =============================================================================
# import sys 
# sys.exit()
# =============================================================================
test_runner(desired_cap_list,big_dict,posa_list,wks,bs_local)

end_time=datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
tdelta = datetime.strptime(end_time, '%Y-%m-%d-%H-%M-%S') - datetime.strptime(start_time, '%Y-%m-%d-%H-%M-%S')  
print(tdelta)     
                



#references :
#https://bytes.com/topic/python/answers/781432-how-create-list-dictionaries
