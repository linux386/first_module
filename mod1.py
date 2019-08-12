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
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
from matplotlib import font_manager, rc
font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
rc('font', family=font_name)

today = datetime.now()
real_yesterday = (today-timedelta(1)).strftime('%Y-%m-%d')
real_today = today.strftime('%Y-%m-%d')

now = dt.datetime.today().strftime('%Y-%m-%d')
engine = sqlalchemy.create_engine('mysql+pymysql://kkang:leaf2027@localhost/stock?charset=utf8',encoding='utf-8')
conn = engine.connect()

class to_report:
    def stock_select_with_Volume_Close(self):
    
        yesterday = input("어제날짜를 입력하세요 : sample: '2019-02-07'  ") or real_yesterday
        today = input("오늘날짜를 입력하세요 : sample: '2019-02-07'  ") or real_today
    
        select_query = "select * from market where Date >="
        volume_query = "&& Volume >  500000"
    
        var = select_query +"'"+yesterday+"'"+ volume_query
        df = pd.read_sql(var ,engine)

        df1 = df[df['Date'].astype(str) == yesterday]
        df1 = df1[['Name','Volume','Close']]
        df1.columns = ['Name','yester_Volume','yester_Close']
        #display(df1)

        df2 = df[df['Date'].astype(str) == today]
        df2 = df2[['Name','Volume','Close']]
        df2.columns = ['Name','today_Volume','today_Close']
        #display(df2)

        df3 = pd.merge(df1,df2,on='Name')
        df3['Close']=df3['today_Close']/df3['yester_Close']
        df3['Volume']=df3['today_Volume']/df3['yester_Volume']
        df3 = df3.sort_values(by=['Volume','Close'],ascending=False)
        df4 = df3.sort_values(by=['Close','Volume'],ascending=False)
        df3 = df3.reset_index(drop=True)

        df3 = df3[:15]
        df4 = df4.reset_index(drop=True)
        df4 = df4[:15]
        display(df3)
        display(df4)

    def get_graph(self):
        graph = input("그래프종류를 입력하세요 sample: 'money' or 'program' or 'stock': ")
        date = input("날짜를 입력하세요 sample: '2019-01-10':") or '2019-01-01'
    
        if graph == 'money' :
            money_name = ['kpi200', '거래량', '고객예탁금', '신용잔고']
            money_query = "select * from kpi_with_money where Date >"+"'"+date+"'"
            money_df = pd.read_sql(money_query ,engine)
        
            money_df.columns=['Date','kpi200', '거래량', '고객예탁금', '신용잔고', '주식형펀드', '혼합형펀드', '채권형펀드']
            money_df = money_df.set_index('Date')
            df1 = money_df[money_name]
            #return df1

            plt.figure(figsize=(16,4))         
            colors = ['red','green','blue','black']
            for i in range(len(money_name)):
                plt.subplot(2,2,i+1)
                plt.plot(df1[money_name[i]]/df1[money_name[i]].loc[money_df.index[0]]*100, color=colors[i])
                plt.legend(loc=0)
                plt.grid(True,color='0.7',linestyle=':',linewidth=1)
                #plt.show()
        
        elif graph == 'program' :
            program_name = ['차익', '비차익', '전체']
            program_query = "select * from programtrend where Date >"+"'"+date+"'"
            program_df = pd.read_sql(program_query ,engine)
    
            program_df.columns=['Date','차익', '비차익', '전체']
            program_df = program_df.set_index('Date')
            df1=program_df[program_name]
            #return df1

            plt.figure(figsize=(16,4))        
            colors = ['red','green','blue','black']
            for i in range(len(program_name)):

                plt.subplot(2,2,i+1)
                plt.plot(df1[program_name[i]],color=colors[i])
        
                plt.legend(loc=0)
                plt.grid(True,color='0.7',linestyle=':',linewidth=1)
                #plt.show()
            
        elif graph == 'stock' :
            name = input('주식이름을 입력하세요:').split()
            #date = input("날짜를 입력하세요 sample: '2019-01-10':")
        
            select_query = "select Date,Volume,Close from market where Name= "
            date_query = "Date > "
    

            tuple_name=tuple(name)
            df1 = pd.DataFrame()
    
            for x in tuple_name:
                var = select_query +"'"+x+"'"+" "+"&&"+" "+date_query+"'"+date+"'"
                df = pd.read_sql(var ,engine)
                df.columns=['Date',x+'거래량',x]
                if df1.empty:
                    df1 = df
                else:
                    df1 = pd.merge (df,df1,on='Date')
            df1=df1.set_index('Date')
            size = len(df1.index)
        
            plt.figure(figsize=(16,4))
            for i in range(len(name)):
                plt.plot(df1[name[i]]/df1[name[i]].loc[df['Date'][0]]*100)
        
                plt.legend(loc=0)
                plt.grid(True,color='0.7',linestyle=':',linewidth=1)

            plt.figure(figsize=(16,4))
            for i in range(len(name)):
                volume_average = df1[name[i]+'거래량'].sum(axis=0)/size
                plt.plot(df1[name[i]+'거래량']/volume_average)
                #plt.plot(df1[name[i]+'거래량']/df1[name[i]+'거래량'].loc[df['Date'][0]]*100, label =[name[i]+'거래량'] )
                plt.legend(loc=0)
                plt.grid(True,color='0.7',linestyle=':',linewidth=1)        

