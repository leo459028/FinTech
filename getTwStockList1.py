import pandas as pd

def getstocklist(stksite):
    df=pd.read_html(stksite,encoding='big5hkscs',header=0)
    newdf=df[0][df[0]['產業別'] > '0']
    del newdf['國際證券辨識號碼(ISIN Code)'],newdf['CFICode'],newdf['備註']
    newdf_no=newdf['有價證券代號及名稱'].str.split('　', expand=True) #全形才可以
    newdf_no = newdf_no.reset_index(drop=True)
    newdf = newdf.reset_index(drop=True)
    for i in newdf_no.index:
        if '　' in newdf_no.iat[i,0]:
            newdf_no.iat[i,1]=newdf_no.iat[i,0].split('　')[1]
            newdf_no.iat[i,0]=newdf_no.iat[i,0].split('　')[0]
    newdf=newdf_no.join(newdf)
    newdf=newdf.rename(columns = {0:'股票代號',1:'股票名稱'})
    del newdf['有價證券代號及名稱']
    return newdf

newdf1=getstocklist('http://isin.twse.com.tw/isin/C_public.jsp?strMode=2')
newdf2=getstocklist('http://isin.twse.com.tw/isin/C_public.jsp?strMode=4')
newdfok=pd.concat([newdf1,newdf2],keys='股票代號')
newdfok=newdfok.sort_values(by='股票代號')
newdfok.to_excel('c:\\pyexport\getTwStocklist.xlsx', sheet_name='Sheet1',index=False)
