{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "import FinanceDataReader as fdr\n",
    "import pandas as pd\n",
    "from datetime import datetime\n",
    "\n",
    "class kospi_stock_price_to_excel:\n",
    "    \n",
    "    data = pd.read_excel('d:\\\\kospi_list.xlsx')\n",
    "\n",
    "    code_list = data['종목코드'].tolist()\n",
    "    code_list = [str(item).zfill(6) for item in code_list]\n",
    "    name_list = data['종목명'].tolist()\n",
    "\n",
    "    # 코스피 상장종목 전체\n",
    "    stock_dic = dict(list(zip(code_list,name_list)))\n",
    "\n",
    "    for code in stock_dic.keys():\n",
    "        df  = fdr.DataReader(code,'2019-01-01')\n",
    "        print(code,stock_dic[code])\n",
    "        df['Code'],df['Name'] = code,stock_dic[code]\n",
    "        df = df[['Code','Name','Open','High','Low','Volume','Close']]\n",
    "    \n",
    "        #df.to_excel('d:\\\\data_set\\\\kospi\\\\'+ stock_dic[code] +'.xlsx',engine = 'xlsxwriter')\n",
    "        print(df)\n",
    "\n",
    "        \n",
    "\n",
    "\n",
    "if __name__ == __main()__:\n",
    "    print('it is module !')"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.6.8"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