class to_sql:
    
    def excel_to_mysql(self):

        file_name = input('파일이름을 입력하세요:')
        
        df=pd.read_excel('d:\\'+ file_name)
        if file_name=='kpi200.xlsx':
            df.columns=['Date','kpi200','거래량']
            table_name = 'kpi200'
 
        elif file_name=='investortrend.xlsx':
            table_name = 'investortrend'
            df.columns=['Date', '개인', '외국인','기관']
        
        elif file_name=='moneytrend.xlsx':
            table_name = 'moneytrend'
            df.columns=['Date', '고객예탁금', '신용잔고','주식형펀드','혼합형펀드','채권형펀드']
        
        elif file_name=='programtrend.xlsx':
            table_name = 'programtrend'
            df.columns=['Date', '차익', '비차익','전체']
        
        elif file_name=='market.xlsx':
            data = pd.read_excel('d:\\market.xlsx')
            start_date = input("시작날자를 입려하세요 : sample: '2015-01-01'")

            code_list = data['종목코드'].tolist()
            code_list = [str(item).zfill(6) for item in code_list]
            name_list = data['종목명'].tolist()

            # 코스피 상장종목 전체
            stock_dic = dict(list(zip(code_list,name_list)))

            for code in sorted(stock_dic.keys()):
                df  = fdr.DataReader(code,start_date)
                print(code,stock_dic[code])
                df['Code'],df['Name'] = code,stock_dic[code]
                df = df[['Code','Name','Open','High','Low','Volume','Close']]
                df.to_sql(name='market', con=engine, if_exists='append')
            return 
    
        else:
            print('\n file_name error\n')
    
        df.to_sql(name=table_name, con=engine, if_exists='append', index = False)

        print(df)


    def get_stock_price_from_fdr(self, end_date=now):
        
        file_name = input('파일이름을 입력하세요:')
        toward = input('저장 방식을 입력하세요 : sample: excel, sql ')
        start_date = input("시작날자를 입려하세요 : sample: '2015-01-01'")
        table_name = input("table명을 입력하세요 : sample: market")
    
        data=pd.read_excel('d:\\'+ file_name)
   
        code_list = data['종목코드'].tolist()
        code_list = [str(item).zfill(6) for item in code_list]
        name_list = data['종목명'].tolist()

        # 코스피 상장종목 전체
        stock_dic = dict(list(zip(code_list,name_list)))

        for code in sorted(stock_dic.keys()):
            df  = fdr.DataReader(code,start_date,now)
            print(code,stock_dic[code])
            df['Code'],df['Name'] = code,stock_dic[code]
            df = df[['Code','Name','Open','High','Low','Volume','Close']]
            if toward == 'excel':
                df.to_excel('d:\\data_set\\kospi\\'+ stock_dic[code] +'.xlsx',engine = 'xlsxwriter')
            elif toward == 'sql':
                df.to_sql(name=table_name, con=engine, if_exists='append')
        

