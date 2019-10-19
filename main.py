from urllib.request import Request
import requests
from bs4 import BeautifulSoup
import numpy as np
import re
import ast
import pandas as pd
import datetime
from openpyxl.workbook import workbook

url = 'https://steamcommunity.com/market/listings/730/MP7%20%7C%20Mischief%20%28Minimal%20Wear%29'
r= requests.get(url)
html_doc=r.text
soup = BeautifulSoup(html_doc,'html.parser')
body = str(soup.find('body'))


pattern = re.compile(r'var line1=.*;')
matches = pattern.finditer(body)

x = []


for match in matches: 
    phrase = match.group(0)
    finalPattern = re.compile(r'\[.*\]')
    finalMatch = finalPattern.finditer(phrase)
    for match1 in finalMatch:
        x=ast.literal_eval(match1.group(0))
    

colNames = pd.Index(['Date Time','Price','Units Sold'])
df = pd.DataFrame(data=x, columns=colNames)

#unitsSold = CalculateCut()
df['Units Sold']=df.apply(lambda row: float(row['Units Sold']), axis =1)
df['Cut']=df.apply(lambda row: row['Price']* row['Units Sold']*0.15, axis =1)
df['Date Time']=df.apply(lambda row : datetime.datetime.strptime(row['Date Time'],'%b %d %Y %H: +0'),axis= 1)

filteredDateDf = df[df['Date Time'] > pd.Timestamp('2019-04-13 00:00:00')]
filteredDateDf = df[df['Date Time'] < pd.Timestamp('2019-05-13 23:00:00')]
#filteredDateDf = filteredDateDf[filteredDateDf['Date Time'] < datetime.datetime(2019,4,13,23,59,59)]
# for item in df.keys():
#     item['Cut'] = item['Price']* float(item['Units Sold'])*0.15
#filteredDateDf.loc['Total']= pd.Series(filteredDateDf['Price'].sum(), index=['Price'])
filteredDateDf.at['Total', 'Price'] = filteredDateDf['Price'].sum()
filteredDateDf.at['Total', 'Cut'] = filteredDateDf['Cut'].sum()
filteredDateDf.at['Total', 'Units Sold'] = filteredDateDf['Units Sold'].sum()
# filteredDateDf.loc['Total']= pd.Series(filteredDateDf['Units Sold'].sum(), index=['Units Sold'])
# filteredDateDf.loc['Total']= pd.Series(filteredDateDf['Cut'].sum(), index=['Cut'])
#df['Cut']= CalculateCut()
with pd.ExcelWriter('MP7Mischief.xlsx') as writer:
    filteredDateDf.to_excel(writer , sheet_name = 'MP7 | Mischief') 

print(df)
