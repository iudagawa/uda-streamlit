import streamlit as st
import pandas as pd

#タイトル表示
st.title('demoLayout.py')

#サイドバー
st.sidebar.text('サイドバー項目')
text = st.sidebar.text_input('テキスト入力')
selectValue = st.sidebar.slider('設定値',0,100,20)

#タイトル　数値表示
'テキスト入力',text
'設定値',selectValue

#左右カラムを作成
left_column, right_column = st.columns(2)
#左右にボタンを配置する
button = left_column.button('右カラムに文字を表示')
button2 = right_column.button('左カラムに文字を表示')
#左右ボタンが押された時のテキスト領域を配置／アクション時
if button:
    right_column.write('ここは右カラムです')

if button2:
    left_column.write('ここは左カラムです')


#エキスパンダーテキストBOX
expand1 = st.expander('問い合わせ１')
expand1.write('回答１')
expand2 = st.expander('問い合わせ2')
expand2.write('回答2')
expand3 = st.expander('問い合わせ3')
expand3.write('回答3')