class to_excel:
    
    def get_investor_trend(self):
        url = 'http://finance.naver.com/sise/investorDealTrendDay.nhn?bizdate=2020601&sosok=&page='

        source = urlopen(url).read()   # 지정한 페이지에서 코드 읽기
        source = BeautifulSoup(source, 'lxml')   # 뷰티풀 스프로 태그별로 코드 분류

        last = source.find('td',class_='pgRR').find('a')['href']
        last = last.split('page')[1]
        last = last.split('=')[1]
        last = int(last)
        print(last)

        # 사용자의 PC내 폴더 주소를 입력하시면 됩니다.
        path = 'd:\\investortrend.xlsx'
    
        # 날짜를 받을 리스트
        date_list = []

        # 값을 받을 사전
        dictionary = {'개인': [],'외국인': [],'기관': []}

        # dictionary key 인덱싱을 위한 리스트
        name_list = ['개인','외국인','기관']


        # count mask
        mask = [1,2,3]
    
        for i in range(1,last+1):
        
            source = urlopen(url+ str(i)).read()
            source = BeautifulSoup(source,'lxml')

            #tbody = source.find('div',{'id':'wrap'}).find('div',{'class':'box_type_m'})
            #trs = tbody.find_all('tr')

            body = source.find('body')
            trs = body.find_all('tr')

            for tr in trs:
                tds = tr.find_all('td',{'class':['date2','rate_down3','rate_up3']})
                count = 0
    
                for td in tds:
                    if count == 0:
                        date_ = td.text.strip().replace('.','-')
                        date_list.append(date_)
                        
                      
                    elif count in mask:
                        temp = int(count-1)
                        dictionary[name_list[temp]].append(td.text.strip().replace(',',''))
        
                    count += 1
                if len(date_list) != len(dictionary['개인']):
                    print(str(i)+ '번째 페이지에서 누락된 값 발생')
                    print('누락된 데이터를 제거합니다')
                    
                    date_list.pop(-1)
                    dictionary['개인'].pop(-1)
                    dictionary['외국인'].pop(-1)
                    dictionary['기관'].pop(-1)
                
        # 개별 list 요소 갯수 파악 
        #print(len(date_list))
        #print(len(dictionary['개인']))
        #print(len(dictionary['외국인']))
        #print(len(dictionary['기관']))

        print(str(i) + '번째 페이지 크롤링 완료')
        df = pd.DataFrame(dictionary,index = date_list)
        df = df.sort_index()
        df.to_excel(path, encoding='utf-8')
        print(df)
        
    def get_investor_trend_date(self,until_date='2000-12-27'):
    
        url = 'http://finance.naver.com/sise/investorDealTrendDay.nhn?bizdate=2020601&sosok=&page='

        source = urlopen(url).read()   # 지정한 페이지에서 코드 읽기
        source = BeautifulSoup(source, 'lxml')   # 뷰티풀 스프로 태그별로 코드 분류

        last = source.find('td',class_='pgRR').find('a')['href']
        last = last.split('page')[1]
        last = last.split('=')[1]
        last = int(last)
        print(last)

        # 사용자의 PC내 폴더 주소를 입력하시면 됩니다.
        path = 'd:\\investortrend.xlsx'

        until_date = input("날짜를 입력하세요 sample: '2019-01-10': ")
    
        year = until_date.split('-')[0]
        mm = until_date.split('-')[1]
        dd = until_date.split('-')[2]
        year=year[2:]
        until_date = year+'-'+mm+'-'+dd
    
        # 날짜를 받을 리스트
        date_list = []

        # 값을 받을 사전
        dictionary = {'개인': [],'외국인': [],'기관': []}

        # dictionary key 인덱싱을 위한 리스트
        name_list = ['개인','외국인','기관']


        # count mask
        mask = [1,2,3]
    
        for i in range(1,last+1):
        
            source = urlopen(url+ str(i)).read()
            source = BeautifulSoup(source,'lxml')

            #tbody = source.find('div',{'id':'wrap'}).find('div',{'class':'box_type_m'})
            #trs = tbody.find_all('tr')

            body = source.find('body')
            trs = body.find_all('tr')

            for tr in trs:
                tds = tr.find_all('td',{'class':['date2','rate_down3','rate_up3']})
                count = 0
    
                for td in tds:
                    if count == 0:
                        date_ = td.text.strip().replace('.','-')
                        if date_ <=  until_date :
                            df = pd.DataFrame(dictionary,index = date_list)
                            df = df.sort_index()
                            df.to_excel(path, encoding='utf-8')
                            return df   
                        date_list.append(date_)
                        #print(date_list)
                    elif count in mask:
                        temp = int(count-1)
                        dictionary[name_list[temp]].append(td.text.strip().replace(',',''))
                    
                    count += 1
    
    def get_moneytrend(self):
    
        url = 'http://finance.naver.com/sise/sise_deposit.nhn?&page='

        source = urlopen(url).read()   # 지정한 페이지에서 코드 읽기
        source = BeautifulSoup(source, 'lxml')   # 뷰티풀 스프로 태그별로 코드 분류

        last = source.find('td',class_='pgRR').find('a')['href']
        last = last.split('&')[1]
        last = last.split('=')[1]
        last = int(last)

        # 사용자의 PC내 폴더 주소를 입력하시면 됩니다.
        path = 'd:\\moneytrend.xlsx'   
    
        # 날짜를 받을 리스트
        date_list = []

        # 값을 받을 사전
        dictionary = {'고객예탁금': [],'신용잔고': [],'주식형 펀드': [],'혼합형 펀드': [],'채권형 펀드': []}

        # dictionary key 인덱싱을 위한 리스트
        name_list = ['고객예탁금','신용잔고','주식형 펀드','혼합형 펀드','채권형 펀드']


        # count mask
        mask = [1,3,5,7,9]
    
        for i in range(1,last+1):
        
            source = urlopen(url+ str(i)).read()
            source = BeautifulSoup(source,'lxml')

            #tbody = source.find('div',{'id':'wrap'}).find('div',{'class':'box_type_m'})
            #trs = tbody.find_all('tr')

            body = source.find('body')
            trs = body.find_all('tr')

            for tr in trs:
                tds = tr.find_all('td',{'class':['date','rate_down','rate_up']})
                count = 0
    
                for td in tds:
                    if count == 0:
                        date_ = td.text.strip().replace('.','-')
                        date_list.append(date_)
                        
                      
                    elif count in mask:
                        temp = int((count-1)/2)
                        dictionary[name_list[temp]].append(td.text.strip().replace(',',''))
        
                    count += 1
                if len(dictionary['고객예탁금']) != len(dictionary['채권형 펀드']):
                    print(str(i)+ '번째 페이지에서 누락된 값 발생')
                    print('누락된 데이터를 제거합니다')
                    
                    date_list.pop(-1)
                    dictionary['고객예탁금'].pop(-1)
                    dictionary['신용잔고'].pop(-1)
                    dictionary['주식형 펀드'].pop(-1)
                    dictionary['혼합형 펀드'].pop(-1)
                
        # 개별 list 요소 갯수 파악 
        #print(len(date_list))
        #print(len(dictionary['고객예탁금']))
        #print(len(dictionary['신용잔고']))
        #print(len(dictionary['주식형 펀드']))
        #print(len(dictionary['혼합형 펀드']))
        #print(len(dictionary['채권형 펀드']))
        print(str(i) + '번째 페이지 크롤링 완료')
        df = pd.DataFrame(dictionary,index = date_list)
        df = df.sort_index()
        df.to_excel(path, encoding='utf-8')
        print(df)

    def get_moneytrend_date(self,until_date='2000-12-27'):
        
        url = 'http://finance.naver.com/sise/sise_deposit.nhn?&page='

        source = urlopen(url).read()   # 지정한 페이지에서 코드 읽기
        source = BeautifulSoup(source, 'lxml')   # 뷰티풀 스프로 태그별로 코드 분류

        last = source.find('td',class_='pgRR').find('a')['href']
        last = last.split('&')[1]
        last = last.split('=')[1]
        last = int(last)

        # 사용자의 PC내 폴더 주소를 입력하시면 됩니다.
        path = 'd:\\moneytrend.xlsx'

    
        until_date = input("날짜를 입력하세요 sample: '2019-01-10': ") or real_today
    
        year = until_date.split('-')[0]
        mm = until_date.split('-')[1]
        dd = until_date.split('-')[2]
        year=year[2:]
        until_date = year+'-'+mm+'-'+dd
    
        #df = DataFrame(columns = ['고객예탁금', '신용잔고','주식형 펀드','혼합형 펀드','채권형 펀드'])

        # 날짜를 받을 리스트
        date_list = []

    
        # 값을 받을 사전
        dictionary = {'고객예탁금': [],'신용잔고': [],'주식형 펀드': [],'혼합형 펀드': [],'채권형 펀드': []}

        # dictionary key 인덱싱을 위한 리스트
        name_list = ['고객예탁금','신용잔고','주식형 펀드','혼합형 펀드','채권형 펀드']


        # count mask
        mask = [1,3,5,7,9]
    
        for i in range(1,last+1):
        
            source = urlopen(url+ str(i)).read()
            source = BeautifulSoup(source,'lxml')

            #tbody = source.find('div',{'id':'wrap'}).find('div',{'class':'box_type_m'})
            #trs = tbody.find_all('tr')

            body = source.find('body')
            trs = body.find_all('tr')

            for tr in trs:
                tds = tr.find_all('td',{'class':['date','rate_down','rate_up']})
                count = 0
    
                for td in tds:
                    if count == 0:
                        date_ = td.text.strip().replace('.','-')
                        if date_ <=  until_date :
                        #if date_ <=  '19-03-05' :
                            df = pd.DataFrame(dictionary,index = date_list)
                            df = df.sort_index()
                            df.to_excel(path, encoding='utf-8')
                            return df
                        date_list.append(date_)
                    
                    elif count in mask:
                        temp = int((count-1)/2)
                        dictionary[name_list[temp]].append(td.text.strip().replace(',',''))
                
       
                    count += 1
            
            
    def get_kpi200(self):
        
        url = 'https://finance.naver.com/sise/sise_index_day.nhn?code=KPI200&page='

        source = urlopen(url).read()   # 지정한 페이지에서 코드 읽기
        source = BeautifulSoup(source, 'lxml')   # 뷰티풀 스프로 태그별로 코드 분류

        last = source.find('td',class_='pgRR').find('a')['href']
        last = last.split('page')[1]
        last = last.split('=')[1]
        last = int(last)
        print(last)

        # 사용자의 PC내 폴더 주소를 입력하시면 됩니다.
        path = 'd:\\kpi200.xlsx'
    
        # 날짜를 받을 리스트
        date_list = []

        # 값을 받을 사전
        dictionary = {'KPI200': [],'거래량': []}

        # dictionary key 인덱싱을 위한 리스트
        name_list = ['KPI200','거래량']


        # count mask
        mask = [1,3]
    
        for i in range(1,last+1):
        
            source = urlopen(url+ str(i)).read()
            source = BeautifulSoup(source,'lxml')

            #tbody = source.find('div',{'id':'wrap'}).find('div',{'class':'box_type_m'})
            #trs = tbody.find_all('tr')

            body = source.find('body')
            trs = body.find_all('tr')

            for tr in trs:
                tds = tr.find_all('td',{'class':['date','number_1']})
                count = 0
    
                for td in tds:
                    if count == 0:
                        date_ = td.text.strip().replace('.','-')
                        date_list.append(date_)
                        
                      
                    elif count in mask:
                        temp = int(count/3)
                        dictionary[name_list[temp]].append(td.text.strip().replace(',',''))
        
                    count += 1
                if len(date_list) != len(dictionary['KPI200']):
                    print(str(i)+ '번째 페이지에서 누락된 값 발생')
                    print('누락된 데이터를 제거합니다')
                    
                    date_list.pop(-1)
                    dictionary['KPI200'].pop(-1)
                    dictionary['거래량'].pop(-1)
                
        # 개별 list 요소 갯수 파악 
        #print(len(date_list))
        #print(len(dictionary['개인']))
        #print(len(dictionary['외국인']))
        #print(len(dictionary['기관']))

        print(str(i) + '번째 페이지 크롤링 완료')
        df = pd.DataFrame(dictionary,index = date_list)
        df = df.sort_index()
        df.to_excel(path, encoding='utf-8')
        print(df)
       

    def get_kpi200_date(self,until_date='2000-12-27'):
    
        url = 'https://finance.naver.com/sise/sise_index_day.nhn?code=KPI200&page='

        source = urlopen(url).read()   # 지정한 페이지에서 코드 읽기
        source = BeautifulSoup(source, 'lxml')   # 뷰티풀 스프로 태그별로 코드 분류

        last = source.find('td',class_='pgRR').find('a')['href']
        last = last.split('page')[1]
        last = last.split('=')[1]
        last = int(last)
        print(last)

        # 사용자의 PC내 폴더 주소를 입력하시면 됩니다.
        path = 'd:\\kpi200.xlsx'

        until_date = input("날짜를 입력하세요 sample: '2019-01-10': ") or real_today
    
        year = until_date.split('-')[0]
        mm = until_date.split('-')[1]
        dd = until_date.split('-')[2]
        #year=year[2:]
        until_date = year+'-'+mm+'-'+dd
    
        # 날짜를 받을 리스트
        date_list = []

        # 값을 받을 사전
        dictionary = {'KPI200': [],'거래량': []}

        # dictionary key 인덱싱을 위한 리스트
        name_list = ['KPI200','거래량']


        # count mask
        mask = [1,3]
    
        for i in range(1,last+1):
        
            source = urlopen(url+ str(i)).read()
            source = BeautifulSoup(source,'lxml')

            #tbody = source.find('div',{'id':'wrap'}).find('div',{'class':'box_type_m'})
            #trs = tbody.find_all('tr')

            body = source.find('body')
            trs = body.find_all('tr')

            for tr in trs:
                tds = tr.find_all('td',{'class':['date','number_1']})
                count = 0
    
                for td in tds:
                    if count == 0:
                        date_ = td.text.strip().replace('.','-')
                        if date_ <=  until_date :
                        #if date_ <=  '19-03-05' :
                            df = pd.DataFrame(dictionary,index = date_list)
                            df = df.sort_index()
                            df.to_excel(path, encoding='utf-8')
                            return df   
                        date_list.append(date_)
                        #print(date_list)
                    elif count in mask:
                        temp = int(count/3)
                        dictionary[name_list[temp]].append(td.text.strip().replace(',',''))
                        #print(dictionary[name_list[temp]])
                    count += 1
                    
                    
    def get_program_trend(self):
    
        url = 'https://finance.naver.com/sise/programDealTrendDay.nhn?bizdate=20200315&sosok=&page='

        source = urlopen(url).read()   # 지정한 페이지에서 코드 읽기
        source = BeautifulSoup(source, 'lxml')   # 뷰티풀 스프로 태그별로 코드 분류

        last = source.find('td',class_='pgRR').find('a')['href']
        last = last.split('page')[1]
        last = last.split('=')[1]
        last = int(last)
        print(last)

        # 사용자의 PC내 폴더 주소를 입력하시면 됩니다.
        path = 'd:\\programtrend.xlsx'
    
        # 날짜를 받을 리스트
        date_list = []

        # 값을 받을 사전
        dictionary = {'차익': [],'비차익': [],'전체': []}

        # dictionary key 인덱싱을 위한 리스트
        name_list = ['차익','비차익','전체']


        # count mask
        mask = [3,6,9]
    
        for i in range(1,last+1):
        
            source = urlopen(url+ str(i)).read()
            source = BeautifulSoup(source,'lxml')

            #tbody = source.find('div',{'id':'wrap'}).find('div',{'class':'box_type_m'})
            #trs = tbody.find_all('tr')

            body = source.find('body')
            trs = body.find_all('tr')

            for tr in trs:
                tds = tr.find_all('td',{'class':['date','rate_down','rate_up']})
                count = 0
    
                for td in tds:
                    if count == 0:
                        date_ = td.text.strip().replace('.','-')
                        date_list.append(date_)
                        
                      
                    elif count in mask:
                        temp = int((count/3)-1)
                        dictionary[name_list[temp]].append(td.text.strip().replace(',',''))
        
                    count += 1
                if len(date_list) != len(dictionary['전체']):
                    print(str(i)+ '번째 페이지에서 누락된 값 발생')
                    print('누락된 데이터를 제거합니다')
                    
                    date_list.pop(-1)
                    dictionary['차익'].pop(-1)
                    dictionary['비차익'].pop(-1)
                    #dictionary['전체'].pop(-1)
                
        # 개별 list 요소 갯수 파악 
        print(len(date_list))
        print(len(dictionary['차익']))
        print(len(dictionary['비차익']))
        print(len(dictionary['전체']))

        print(str(i) + '번째 페이지 크롤링 완료')
        df = pd.DataFrame(dictionary,index = date_list)
        df = df.sort_index()
        df.to_excel(path, encoding='utf-8')
        print(df)
            
    def get_program_trend_date(self,until_date='2000-12-27'):
    
        url = 'https://finance.naver.com/sise/programDealTrendDay.nhn?bizdate=20200315&sosok=&page='

        source = urlopen(url).read()   # 지정한 페이지에서 코드 읽기
        source = BeautifulSoup(source, 'lxml')   # 뷰티풀 스프로 태그별로 코드 분류

        last = source.find('td',class_='pgRR').find('a')['href']
        last = last.split('page')[1]
        last = last.split('=')[1]
        last = int(last)
        print(last)

        # 사용자의 PC내 폴더 주소를 입력하시면 됩니다.
        path = 'd:\\programtrend.xlsx'

        until_date = input("날짜를 입력하세요 sample: '2019-01-10': ")
    
        year = until_date.split('-')[0]
        mm = until_date.split('-')[1]
        dd = until_date.split('-')[2]
        year=year[2:]
        until_date = year+'-'+mm+'-'+dd
    
        # 날짜를 받을 리스트
        date_list = []

        # 값을 받을 사전
        dictionary = {'차익': [],'비차익': [],'전체': []}

        # dictionary key 인덱싱을 위한 리스트
        name_list = ['차익','비차익','전체']


        # count mask
        mask = [3,6,9]
    
        for i in range(1,last+1):
        
            source = urlopen(url+ str(i)).read()
            source = BeautifulSoup(source,'lxml')

            #tbody = source.find('div',{'id':'wrap'}).find('div',{'class':'box_type_m'})
            #trs = tbody.find_all('tr')

            body = source.find('body')
            trs = body.find_all('tr')

            for tr in trs:
                tds = tr.find_all('td',{'class':['date','rate_down','rate_up']})
                count = 0
    
                for td in tds:
                    if count == 0:
                        date_ = td.text.strip().replace('.','-')
                        if date_ <=  until_date :
                            df = pd.DataFrame(dictionary,index = date_list)
                            df = df.sort_index()
                            df.to_excel(path, encoding='utf-8')
                            return df   
                        date_list.append(date_)
                        #print(date_list)
                    elif count in mask:
                        temp = int((count/3)-1)
                        dictionary[name_list[temp]].append(td.text.strip().replace(',',''))
                    
                    count += 1
            
            

if __name__ == "__main__":
    print("This is Module")
    
    
