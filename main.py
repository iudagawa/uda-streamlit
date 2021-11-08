import  streamlit as st
import numpy as np
import time

st.title('Streamlit 入門')
st.write('プログレスバーの表示')
'Start'

latest_iteration = st.empty()
bar = st.progress(0)

for i in range(100):
    latest_iteration.text(f'count{i+1}')
    bar.progress(i+1)
    time.sleep(0.1)     # 0.1 sec wait

'Done!!'