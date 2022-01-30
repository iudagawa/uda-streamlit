from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
from PIL import Image
import sys
import time
import json

#秘密鍵を読み込む

with open("c:/udagawa/Py/vscodeProjects/udemy_streamlit/secret.json") as f:
    secret = json.load(f)
        
KEY = secret["KEY"]
ENDPOINT = secret["ENDPOINT"]


#クライアントを認証する
computervision_client = ComputerVisionClient(ENDPOINT, CognitiveServicesCredentials(KEY))


## 画像タグ名取得
def get_tags( filename ):
    
    local_image = open(filename, "rb")

    # Call API with remote image
    tags_resulte = computervision_client.tag_image_in_stream(local_image)
    tags = tags_resulte.tags

    tags_name = []

    for tag in tags:
        tags_name.append( tag.name )
        
    return tags_name

##    物体検出
def detect_objects( filename ):
    local_image = open( filename, "rb")

    # Call API with URL
    detect_objects_results = computervision_client.detect_objects_in_stream( local_image )  #detect_objects_in_stream
    detect_objects =  detect_objects_results.objects
    
    return detect_objects
    

#=====================================================================
#               移行にstreamlit で画面構築
#=====================================================================
import streamlit as st
from PIL import ImageDraw       # 描画の為
from PIL import ImageFont       # 描画の為

st.title('物体検出アプリ')

upload_file = st.file_uploader('画像ファイル選択',type=['jpg','png'])
#file_uploaderにはファイルパス取得が出来ない
if upload_file is not None:
    img = Image.open(upload_file)
    
    
    #物体検出に画像ファイル名を引き渡すため一度パスが分かるテンポラリに保存する
    img_path = f'img/{upload_file.name}'
    img.save(img_path)
    
    #物体検出
    objects = detect_objects(img_path)

    #描画(PIL)
    draw = ImageDraw.Draw(img)

    for object in objects:
        x = object.rectangle.x
        y = object.rectangle.y
        w = object.rectangle.w
        h = object.rectangle.h
        #caption = object.object
        caption = object.object_property
        
        font = ImageFont.truetype(font='./udemy_streamlit/Helvetica 400.ttf',size=50) 
        text_w, text_h = draw.textsize(caption,font=font)
        
        draw.rectangle([(x,y),(x+w,y+h)],fill=None, outline='green', width =5)
        draw.rectangle([(x,y),(x+text_w,y+text_h)],fill='green')
        draw.text((x,y),caption,fill='white',font=font)
            
    st.image(img)  # 画像を表示する

    tags_name = get_tags(img_path)  #['XXXX','XXXX','XXXX',....]
    
    tag_mes = ', '.join(tags_name)    # XXXX, XXXX, XXXX, ・・・・　各要素を", " で区切り連結


    st.markdown('**認識されたコンテンツタグ**')
    st.markdown(f'>{tag_mes}')
    
    
