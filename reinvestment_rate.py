# ---------------------------------------------------------------------------------------------------------------------------------------
# 體質評估: 採IFRS後的財報, 計算出盈再率
# 1. 盈再率＜40%，即為低再盈率，通常是體質不錯的好公司。
# 2. 盈再率＞80%，偏高，不適合投資。
# 3. 盈再率＞200%，極可能是潛在地雷股（公司遭掏空），如已下市的電子公司博達、陞技，爆發財務危機前就有此徵兆。
# source: http://smart.businessweekly.com.tw/Reading/WebArticle.aspx?id=38494
# ---------------------------------------------------------------------------------------------------------------------------------------
import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
print('')
print('體質評估: 採IFRS後的財報, 計算出盈再率')
print('1. 盈再率＜40%，即為低再盈率，通常是體質不錯的好公司。')
print('2. 盈再率＞80%，偏高，不適合投資。')
print('3. 盈再率＞200%，極可能是潛在地雷股（公司遭掏空），如已下市的電子公司博達、陞技，爆發財務危機前就有此徵兆。')
print('------------------------------------------------------------------------------------------------------------------')
stock_num = input('Please enter the stock number (ex, 2330): ')
input_season = input('Please enter the season (ex, 1-4): ')
print('------------------------------------------------------------------------------------------------------------------')

stock_num = int(stock_num)
input_year = 108
input_season = int(input_season)

def get_the_sum_of_the_last_4years_NI(input_year,stock_num):
    NI_list = []
    NI_value =[]
    NI_flag = 0
    NIvalue = 0
    NI_sum = 0
    NI_count = 0
    for y in range(input_year-1,input_year-6,-3):
        #print(y)
        url = 'https://mops.twse.com.tw/mops/web/ajax_t163sb17'
        payload = {'encodeURIComponent': 1,'step': 1,'firstin': 1,'off': 1,'queryName': 'co_id','t05st29_c_ifrs': 'N','t05st30_c_ifrs': 'N','inpuType': 'co_id','TYPEK': 'all','isnew': 'false','co_id': stock_num,'year': y}
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
        list_req = requests.post(url, data = payload, headers = headers)
        soup = BeautifulSoup(list_req.content,'lxml')
        #print(soup.prettify())
        #print(soup.text)
        soup = soup.find_all(["th", "td"])
        #print(soup)
        for x in soup:
            #print(x.string)
            if x.string == '本期淨利（淨損）':
                NI_flag = 1
            elif x.string == '其他綜合損益（淨額）':
                NI_flag = 0
            elif NI_flag == 1:
                #print(td_tag.string)
                NI_list.append(x.string)
            else:
                if x.string == '其他綜合損益（淨額）':
                    break
        #print(NI_list)
        #print(len(NI_list))
        for n in range(0,len(NI_list)):
            NIvalue = NI_list[n].lstrip()
            NIvalue = NIvalue.replace('\'','')
            NIvalue = NIvalue.replace(',','')
            #print(NIvalue)
            NIvalue = int(NIvalue)
            NI_count = NI_count + 1
            if NI_count < 4:
                #print(NI_count)
                #print(NIvalue)
                NI_value.append(NIvalue)
                NI_sum = NI_sum + NIvalue
            elif NI_count == 4:
                NIvalue = NI_list[2].lstrip()
                NIvalue = NIvalue.replace('\'','')
                NIvalue = NIvalue.replace(',','')
                #print(NI_count)
                #print(NIvalue)
                NI_sum = NI_sum + int(NIvalue)
        NI_flag = 0
        NI_list_num = 0
        NI_list = []
    return float(NI_sum)



