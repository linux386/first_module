# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import FinanceDataReader as fdr
import pandas as pd
from bs4 import BeautifulSoup
import datetime as dt
from urllib.request import urlopen

def date_format(d):
    d = str(d).replace('-', '.')
    
    yyyy = int(d.split('.')[0]) 
    mm = int(d.split('.')[1])
    dd = int(d.split('.')[2])

    this_date= dt.date(yyyy, mm, dd)
    return this_date
    
class excel:
    

    def kospi_stock_price(self):
    
        data = pd.read_excel('d:\\kospi_list.xlsx')

        code_list = data['종목코드'].tolist()
        code_list = [str(item).zfill(6) for item in code_list]
        name_list = data['종목명'].tolist()

        # 코스피 상장종목 전체
        stock_dic = dict(list(zip(code_list,name_list)))

        for code in stock_dic.keys():
            df  = fdr.DataReader(code,'2019-01-01')
            print(code,stock_dic[code])
            df['Code'],df['Name'] = code,stock_dic[code]
            df = df[['Code','Name','Open','High','Low','Volume','Close']]
    
            #df.to_excel('d:\\data_set\\kospi\\'+ stock_dic[code] +'.xlsx',engine = 'xlsxwriter')
            print(df)
            
    def kosdaq_stock_price(self, start_date ,end_date):
        self.start_date = start_date
        self.end_date = end_date
        data = pd.read_excel('d:\\kosdaq_list.xlsx')

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
            #df.to_excel('d:\\data_set\\kosdaq\\'+ stock_dic[code] +'.xlsx',engine = 'xlsxwriter')
            print(df)

        
    def get_money_trend(self):
    
        path = 'd:\\money_trend.xlsx'

        url = 'http://finance.naver.com/sise/sise_deposit.nhn?&page='    
        Data = pd.DataFrame(columns = ['고객예탁금', '신용잔고','주식형 펀드','혼합형 펀드','채권형 펀드'])
        date_list = []
    
        # 값을 받을 사전
        dictionary = {'고객예탁금': [],'신용잔고': [],'주식형 펀드': [],'혼합형 펀드': [],'채권형 펀드': []}

        # dictionary key 인덱싱을 위한 리스트
        name_list = ['고객예탁금','신용잔고','주식형 펀드','혼합형 펀드','채권형 펀드']

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
                                    df.to_excel(path, encoding='utf-8')
                                
                                    return df

                            elif count in mask:
                                temp = int((count-1)/2)
                                dictionary[name_list[temp]].append(td.text.strip())
        
                        count += 1
            
                # 누락된 값을 발견하면 (펀드 자료에 누락된 값이 존재함)
                if len(dictionary['고객예탁금']) != len(dictionary['주식형 펀드']):
                    print(str(i)+ '번째 페이지에서 누락된 값 발생')
                    print('누락된 데이터를 제거합니다')
                    
                    date_list.pop(-1)
                    dictionary['고객예탁금'].pop(-1)
                    dictionary['신용잔고'].pop(-1)
               

            print(str(i) + '번째 페이지 크롤링 완료')

    def get_money_trend_date(self,until_date='00-12-27'):
    
        path = 'd:\\money_trend.xlsx'

        url = 'http://finance.naver.com/sise/sise_deposit.nhn?&page='    
        Data = pd.DataFrame(columns = ['고객예탁금', '신용잔고','주식형 펀드','혼합형 펀드','채권형 펀드'])
        date_list = []
    
        # 값을 받을 사전
        dictionary = {'고객예탁금': [],'신용잔고': [],'주식형 펀드': [],'혼합형 펀드': [],'채권형 펀드': []}

        # dictionary key 인덱싱을 위한 리스트
        name_list = ['고객예탁금','신용잔고','주식형 펀드','혼합형 펀드','채권형 펀드']

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
                                    if date_ == until_date or i > 207:
                                        print(str(i-1) + '번째 페이지에서 크롤링 종료')
                                        date_list.pop(-1)
                                        df = pd.DataFrame(dictionary,index = date_list)
                                        df = df.sort_index()
                                        df.to_excel(path, encoding='utf-8')
                                
                                        return df

                            elif count in mask:
                                temp = int((count-1)/2)
                                dictionary[name_list[temp]].append(td.text.strip())
        
                        count += 1
            
                # 누락된 값을 발견하면 (펀드 자료에 누락된 값이 존재함)
                if len(dictionary['고객예탁금']) != len(dictionary['주식형 펀드']):
                    print(str(i)+ '번째 페이지에서 누락된 값 발생')
                    print('누락된 데이터를 제거합니다')
                    
                    date_list.pop(-1)
                    dictionary['고객예탁금'].pop(-1)
                    dictionary['신용잔고'].pop(-1)
                
            print(str(i) + '번째 페이지 크롤링 완료')
            
            
    def get_kpi_200_date(self,until_date='00-12-27'):
    
        path = 'd:\\kpi_200.xlsx'

        Data = pd.DataFrame(columns = ['KPI200','거래량'])
        date_list = []
    
        # 값을 받을 사전
        dictionary = {'KPI200': [],'거래량': []}

        # dictionary key 인덱싱을 위한 리스트
        name_list = ['KPI200','거래량']

        # count mask
        mask = [0,1,5]
    
        for i in range(1,last+3):
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
                                    if date_ == until_date or i > 5:
                                        print(str(i-1) + '번째 페이지에서 크롤링 종료')
                                        date_list.pop(-1)
                                        df = pd.DataFrame(dictionary,index = date_list)
                                        df = df.sort_index()
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
    
    