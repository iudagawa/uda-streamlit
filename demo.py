import streamlit as st
import numpy as np
import pandas as pd

st.title('Streamlit タイトル')

st.write('DataFrame')

df = pd.DataFrame({
    '1列目':[40,30,20,10],
    '2列目':[100,200,300,400],
})

st.write( df )
st.dataframe( df )
st.dataframe( df.style.highlight_max(axis=0) ,width=500,height=100) #最大／最小を黄色　Pandasの機能らしい！　width=500は効かない見たい
st.table(df.style.highlight_max(axis=0)) #ソートが出来ない

"""
# 章　ABC
## 節　ABC
###     項　ABC

```
st.write( df )
st.dataframe( df )
st.dataframe( df.style.highlight_max(axis=0) ,width=500,height=100) #最大／最小を黄色　Pandasの機能らしい！　width=500は効かない見たい
st.table(df.style.highlight_max(axis=0)) #ソートが出来ない
```
"""