def get_total_non_current_assets(input_year,stock_num,input_season):
    non_current_assets = []
    assets_list = []
    tdflag = 0
    for y in range(input_year,input_year-8,-4):
        #print(y)
        url = 'https://mops.twse.com.tw/mops/web/ajax_t164sb03'
        payload = {'encodeuricomponent': 1,'step': 1,'firstin': 1,'off': 1,'queryname': 'co_id','t05st29_c_ifrs': 'n','t05st30_c_ifrs': 'n','inputype': 'co_id','typek': 'all','isnew': 'false','co_id': stock_num,'year': y, 'season': input_season}
        headers = {'user-agent':'mozilla/5.0 (windows nt 10.0; win64; x64) applewebkit/537.36 (khtml, like gecko) chrome/78.0.3904.108 safari/537.36'}
        list_req = requests.post(url, data = payload, headers = headers)
        soup = BeautifulSoup(list_req.content,'lxml')
        # print(soup.prettify())
        # print(soup.text)
        td_label = soup.find_all('td')
        for td_tag in td_label:
            if td_tag.string == '　　非流動資產合計':
                tdflag = 1
            elif td_tag.string == '　資產總額':
                tdflag = 0
            elif tdflag == 1:
                #print(td_tag.string)
                non_current_assets.append(td_tag.string)
            else:
                if td_tag.string == '　資產總額':
                    break
        #print(non_current_assets)
        assets = non_current_assets[0].lstrip()
        assets = assets.replace(',','')
        assets = int(assets)
        assets_list.append(assets)
        #print(assets)
        #print(type(assets))
        tdflag = 0
        non_current_assets = []
    #print(assets_list)
    calculate = ((assets_list[0]-assets_list[1]))
    #print(assets_list[0])
    #print(assets_list[1])
    QOY = float(calculate)
    return QOY

QOY = get_total_non_current_assets(input_year,stock_num,input_season)
calculate = QOY / get_the_sum_of_the_last_4years_NI(input_year,stock_num)
calculate = calculate*100
calculate = round(calculate,3)
print('')
print('近四年的稅後淨利總和: ',get_the_sum_of_the_last_4years_NI(input_year,stock_num))
print('近四年的非流動資產合計: ',QOY)
print('------------------------------------------------------')
if calculate < 40.0:
    print('盈再率為: ',calculate,'% Good!')
elif (calculate > 40.0) and (calculate < 80.0):
    print('盈再率為: ',calculate,'% 尚可!')
elif (calculate > 80.0):
    print('盈再率為: ',calculate,'% 偏高!')
elif (calculate > 200.0):
    print('盈再率為: ',calculate,'% 極可能是潛在地雷股!')
print('------------------------------------------------------')


























#def get_the_sum_of_the_last_4years_eps():
#    eps_sum = 0
#    eps_count = 0
#    for y in range(107,101,-3):
#        # print(y)
#        url = 'https://mops.twse.com.tw/mops/web/ajax_t163sb17'
#        payload = {'encodeURIComponent': 1,'step': 1,'firstin': 1,'off': 1,'queryName': 'co_id','t05st29_c_ifrs': 'N','t05st30_c_ifrs': 'N','inpuType': 'co_id','TYPEK': 'all','isnew': 'false','co_id': 2330,'year': y}
#        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
#        list_req = requests.post(url, data = payload, headers = headers)
#        soup = BeautifulSoup(list_req.content,'lxml')
#        # print(soup.prettify())
#        # print(soup.text)
#        soup = soup.select('table')[1]
#        # print(soup.text)
#        df = pd.read_html(str(soup))[0]
#        df = df.rename(columns={'Unnamed: 0':'Item'})
#        # print(df)
#        row_num = len(df)
#        row_start = row_num-1
#        row_end = row_num
#        eps_list = df.iloc[row_start:row_end,1:] 
#        # print(eps_list)
#        col_num = eps_list.size
#        for num in range(1,col_num+1):
#            eps_buf = df.iloc[row_start:row_end,num]
#            eps_buf = float(eps_buf)
#            #print(eps_buf)
#            eps_count  = eps_count + 1
#            if eps_count <= 4:
#                #print(eps_count)
#                eps_sum = eps_sum + eps_buf
#        #print('----------------------------------------------------------------------------------------------------------')
#        print(eps_sum)
#        print('----------------------------------------------------------------------------------------------------------')
#        return(eps_sum)
