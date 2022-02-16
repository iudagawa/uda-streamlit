'''
 スクレイピング
'''
from bs4 import BeautifulSoup
import requests
import pandas as pd

import gspread
from google.oauth2.service_account import Credentials

import altair as alt
import streamlit as st

import datetime
from gspread_dataframe import set_with_dataframe

def get_data_udem():
    url = 'https://scraping-for-beginner.herokuapp.com/udemy'
    res = requests.get(url)
    #res.text
    soup = BeautifulSoup(res.text,'html.parser')

    temp = soup.find('p',{'class':'subscribers'}).text
    tt = temp.split('：')
    n_subscriber = int(tt[1])
    

    temp = soup.find('p',{'class':'reviews'}).text
    tt = temp.split('：')
    n_review = int(tt[1])
    
    return{
        'n_subscriber':n_subscriber,
        'n_review':n_review
    }


def main():
    worksheet = get_worksheet()
    data = worksheet.get_all_values()      #[[],[]…]　形式で取得
    df = pd.DataFrame(data[1:],columns=data[0])

    #追加する情報
    dict_data = get_data_udem()
    today1 = datetime.datetime.today()
    today1  #出力＞datetime.datetime(2022, 2, 9, 12, 8, 31, 36013)
    today2 = today1.strftime('%Y/%m/%d')
    dict_data['date'] = today2
    
    d_count = df[ df['date'] == today2 ].count()['date']    #同じ日付が既にあるか確認 　date のみのカウント値 
    if d_count==0:
        df = df.append( dict_data, ignore_index=True)
        
    set_with_dataframe(worksheet, df, row=1, col=1)


def get_df_ec():
    '''
        udemyサイトから登録者数とレビュー数を取得する関数
        返り値:pandas dataframe型
    '''
    url_ec = 'https://scraping.official.ec/'
    res = requests.get(url_ec)
    soup = BeautifulSoup(res.text,'html.parser')

    item_list = soup.find('ul',{'id':'itemList'})       #idはallにしなくていい！
    items = item_list.find_all('li') #だけでいい！！

    data_ec =[]

    for item in items:
        datum = {}    
        
        title = item.find('p', {'class': 'items-grid_itemTitleText_5a0255a1'}).text
        datum['title'] = title
        
        #価格取得
        price = item.find('p',{'class':'items-grid_price_5a0255a1'}).text
        price = int(price.replace('¥','').replace(',',''))
        datum['price'] = price
        
        #URL取得
        link = item.find('a')['href']
        datum['link'] = link
        
        #在庫確認
        is_stock = item.find('p',{'class':'items-grid_soldOut_5a0255a1'}) == None
        is_stock = '在庫あり' if is_stock == True else '在庫なし'
        datum['is_stock'] = is_stock
        
        #print('is_stock=',is_stock)
        #print('link=',link)
        #print('price=',price)
        
        data_ec.append(datum)

    #print(data_ec)  [{'price':1000,'link':'URL','is_stock':'在庫あり'},・・・]
    
    return( pd.DataFrame(data_ec) )


def get_worksheet():
    scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]

    credentials = Credentials.from_service_account_file(
        #'./udemy_streamlit/service_account.json',
        'service_account.json',
         scopes=scopes
    )

    gc = gspread.authorize(credentials)    
        
    #Googleドライブに保存したシートファイルのURLを取得
    #https://docs.google.com/spreadsheets/d/1KCCK_CvtwMLtEauShY2bJSAU5yeZlw9QKR2mtEWlV9Q/edit?usp=sharing
    #Google Drive API と Google Sheet APIの認証を有効化し秘密キーを（jsonファイル）を取得した時に
    
    #記載されているclient_emailを【共有】
    #service_account.json
    #"client_email": "udemy-20220207@serious-music-336206.iam.gserviceaccount.com",

    SP_SHEET_KEY = '1KCCK_CvtwMLtEauShY2bJSAU5yeZlw9QKR2mtEWlV9Q'

    sh = gc.open_by_key(SP_SHEET_KEY)        
    
    SP_SHEET = 'db' #シート名
    worksheet = sh.worksheet(SP_SHEET)
            
    return worksheet

def get_chart():
    worksheet = get_worksheet()
    data = worksheet.get_all_values()      #[[],[]…]　形式で取得
    df_udemy = pd.DataFrame(data[1:],columns=data[0])
    df_udemy = df_udemy.astype({
    'n_subscriber':int,
    'n_review':int,
    })

    ymin1 = df_udemy.n_subscriber.min() -10
    ymax1 = df_udemy.n_subscriber.max() +10

    ymin2 = df_udemy.n_review.min() - 10
    ymax2 = df_udemy.n_review.max() + 10
    
    #X軸（共通）
    base = alt.Chart(df_udemy).encode(
        alt.X('date:T', axis=alt.Axis(title='日付'))
    )

    #Y1軸　
    line1 = base.mark_line(opacity=0.3, color='#57A44C').encode(
        alt.Y('n_subscriber',
            axis=alt.Axis(title='受講生数', titleColor='#57A44C'),
            scale=alt.Scale(domain=[ymin1,ymax1])       # 範囲（上下限値）を追加
        )
    )

    #Y2軸
    line2 = base.mark_line(stroke='#5276A7', interpolate='monotone').encode(
        alt.Y('n_review',
            axis=alt.Axis(title='レビュー数', titleColor='#5276A7'),
            scale=alt.Scale(domain=[ymin2,ymax2])     # 範囲（上下限値）を追加
        )
    )

    #描画
    chart = alt.layer(line1, line2).resolve_scale(
        y = 'independent'
    )
    
    return chart

#print( get_data_ec() )
#print( get_data_udem() )


#df_ec = get_df_ec()
#chart = get_chart()

#st.title('Webスクレイピング活用アプリ')

#st.write('## Udemy情報')
#st.altair_chart(chart, use_container_width=True)

#st.write('## EC在庫情報', df_ec)

#button1 = st.button('追加')
#if button1:
#    main()

if __name__ == '__main__':
    main()
    