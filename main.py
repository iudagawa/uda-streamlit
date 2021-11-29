import streamlit as st
import numpy as np
import pandas as pd
import time


st.title('Streamlit 入門')
st.write('プログレスバーの表示')
'Start'

# メイン画面

st.write('読み込みデータ')
uploaded_file = st.file_uploader('ファイルアップロード1',type='xlsx')
if uploaded_file is not None:
    # アップロードファイルをメイン画面にデータ表示
    df = pd.read_excel(uploaded_file ,engine="openpyxl")
    st.dataframe( df, 640,240)


st.write('読み込みデータ2')
uploaded_file2 = st.file_uploader('ファイルアップロード2',type='xlsx')
if uploaded_file2 is not None:
    # アップロードファイルをメイン画面にデータ表示
    df2 = pd.read_excel(uploaded_file2 ,engine="openpyxl")
    st.dataframe( df2, 640,240)



latest_iteration = st.empty()
bar = st.progress(0)

for i in range(100):
    latest_iteration.text(f'count{i+1}')
    bar.progress(i)
    time.sleep(0.01)     # 0.1 sec wait

'Done!!'

if st.button("Exec Create Excel file"):
    pass
    st.write('create file')
