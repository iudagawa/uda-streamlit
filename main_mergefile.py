import streamlit as st
import numpy as np
import pandas as pd
import time

st.title('LabAlert/GP10 測定データマージツール2')


# メイン画面
#st.write('LabAlert AssetMeasure 読み込みデータ')
uploaded_file1 = st.file_uploader('LabAlert AssetMeasure 読み込み',type='xlsx')
if uploaded_file1 is not None:
    # アップロードファイルをメイン画面にデータ表示
    la_data = pd.read_excel(uploaded_file1 ,engine="openpyxl")
    st.dataframe( la_data, 640,120)

#st.write('GP10 読み込みデータ')
uploaded_file2 = st.file_uploader('GP10 読み込み',type='xlsx')
if uploaded_file2 is not None:
    # アップロードファイルをメイン画面にデータ表示
    gp10_data = pd.read_excel(uploaded_file2 ,engine="openpyxl")
    st.dataframe( gp10_data, 640,120)

st.write('マージした結果は [c:\\xls\\pandas_to_excel.xlsx] に書き込みます')

if st.button("Exec Create Excel file"):
    #LabAlert (AssetMeasureLogs_export.xls) データ読み込み
    #la_data = pd.read_excel('c:/udagawa/Py/vscodeProjects/udagawa/validation/AssetMeasureLogs_export.xlsx',engine="openpyxl")
    la_data['Timestamp'] = pd.to_datetime( la_data['Timestamp (Asia/Tokyo)'])
    la_data['Timestamp2'] = la_data['Timestamp'].dt.strftime("%Y/%m/%d %H:%M %p")

    #GP10 Excel Data(gp10.xlsx)  データ読み込み
    #gp10_data = pd.read_excel('c:/udagawa/Py/vscodeProjects/udagawa/validation/gp10.xlsx',engine="openpyxl")
    gp10_data['Timestamp2'] = gp10_data['時刻'].dt.strftime("%Y/%m/%d %H:%M %p")

    #ファイルマージ
    join_data = pd.merge( gp10_data, la_data, on='Timestamp2',how='left')

    join_data2 = join_data.dropna(subset=['Value'])
    join_data2.rename(columns = { join_data2.columns[2]: '標準器指示値' }, inplace=True)
    join_data3 = join_data2.copy()


    join_data3['fvalue'] = join_data3['Value'].str.replace('C','').astype(float)
    join_data3['delta'] = join_data3['標準器指示値'] - join_data3['fvalue']     #GP10とLabAlert との温度差を算出
    join_data3 = join_data3.loc[:,['Timestamp2','標準器指示値','fvalue','delta','CH0001 [°C]']]

    #ファイルに保存
    join_data3.to_excel('c:\\xls\\pandas_to_excel.xlsx')

    st.dataframe( join_data3, 640, 240 )

    st.write('create file')
    