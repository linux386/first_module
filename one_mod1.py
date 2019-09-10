# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import FinanceDataReader as fdr
import pandas as pd
from bs4 import BeautifulSoup
import datetime as dt
from datetime import datetime,timedelta
from urllib.request import urlopen
import sqlalchemy 
import pymysql
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
rc('font', family=font_name)

now = dt.datetime.today().strftime('%Y-%m-%d')
engine = sqlalchemy.create_engine('mysql+pymysql://kkang:leaf2027@localhost/stock?charset=utf8',encoding='utf-8')
conn = engine.connect()

def stock_select_with_Volume_Close():
    
    yesterday = input("어제날짜를 입력하세요 : sample: '2019-02-07 00:00:00'  ") 
    today = input("오늘날짜를 입력하세요 : sample: '2019-02-07 00:00:00'  ")
    
    select_query = "select * from market where Date >="
    volume_query = "&& Volume >  500000"
    
    var = select_query +"'"+yesterday+"'"+ volume_query
    df = pd.read_sql(var ,engine)

    df1 = df[df['Date'] == yesterday]
    df1 = df1[['Name','Volume','Close']]
    df1.columns = ['Name','yester_Volume','yester_Close']
    #display(df1)

    df2 = df[df['Date'] == today]
    df2 = df2[['Name','Volume','Close']]
    df2.columns = ['Name','today_Volume','today_Close']
    #display(df2)

    df3 = pd.merge(df1,df2,on='Name')
    df3['Close']=df3['today_Close']/df3['yester_Close']
    df3['Volume']=df3['today_Volume']/df3['yester_Volume']
    df3 = df3.sort_values(by=['Volume','Close'],ascending=False)
    df3 = df3.reset_index(drop=True)
    df3 = df3[:10]
    df4 = df3.sort_values(by=['Close','Volume'],ascending=False)
    df4 = df4.reset_index(drop=True)
    df4 = df4[:10]
    display(df3)
    display(df4)

def stock_price_graph():
    
    name = input('주식이름을 입력하세요:').split()
    date = input("날짜를 입력하세요 sample: '2019-01-10':")
    #table= input('write table name:')
    
    select_query = "select DATE(Date),Close from market where Name= "
    date_query = "Date > "
    

    #print("\n")
    tuple_name=tuple(name)
    df1 = pd.DataFrame()
    
    for x in tuple_name:
        #print(x)
        
        var = select_query +"'"+x+"'"+" "+"&&"+" "+date_query+"'"+date+"'"
        #print(var)
        df = pd.read_sql(var ,engine)
        df.columns=['Date',x]
        if df1.empty:
            df1 = df
        else:
            df1 = pd.merge (df,df1,on='Date')
    df1=df1.set_index('Date')
    #first_date = date_format(df['Date'][0])
    plt.figure(figsize=(12,5))
    for i in range(len(name)):
        plt.plot(df1[name[i]]/df1[name[i]].loc[df['Date'][0]]*100)
        #plt.plot(df1[name[1]]/df1[name[1]].loc[dt.date(2017,1,2)]*100)
    plt.legend(loc=0)
    plt.grid(True,color='0.7',linestyle=':',linewidth=1)   


def excel_to_mysql():
    file_name = input('파일이름을 입력하세요:')
        
    df=pd.read_excel('d:\\'+ file_name)
    df.index.name='Date'
    df.to_sql(name=file_name, con=engine, if_exists='append')
    return df


def get_stock_price_from_fdr(end_date=now):
        
    file_name = input('파일이름을 입력하세요:')
    toward = input('저장 방식을 입력하세요 : sample: excel, sql ')
    start_date = input("시작날자를 입려하세요 : sample: '2015-01-01'")
    data=pd.read_excel('d:\\'+ file_name)
   
    code_list = data['종목코드'].tolist()
    code_list = [str(item).zfill(6) for item in code_list]
    name_list = data['종목명'].tolist()

    # 코스피 상장종목 전체
    stock_dic = dict(list(zip(code_list,name_list)))

    for code in stock_dic.keys():
        df  = fdr.DataReader(code,start_date,end_date)
        print(code,stock_dic[code])
        df['Code'],df['Name'] = code,stock_dic[code]
        df = df[['Code','Name','Open','High','Low','Volume','Close']]
        if toward == 'excel':
            df.to_excel('d:\\data_set\\kospi\\'+ stock_dic[code] +'.xlsx',engine = 'xlsxwriter')
        elif toward == 'sql':
            df.to_sql(name=market, con=engine, if_exists='append')
        print(df)


