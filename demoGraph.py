import streamlit as st
import numpy as np
import pandas as pd

st.title('Streamlit タイトル')
st.write('DataFrame')

df = pd.DataFrame(
   np.random.rand(20,3),    #２０行、３列　　０～１．０
   columns=['a','b','c']    #１，２，３　列名
)
st.line_chart(df)
#st.area_chart(df)


df = pd.DataFrame(
     np.random.rand(100,2)/(50,50) + [35.69, 139.70],
     columns=['lat','lon']
)
st.map(df)