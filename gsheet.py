#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  8 14:31:27 2018

@author: sumkumar
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  8 14:24:00 2018

@author: sumkumar
"""
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('C:\BoomAudit\Boom_Audit-242553955108.json', scope)

gc = gspread.authorize(credentials)
big_dict={}
wks = gc.open("BoomAudit").worksheet('PWA Pages')

#getting the variables
col1=wks.col_values(1, value_render_option='FORMATTED_VALUE')
col2=wks.col_values(2, value_render_option='FORMATTED_VALUE')
col3=wks.col_values(3, value_render_option='FORMATTED_VALUE')
big_dict['Homepage']=[list(a) for a in zip(col1, col2, col3)]
del big_dict['Homepage'][0]
del big_dict['Homepage'][0]


#getting the variables
col5=wks.col_values(5, value_render_option='FORMATTED_VALUE')
col6=wks.col_values(6, value_render_option='FORMATTED_VALUE')
col7=wks.col_values(7, value_render_option='FORMATTED_VALUE')
big_dict['page.Hotel-Search']=[list(a) for a in zip(col5, col6, col7)]
del big_dict['page.Hotel-Search'][0]
del big_dict['page.Hotel-Search'][0]

#getting the variables
col9=wks.col_values(9, value_render_option='FORMATTED_VALUE')
col10=wks.col_values(10, value_render_option='FORMATTED_VALUE')
col11=wks.col_values(11, value_render_option='FORMATTED_VALUE')
big_dict['page.Hotels.Infosite.Information']=[list(a) for a in zip(col9, col10, col11)]
del big_dict['page.Hotels.Infosite.Information'][0]
del big_dict['page.Hotels.Infosite.Information'][0]

wks = gc.open("BoomAudit").worksheet('PWA Browsers & POSa')
#getting the browsers 
col1=wks.col_values(1, value_render_option='FORMATTED_VALUE')
col2=wks.col_values(2, value_render_option='FORMATTED_VALUE')
col3=wks.col_values(3, value_render_option='FORMATTED_VALUE')
col4=wks.col_values(4, value_render_option='FORMATTED_VALUE')
big_dict['browsers']=[list(a) for a in zip(col1, col2, col3,col4)]
del big_dict['browsers'][0]
del big_dict['browsers'][0]


#getting the POSa
col6=wks.col_values(6, value_render_option='FORMATTED_VALUE')
big_dict['posa']=[list(a) for a in zip(col6)]
del big_dict['posa'][0]

print(big_dict)

#print(big_dict)

#getting the valida

#wks.update_acell('E2', "down there somewhere, let me take another look.")


#https://developers.google.com/sheets/api/quickstart/python
#https://github.com/burnash/gspread
#http://gspread.readthedocs.io/en/latest/#main-interface
#http://gspread.readthedocs.io/en/latest/oauth2.html
#https://docs.google.com/spreadsheets/d/1e5eLD19n09xw8Sa_5s2xRhDlkg0UfzInWfNEuSzN254/edit#gid=0