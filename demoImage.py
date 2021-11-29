import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image
 
st.title('サンプル画像表示')

#ラジオボタン
if st.checkbox('画像表示有/無'):
    img =Image.open('Image5.bmp')
    st.image( img, caption='udagawa isao',use_column_width=True)
    #Audio　や　動画も表示できる
    
#セレクトBOX
select_No = st.selectbox(
    'あなたが好きな数字を選択してください',
    list( range(1,11) )
)
'あなたが選択したNoは:',select_No,'です'

#テキスト入力
input_text = st.text_input('何かテキストを入力してください') 
'入力：',input_text

#スライダーバー
valueParam = st.slider('設定パラメータ',0,100,20)
'設定値:',valueParam
