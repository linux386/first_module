# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import FinanceDataReader as fdr
import pandas as pd
import datetime as dt
from urllib.request import urlopen  
import bs4

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

        
    def kpi_200(self,index_cd, start_date='', end_date= '', page_n=1, last_page=0):
        
        historical_prices = dict()
        index_cd = 'KPI200'
        page_n = 1
        naver_index = 'http://finance.naver.com/sise/sise_index_day.nhn?code=' + index_cd + '&page=' + str(page_n)
        
        self.start_date = start_date
        self.end_date = end_date
        
        if start_date:  # start_date가 있으면
            start_date = date_format(start_date)   # date 포맷으로 변환
        else:    # 없으면
            start_date = dt.date.today()   # 오늘 날짜를 지정
        if end_date:   
            end_date = date_format(end_date)   
        else:   
            end_date = dt.date.today()  
        
        
        naver_index = 'http://finance.naver.com/sise/sise_index_day.nhn?code=' + index_cd + '&page=' + str(page_n)
    
        source = urlopen(naver_index).read()   # 지정한 페이지에서 코드 읽기
        source = bs4.BeautifulSoup(source, 'lxml')   # 뷰티풀 스프로 태그별로 코드 분류
    
        dates = source.find_all('td', class_='date')   # <td class="date">태그에서 날짜 수집   
        prices = source.find_all('td', class_='number_1')   # <td class="number_1">태그에서 지수 수집
    
        for n in range(len(dates)):
    
            if dates[n].text.split('.')[0].isdigit():
            
                # 날짜 처리
                this_date = dates[n].text
                this_date= date_format(this_date)
            
                if this_date <= end_date and this_date >= start_date:   
                # start_date와 end_date 사이에서 데이터 저장
                    # 종가 처리
                    this_close = prices[n*4].text   # prices 중 종가지수인 0,4,8,...번째 데이터 추출
                    this_close = this_close.replace(',', '')
                    this_close = float(this_close)

                    # 딕셔너리에 저장
                    historical_prices[this_date] = this_close
                
                elif this_date < start_date:   
                    # start_date 이전이면 함수 종료
                    return historical_prices              
            
        # 페이지 네비게이션
        if last_page == 0:
            last_page = source.find('td', class_='pgRR').find('a')['href']
            # 마지막페이지 주소 추출
            last_page = last_page.split('&')[1]   # & 뒤의 page=506 부분 추출
            last_page = last_page.split('=')[1]   # = 뒤의 페이지번호만 추출
            last_page = int(last_page)   # 숫자형 변수로 변환
        
        #다음 페이지 호출
        if page_n < last_page:   
               page_n = page_n + 1   
               self.(index_cd, start_date='', end_date= '', page_n=1, last_page=0)  
        
        return historical_prices  
        print(historical_prices)