class to_excel:
    
    def get_money_trend(self):
    
        path = 'd:\\money_trend.xlsx'

        url = 'http://finance.naver.com/sise/sise_deposit.nhn?&page='    
        Data = pd.DataFrame(columns = ['고객예탁금', '신용잔고','주식형펀드','혼합형펀드','채권형펀드'])
        date_list = []
    
        # 값을 받을 사전
        dictionary = {'고객예탁금': [],'신용잔고': [],'주식형펀드': [],'혼합형펀드': [],'채권형펀드': []}

        # dictionary key 인덱싱을 위한 리스트
        name_list = ['고객예탁금','신용잔고','주식형펀드','혼합형펀드','채권형펀드']

        # count mask
        mask = [0,1,3,5,7,9]
    
        for i in range(1,300):
            source = urlopen(url+ str(i)).read()
            source = BeautifulSoup(source,'lxml')

            tbody = source.find('div',{'id':'wrap'}).find('div',{'class':'box_type_m'})
            trs = tbody.find_all('tr')
            for tr in trs:
                tds = tr.find_all('td')
                count = 0
    
                for td in tds:
                    # 변화량 제외하고 잔고량만 가져오기
                    if not td.text.strip() == 0:
                        if len(td.text.strip()) >= 4:
            
                            if count == 0:
                                date_ = td.text.strip().replace('.','-')
                        
                                if not date_ in date_list:
                                    date_list.append(date_)
                        
                                #마지막 페이지인 경우
                                else:
                                    print(str(i-1) + '번째 페이지에서 크롤링 종료')
                                
                                    df = pd.DataFrame(dictionary,index = date_list)
                                    df = df.sort_index()
                                    df.고객예탁금 = df.고객예탁금.str.replace(',','')
                                    df.신용잔고 = df.신용잔고.str.replace(',','')
                                    df.주식형펀드 = df.주식형펀드.str.replace(',','')
                                    df.혼합형펀드 = df.혼합형펀드.str.replace(',','')
                                    df.채권형펀드 = df.채권형펀드.str.replace(',','')
                                    df.to_excel(path, encoding='utf-8')
                                
                                    return df

                            elif count in mask:
                                temp = int((count-1)/2)
                                dictionary[name_list[temp]].append(td.text.strip())
        
                        count += 1
            
                # 누락된 값을 발견하면 (펀드 자료에 누락된 값이 존재함)
                if len(dictionary['고객예탁금']) != len(dictionary['주식형펀드']):
                    print(str(i)+ '번째 페이지에서 누락된 값 발생')
                    print('누락된 데이터를 제거합니다')
                    
                    date_list.pop(-1)
                    dictionary['고객예탁금'].pop(-1)
                    dictionary['신용잔고'].pop(-1)
               

            print(str(i) + '번째 페이지 크롤링 완료')

    def get_money_trend_date(self,until_date='2000-12-27'):
        
        year = until_date.split('-')[0]
        mm = until_date.split('-')[1]
        dd = until_date.split('-')[2]
        year=year[2:]
        until_date = year+'-'+mm+'-'+dd
    
        path = 'd:\\money_trend.xlsx'
        print(path)

        url = 'http://finance.naver.com/sise/sise_deposit.nhn?&page='    
        Data = pd.DataFrame(columns = ['고객예탁금', '신용잔고','주식형펀드','혼합형펀드','채권형펀드'])
        date_list = []
    
        # 값을 받을 사전
        dictionary = {'고객예탁금': [],'신용잔고': [],'주식형펀드': [],'혼합형펀드': [],'채권형펀드': []}

        # dictionary key 인덱싱을 위한 리스트
        name_list = ['고객예탁금','신용잔고','주식형펀드','혼합형펀드','채권형펀드']

        # count mask
        mask = [0,1,3,5,7,9]
    
        for i in range(1,300):
            source = urlopen(url+ str(i)).read()
            source = BeautifulSoup(source,'lxml')

            tbody = source.find('div',{'id':'wrap'}).find('div',{'class':'box_type_m'})
            trs = tbody.find_all('tr')
            for tr in trs:
                tds = tr.find_all('td')
                count = 0
    
                for td in tds:
                    # 변화량 제외하고 잔고량만 가져오기
                    if not td.text.strip() == 0:
                        if len(td.text.strip()) >= 4:
            
                            if count == 0:
                                date_ = td.text.strip().replace('.','-')
                        
                                if not date_ in date_list :
                                    date_list.append(date_)
                        
                                #마지막 페이지인 경우
                                    if date_ <= until_date or i > 3:
                                        print(str(i-1) + '번째 페이지에서 크롤링 종료')
                                        date_list.pop(-1)
                                        df = pd.DataFrame(dictionary,index = date_list)
                                        df = df.sort_index()
                                        df.고객예탁금 = df.고객예탁금.str.replace(',','')
                                        df.신용잔고 = df.신용잔고.str.replace(',','')
                                        df.주식형펀드 = df.주식형펀드.str.replace(',','')
                                        df.혼합형펀드 = df.혼합형펀드.str.replace(',','')
                                        df.채권형펀드 = df.채권형펀드.str.replace(',','')
                                        df.to_excel(path, encoding='utf-8')
                                
                                        return df

                            elif count in mask:
                                temp = int((count-1)/2)
                                dictionary[name_list[temp]].append(td.text.strip())
        
                        count += 1
            
                # 누락된 값을 발견하면 (펀드 자료에 누락된 값이 존재함)
                if len(dictionary['고객예탁금']) != len(dictionary['주식형펀드']):
                    print(str(i)+ '번째 페이지에서 누락된 값 발생')
                    print('누락된 데이터를 제거합니다')
                    
                    date_list.pop(-1)
                    dictionary['고객예탁금'].pop(-1)
                    dictionary['신용잔고'].pop(-1)
                
            print(str(i) + '번째 페이지 크롤링 완료')
            
    def get_kpi_200(self,until_date='1995-12-27'):
    
        path = 'd:\\kpi_200.xlsx'
        
        url = 'https://finance.naver.com/sise/sise_index_day.nhn?code=KPI200&page='
        Data = pd.DataFrame(columns = ['KPI200','거래량'])
        date_list = []
    
        # 값을 받을 사전
        dictionary = {'KPI200': [],'거래량': []}

        # dictionary key 인덱싱을 위한 리스트
        name_list = ['KPI200','거래량']

        # count mask
        mask = [0,1,5]
    
        for i in range(1,700):
            source = urlopen(url+ str(i)).read()
            source = BeautifulSoup(source,'lxml')

            tbody = source.find('div',{'class':'box_type_m'})
            trs = tbody.find_all('tr')
            for tr in trs:
                tds = tr.find_all('td')
                count = 0
    
                for td in tds:
                    # 변화량 제외하고 잔고량만 가져오기
                    if not td.text.strip() == 0:
                        if len(td.text.strip()) >= 4:
            
                            if count == 0:
                                date_ = td.text.strip().replace('.','-')
                        
                                if not date_ in date_list :
                                    date_list.append(date_)
                                    
                                #마지막 페이지인 경우
                                else:
                                    print(str(i-1) + '번째 페이지에서 크롤링 종료')
                                    df = pd.DataFrame(dictionary,index = date_list)
                                    df = df.sort_index()
                                    df.거래량 = df.거래량.str.replace(',','')
                                    df.to_excel(path, encoding='utf-8')
                                
                                    return df

                            elif count in mask:
                                temp = int(count/5)
                                dictionary[name_list[temp]].append(td.text.strip())
                                
                        #print(count)
                        count += 1
            
                # 누락된 값을 발견하면 (펀드 자료에 누락된 값이 존재함)
                if len(dictionary['KPI200']) != len(dictionary['거래량']):
                    print(str(i)+ '번째 페이지에서 누락된 값 발생')
                    print('누락된 데이터를 제거합니다')
                    
                    date_list.pop(-1)
                    dictionary['KPI200'].pop(-1)
                    dictionary['거래량'].pop(-1)
                
            print(str(i) + '번째 페이지 크롤링 완료')
            
            
    def get_kpi_200_date(self,until_date='1995-12-27'):
    
        path = 'd:\\kpi_200.xlsx'
        
        url = 'https://finance.naver.com/sise/sise_index_day.nhn?code=KPI200&page='
        Data = pd.DataFrame(columns = ['KPI200','거래량'])
        date_list = []
    
        # 값을 받을 사전
        dictionary = {'KPI200': [],'거래량': []}

        # dictionary key 인덱싱을 위한 리스트
        name_list = ['KPI200','거래량']

        # count mask
        mask = [0,1,5]
    
        for i in range(1,700):
            source = urlopen(url+ str(i)).read()
            source = BeautifulSoup(source,'lxml')

            tbody = source.find('div',{'class':'box_type_m'})
            trs = tbody.find_all('tr')
            for tr in trs:
                tds = tr.find_all('td')
                count = 0
    
                for td in tds:
                    # 변화량 제외하고 잔고량만 가져오기
                    if not td.text.strip() == 0:
                        if len(td.text.strip()) >= 4:
            
                            if count == 0:
                                date_ = td.text.strip().replace('.','-')
                        
                                if not date_ in date_list :
                                    date_list.append(date_)
                                    
                                    #마지막 페이지인 경우
                                    if date_ <= until_date or i > 3:
                                        print(str(i-1) + '번째 페이지에서 크롤링 종료')
                                        date_list.pop(-1)
                                        df = pd.DataFrame(dictionary,index = date_list)
                                        df = df.sort_index()
                                        df.거래량 = df.거래량.str.replace(',','')
                                        df.to_excel(path, encoding='utf-8')
                                
                                        return df

                            elif count in mask:
                                temp = int(count/5)
                                dictionary[name_list[temp]].append(td.text.strip())
                                
                        #print(count)
                        count += 1
            
                # 누락된 값을 발견하면 (펀드 자료에 누락된 값이 존재함)
                if len(dictionary['KPI200']) != len(dictionary['거래량']):
                    print(str(i)+ '번째 페이지에서 누락된 값 발생')
                    print('누락된 데이터를 제거합니다')
                    
                    date_list.pop(-1)
                    dictionary['KPI200'].pop(-1)
                    dictionary['거래량'].pop(-1)
                
            print(str(i) + '번째 페이지 크롤링 완료')
            

if __name__ == "__main__":
    print("This is Module")
    
    