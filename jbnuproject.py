import pandas as pd
import numpy as np
import time
from pytz import timezone
from datetime import datetime

# maping
import json
import requests
pip install branca
pip install folium
import branca
import folium
from folium import plugins

import streamlit as st

from streamlit_folium import st_folium


st.title('JBNU PROJECT')

st.header('Map')


# raw_DataFrame
raw_df = pd.read_csv("https://raw.githubusercontent.com/joco49/project/master/result.csv", header = None)
raw_df.columns = ['이수구분', '과목명', '학점', '담당교수', '강의실', '시간', '담은인원', '비고']

# split
df = raw_df[['강의실', '시간']]

# except
_df = df[~df['강의실'].str.contains('익산', na=False)]
df = _df[~_df['강의실'].str.contains('새만금', na=False)]

# 전체 시간표를 리스트로
Day = ['월', '화', '수', '목', '금']
timeset = []
for k in ['A', 'B']:
    for j in Day:
        for i in range(14):
            word = '%s %s-%s' % (j, str(i), k)
            timeset.append(word)

# 전체 시간표를 테이블로 만들기
df_timeset = pd.DataFrame(timeset)
df_timeset.rename(columns = {0:'Time'}, inplace = True)

# 월 0-A => '월', '0-A'
_a = df_timeset['Time'].str.split(' ')
_result = _a.apply(lambda x: pd.Series(x))
_result = pd.DataFrame(_result)

df_timeset = pd.concat([df_timeset, _result], axis = 1)
df_timeset = df_timeset.rename(columns = {"Time":"raw_Time", 0:"Day_N", 1:"N_Time"})

_a = df_timeset['N_Time'].str.split('-')
_result = _a.apply(lambda x: pd.Series(x))
_result = pd.DataFrame(_result)

df_timeset = pd.concat([df_timeset, _result], axis = 1)
df_timeset = df_timeset.rename(columns = {0:"Hour", 1:"Min"})

for i in range(140):
  if df_timeset.loc[i, "Min"] == 'A':
    df_timeset.loc[i, "Min"] = 0
  else:
    df_timeset.loc[i, "Min"] = 30

for i in range(140):
  df_timeset.loc[i, "Hour"] = int(df_timeset.loc[i, "Hour"]) + 8

# current time

KST = timezone('Asia/Seoul')

today = datetime.now()
today = today.astimezone(KST)

days = ['월', '화', '수', '목', '금', '토', '일']

# 현재 시간

time = int(today.weekday())

day = days[time] 

H = today.strftime("%H")
M = today.strftime("%M")

# 임시 시간 정하기
# day = "화"
# H = "11"
# M = "41"


# 현재시간 기준 공강인 건물

def whatemptyroom(data):
  clt = data.groupby(['강의실']).sum()

  if int(M) >= 30:
    M_new = 'B'
  else:
    M_new = 'A'
  abc = day + ' ' + str(int(H) - 8) + '-' + M_new # "화 7-B"

  clt = clt[~clt['시간'].str.contains(abc, na=False)]
  clt_df = pd.DataFrame(clt.index)
  return clt_df


def emptyroom1(coll):
  _df = df[df['강의실'].str.contains(coll, na=False)]
  clt = whatemptyroom(_df)
  return clt


def emptyroom2(coll, hall):
  _df = df[df['강의실'].str.contains(coll, na=False)]
  _df = _df[_df['강의실'].str.contains(hall, na=False)]
  clt = whatemptyroom(_df)
  return clt


# 간호대학
nursing = emptyroom1("간호대학")

# 골프연습장
golf = emptyroom1("골프연습장")

# 공과대학
engineering_1 = emptyroom2("공과대학", "1호관")
engineering_2 = emptyroom2("공과대학", "2호관")
engineering_3 = emptyroom2("공과대학", "3호관")
engineering_4 = emptyroom2("공과대학", "4호관")
engineering_5 = emptyroom2("공과대학", "5호관")
engineering_6 = emptyroom2("공과대학", "6호관")
engineering_7 = emptyroom2("공과대학", "7호관")
engineering_8 = emptyroom2("공과대학", "8호관")
engineering_9 = emptyroom2("공과대학", "9호관")
engineering_subfact = emptyroom2("공과대학", "부속공장")

# 과학관
sciencemuseum = emptyroom1("과학관")

# 글로벌인재관
globalHR = emptyroom1("글로벌인재관")

# 농업생명과학대학
agriculture_1 = emptyroom2("농업생명과학대학", "1호관")
agriculture_2 = emptyroom2("농업생명과학대학", "2호관")
agriculture_3 = emptyroom2("농업생명과학대학", "3호관")
agriculture_4 = emptyroom2("농업생명과학대학", "4호관")
agriculture_main = emptyroom2("농업생명과학대학", "본관")

# 뉴실크로드센터
newsilkroad = emptyroom1("뉴실크로드센터")

# 미술관
artmuseum = emptyroom1("미술관")

# 생활과학대학
domesticscience = emptyroom1("생활과학대학")

# 사범대 본관
education = emptyroom1("사범대")

# 사회과학대학
socialscience = emptyroom1("사회과학대학")

# 상과대학
commercial_1 = emptyroom2("상과대학", "1호관")
commercial_2 = emptyroom2("상과대학", "2호관")
commercial_3 = emptyroom2("상과대학", "3호관")

# 법학전문대학원
law = emptyroom1("법학전문대학원")

# 예술대학
art_2 = emptyroom2("예술대학", "2호관")
art_main = emptyroom2("예술대학", "본관")

# 예체능관
entertainment = emptyroom1("예체능관")

# 의과대학
medical_2 = emptyroom2("의과대학", "2호관")
medical_main = emptyroom2("의과대학", "본관")

# 치과대학
dental_2 = emptyroom2("치과대학", "2호관")
dental_4 = emptyroom2("치과대학", "4호관")
dental_main = emptyroom2("치과대학", "본관")

# 인문대학
humanities_1 = emptyroom2("인문대학", "1호관")
humanities_2 = emptyroom2("인문대학", "2호관")

# 자연과학대학
natural_science_1 = emptyroom2("자연과학대학", "1호관")
natural_science_2 = emptyroom2("자연과학대학", "2호관")
natural_science_3 = emptyroom2("자연과학대학", "3호관")
natural_science_4 = emptyroom2("자연과학대학", "4호관")
natural_science_5 = emptyroom2("자연과학대학", "5호관")
natural_science_main = emptyroom2("자연과학대학", "본관")

# 학술문화관
academicculture = emptyroom1("학술문화관")

# 정보전산원 교육동
informationcomputing = emptyroom1("정보전산원")

# 진수당
jinsudang = emptyroom1("진수당")

# 체육관
gym = emptyroom1("체육관")

# 학술림관리사
experimentforest = emptyroom1("학술림관리사")

# 학습도서관
learninglibrary = emptyroom1("학습도서관")



# 지도 구현
m = folium.Map(
    location = [35.8467747, 127.1306096],
    zoom_start = 16)

popup = folium.Popup(nursing.to_html(), min_width=200, max_width=200)
folium.Marker([35.8471751, 127.1450295], popup=popup).add_to(m)

popup = folium.Popup(engineering_1.to_html(), min_width=200, max_width=200)
folium.Marker([35.8468291, 127.1325569], popup=popup).add_to(m)

popup = folium.Popup(engineering_2.to_html(), min_width=200, max_width=200)
folium.Marker([35.8468569, 127.1316126], popup=popup).add_to(m)

popup = folium.Popup(engineering_3.to_html(), min_width=200, max_width=200)
folium.Marker([35.846884, 127.1335291], popup=popup).add_to(m)

popup = folium.Popup(engineering_4.to_html(), min_width=200, max_width=200)
folium.Marker([35.8474957, 127.1325291], popup=popup).add_to(m)

popup = folium.Popup(engineering_5.to_html(), min_width=200, max_width=200)
folium.Marker([35.8475235, 127.1313348], popup=popup).add_to(m)

popup = folium.Popup(engineering_6.to_html(), min_width=200, max_width=200)
folium.Marker([35.8470514, 127.1344179], popup=popup).add_to(m)

popup = folium.Popup(engineering_7.to_html(), min_width=200, max_width=200)
folium.Marker([35.845996, 127.1344457], popup=popup).add_to(m)

popup = folium.Popup(engineering_8.to_html(), min_width=200, max_width=200)
folium.Marker([35.8482734, 127.133529], popup=popup).add_to(m)

popup = folium.Popup(engineering_9.to_html(), min_width=200, max_width=200)
folium.Marker([35.8475513, 127.1335013], popup=popup).add_to(m)

popup = folium.Popup(sciencemuseum.to_html(), min_width=200, max_width=200)
folium.Marker([35.8457459, 127.1296683], popup=popup).add_to(m)

popup = folium.Popup(globalHR.to_html(), min_width=200, max_width=200)
folium.Marker([35.8456071, 127.1331958], popup=popup).add_to(m)

popup = folium.Popup(agriculture_main.to_html(), min_width=200, max_width=200)
folium.Marker([35.8492733, 127.1328902], popup=popup).add_to(m)

popup = folium.Popup(agriculture_1.to_html(), min_width=200, max_width=200)
folium.Marker([35.8491344, 127.130807], popup=popup).add_to(m)

popup = folium.Popup(agriculture_2.to_html(), min_width=200, max_width=200)
folium.Marker([35.8490511, 127.1318903], popup=popup).add_to(m)

popup = folium.Popup(agriculture_3.to_html(), min_width=200, max_width=200)
folium.Marker([35.848579, 127.1346956], popup=popup).add_to(m)

popup = folium.Popup(agriculture_4.to_html(), min_width=200, max_width=200)
folium.Marker([35.8483846, 127.1356677], popup=popup).add_to(m)

popup = folium.Popup(newsilkroad.to_html(), min_width=200, max_width=200)
folium.Marker([35.8444214, 127.1303931], popup=popup).add_to(m)

popup = folium.Popup(artmuseum.to_html(), min_width=200, max_width=200)
folium.Marker([35.8461625, 127.1267242], popup=popup).add_to(m)

popup = folium.Popup(domesticscience.to_html(), min_width=200, max_width=200)
folium.Marker([35.8424963, 127.1327237], popup=popup).add_to(m)

popup = folium.Popup(education.to_html(), min_width=200, max_width=200)
folium.Marker([35.8425932, 127.1320165], popup=popup).add_to(m)

popup = folium.Popup(socialscience.to_html(), min_width=200, max_width=200)
folium.Marker([35.8440331, 127.1337465], popup=popup).add_to(m)

popup = folium.Popup(commercial_1.to_html(), min_width=200, max_width=200)
folium.Marker([35.8446905, 127.1338624], popup=popup).add_to(m)

popup = folium.Popup(commercial_2.to_html(), min_width=200, max_width=200)
folium.Marker([35.8447183, 127.1353067], popup=popup).add_to(m)

popup = folium.Popup(commercial_3.to_html(), min_width=200, max_width=200)
folium.Marker([35.8446628, 127.1359733], popup=popup).add_to(m)

popup = folium.Popup(law.to_html(), min_width=200, max_width=200)
folium.Marker([35.8447821, 127.1326894], popup=popup).add_to(m)

popup = folium.Popup(art_2.to_html(), min_width=200, max_width=200)
folium.Marker([35.8508286, 127.1280572], popup=popup).add_to(m)

popup = folium.Popup(art_main.to_html(), min_width=200, max_width=200)
folium.Marker([35.8504675, 127.1273073], popup=popup).add_to(m)

popup = folium.Popup(entertainment.to_html(), min_width=200, max_width=200)
folium.Marker([35.8477457, 127.1296961], popup=popup).add_to(m)

popup = folium.Popup(medical_2.to_html(), min_width=200, max_width=200)
folium.Marker([35.8480514, 127.1422782], popup=popup).add_to(m)

popup = folium.Popup(medical_main.to_html(), min_width=200, max_width=200)
folium.Marker([35.8471263, 127.1428746], popup=popup).add_to(m)

popup = folium.Popup(dental_2.to_html(), min_width=200, max_width=200)
folium.Marker([35.8455599, 127.1383343], popup=popup).add_to(m)

popup = folium.Popup(dental_4.to_html(), min_width=200, max_width=200)
folium.Marker([35.84738, 127.137674], popup=popup).add_to(m)

popup = folium.Popup(dental_main.to_html(), min_width=200, max_width=200)
folium.Marker([35.8459127, 127.1385008], popup=popup).add_to(m)

popup = folium.Popup(humanities_1.to_html(), min_width=200, max_width=200)
folium.Marker([35.8431907, 127.1330847], popup=popup).add_to(m)

popup = folium.Popup(humanities_2.to_html(), min_width=200, max_width=200)
folium.Marker([35.844213, 127.132707], popup=popup).add_to(m)

popup = folium.Popup(natural_science_1.to_html(), min_width=200, max_width=200)
folium.Marker([35.8453292, 127.1271964], popup =popup).add_to(m)

popup = folium.Popup(natural_science_2.to_html(), min_width=200, max_width=200)
folium.Marker([35.8450793, 127.1288629], popup=popup).add_to(m)

popup = folium.Popup(natural_science_3.to_html(), min_width=200, max_width=200)
folium.Marker([35.8470513, 127.1304738], popup=popup).add_to(m)

popup = folium.Popup(natural_science_4.to_html(), min_width=200, max_width=200)
folium.Marker([35.8466069, 127.130696], popup=popup).add_to(m)

popup = folium.Popup(natural_science_5.to_html(), min_width=200, max_width=200)
folium.Marker([35.8461348, 127.1307238], popup=popup).add_to(m)

popup = folium.Popup(natural_science_main.to_html(), min_width=200, max_width=200)
folium.Marker([35.8474229, 127.1307156], popup=popup).add_to(m)

popup = folium.Popup(academicculture.to_html(), min_width=200, max_width=200)
folium.Marker([35.8449404, 127.1298628], popup=popup).add_to(m)

popup = folium.Popup(informationcomputing.to_html(), min_width=200, max_width=200)
folium.Marker([35.8439406, 127.1348346], popup=popup).add_to(m)

popup = folium.Popup(jinsudang.to_html(), min_width=200, max_width=200)
folium.Marker([35.8448451, 127.1313825], popup=popup).add_to(m)

popup = folium.Popup(gym.to_html(), min_width=200, max_width=200)
folium.Marker([35.8470234, 127.1252798], popup=popup).add_to(m)

popup = folium.Popup(learninglibrary.to_html(), min_width=200, max_width=200)
folium.Marker([35.8475513, 127.1355288], popup=popup).add_to(m)

st_data = st_folium(m, width=725)


# 검색

st.header('Search')

collage = st.selectbox("원하는 단과대학을 선택하세요.",
                        ["간호대학",
                        "공과대학",
                        "과학관",
                        "글로벌인재관",
                        "농업생명과학대학",
                        "뉴실크로드센터",
                        "미술관",
                        "생활과학대학",
                        "사범대 본관",
                        "사회과학대학",
                        "상과대학",
                        "법학전문대학원",
                        "예술대학",
                        "예체능관",
                        "의과대학",
                        "치과대학",
                        "인문대학",
                        "자연과학대학",
                        "학술문화관",
                        "정보전산원",
                        "진수당",
                        "체육관",
                        "학술림관리사",
                        "학습도서관"])

hall = None

# collage_1 = ["간호대학", "과학관", "글로벌인재관", "뉴실크로드센터", "미술관", "생활과학대학", "사범대 본관", "사회과학대학", "법학전문대학원",
#             "예체능관", "학술문화관", "정보전산원", "진수당", "체육관", "학술림관리사", "학습도서관"]

# collage_2 = ["공과대학", "농업생명과학대학", "상과대학", "예술대학", "의과대학", "치과대학", "인문대학", "자연과학대학"]

if collage in "공과대학":
    hall = st.selectbox("원하는 호관을 선택하세요.",
                        ["1호관",
                        "2호관", 
                        "3호관",
                        "4호관",
                        "5호관",
                        "6호관",
                        "7호관",
                        "8호관",
                        "9호관",
                        "부속공장"])

if collage in "농업생명과학대학":
    hall = st.selectbox("원하는 호관을 선택하세요.",
                        ["1호관",
                        "2호관", 
                        "3호관",
                        "4호관",
                        "본관"])

if collage in "상과대학":
    hall = st.selectbox("원하는 호관을 선택하세요.",
                        ["1호관",
                        "2호관", 
                        "3호관"])

if collage in "예술대학":
    hall = st.selectbox("원하는 호관을 선택하세요.",
                        ["2호관",
                        "본관"])

if collage in "의과대학":
    hall = st.selectbox("원하는 호관을 선택하세요.",
                        ["2호관",
                        "본관"])

if collage in "치과대학":
    hall = st.selectbox("원하는 호관을 선택하세요.",
                        ["2호관",
                        "4호관",
                        "본관"])

if collage in "인문대학":
    hall = st.selectbox("원하는 호관을 선택하세요.",
                        ["1호관",
                        "2호관"])

if collage in "자연과학대학":
    hall = st.selectbox("원하는 호관을 선택하세요.",
                        ["1호관",
                        "2호관", 
                        "3호관",
                        "4호관",
                        "5호관",
                        "본관"])

date = st.selectbox("원하는 요일을 선택하세요.", ["월", "화", "수", "목", "금"])

# dataframe의 시간을 list로 풀어줌
def flatten(lst):
    result = []
    for item in lst:
        result.extend(item)
    return result

# spliting
def spliting(_df):
    _df = _df['시간'].str.split(',')
    reshape = _df.values.reshape(-1, 1)
    reshape = flatten(flatten(reshape))
    return reshape

def emptyroom(reshape, day):
    complement = list(set(timeset).difference(reshape))

    abse = pd.DataFrame(complement)
    abse.columns = ['raw_Time']
    df_merge = pd.merge(df_timeset, abse, how = 'right', on = "raw_Time")

    df_merge = df_merge[df_merge['Day_N'] == day]
    df_merge = df_merge.sort_values(['Hour', 'Min']).reset_index()

    return df_merge[['Hour', 'Min']]

def datetable(number):
    _df = df[df['강의실'].str.contains(collage, na=False)]
    if hall == None:
        pass
    else:
        _df = _df[_df['강의실'].str.contains(hall, na=False)]
    _df = _df[_df['강의실'].str.contains(number, na=False)]
    reshape = spliting(_df)
    return emptyroom(reshape, date)

if collage == '간호대학':
    a = datetable('201')
    b = datetable('202')
    c = datetable('303')
    d = datetable('306')
    e = datetable('307')
    f = datetable('312')
    g = datetable('401')
    h = datetable('403')
    i = datetable('405')
    j = datetable('407')
    k = datetable('416')
    l = datetable('422')
    m = datetable('501')
    datetableset = pd.concat([a, b, c, d, e, f, g, h, i ,j ,k ,l ,m], axis=1)

    datetableset.columns = [['201', '201', '202', '202', '303', '303', '306', '306', '307', '307', '312', '312', '401', '401', '403', '403',
                            '405', '405', '407', '407', '416', '416', '422', '422', '501', '501'],
                            ['Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min',
                            'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min']]

if collage == '공과대학' and hall == '1호관':
    a = datetable('122')
    b = datetable('123')
    c = datetable('130')
    d = datetable('146')
    e = datetable('147')
    f = datetable('149')
    g = datetable('158')
    h = datetable('161')
    i = datetable('219')
    j = datetable('224')
    k = datetable('225')
    l = datetable('234')
    m = datetable('246')
    n = datetable('249')
    o = datetable('302')
    p = datetable('303')
    q = datetable('315')
    r = datetable('317')
    s = datetable('321')
    t = datetable('322')
    u = datetable('328')
    v = datetable('340')
    datetableset = pd.concat([a, b, c, d, e, f, g, h, i ,j ,k ,l ,m, n, o, p, q, r, s, t, u, v], axis=1)

    datetableset.columns = [['122', '122', '123', '123', '130', '130', '146', '146', '147', '147', '149', '149', '158', '158', '161', '161',
                            '219', '219', '224', '224', '225', '225', '234', '234', '246', '246', '249', '249', '302', '302', '303', '303',
                            '315', '315', '317', '317', '321', '321', '322', '322', '328', '328', '340', '340'],
                            ['Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min',
                            'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min',
                            'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min',
                            'Hour', 'Min']]

if collage == '공과대학' and hall == '2호관':
    a = datetable('104')
    b = datetable('105')
    c = datetable('116')
    d = datetable('117')
    e = datetable('403')
    f = datetable('404')
    g = datetable('405')
    h = datetable('416')
    i = datetable('417')
    j = datetable('418')
    datetableset = pd.concat([a, b, c, d, e, f, g, h, i ,j], axis=1)

    datetableset.columns = [['104', '104', '105', '105', '116', '116', '117', '117', '403', '403', '404', '404', '405', '405', '416', '416',
                            '417', '417', '418', '418'],
                            ['Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min',
                            'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min']]

if collage == '공과대학' and hall == '3호관':
    a = datetable('103')
    b = datetable('104')
    c = datetable('108')
    d = datetable('306')
    e = datetable('309')
    f = datetable('310')
    g = datetable('311')
    h = datetable('401')
    i = datetable('403')
    j = datetable('404')
    k = datetable('406')
    l = datetable('408')
    m = datetable('409')
    n = datetable('410')
    o = datetable('411')
    datetableset = pd.concat([a, b, c, d, e, f, g, h, i ,j ,k ,l ,m, n, o], axis=1)

    datetableset.columns = [['122', '122', '123', '123', '130', '130', '146', '146', '147', '147', '149', '149', '158', '158', '161', '161',
                            '219', '219', '224', '224', '225', '225', '234', '234', '246', '246', '249', '249', '302', '302'],
                            ['Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min',
                            'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min',
                            'Hour', 'Min']]

if collage == '공과대학' and hall == '4호관':
    a = datetable('002')
    b = datetable('004')
    c = datetable('126')
    d = datetable('315')
    e = datetable('401')
    f = datetable('402')
    g = datetable('403')
    h = datetable('405')
    i = datetable('418')
    j = datetable('419')
    datetableset = pd.concat([a, b, c, d, e, f, g, h, i ,j], axis=1)

    datetableset.columns = [['002', '002', '004', '004', '126', '126', '315', '315', '401', '401', '402', '402', '403', '403', '405', '405',
                            '418', '418', '419', '419'],
                            ['Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min',
                            'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min']]

if collage == '공과대학' and hall == '5호관':
    a = datetable('302')
    b = datetable('303')
    c = datetable('311')
    d = datetable('312')
    e = datetable('314')
    f = datetable('414')
    g = datetable('503')
    h = datetable('507')
    i = datetable('509')
    j = datetable('513')
    datetableset = pd.concat([a, b, c, d, e, f, g, h, i ,j], axis=1)

    datetableset.columns = [['302', '302', '303', '303', '311', '311', '312', '312', '314', '314', '414', '414', '503', '503', '507', '507',
                            '509', '509', '513', '513'],
                            ['Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min',
                            'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min']]

if collage == '공과대학' and hall == '6호관':
    a = datetable('111')
    b = datetable('309')
    c = datetable('310')
    d = datetable('312')
    e = datetable('318')
    f = datetable('407')
    g = datetable('508')
    h = datetable('509')
    i = datetable('516')
    j = datetable('517')
    k = datetable('B11')
    l = datetable('B12')
    m = datetable('B13')
    n = datetable('B14')
    o = datetable('B15')
    p = datetable('B16')
    q = datetable('B17')
    r = datetable('B18')
    datetableset = pd.concat([a, b, c, d, e, f, g, h, i ,j ,k ,l ,m, n, o, p, q, r], axis=1)

    datetableset.columns = [['111', '111', '309', '309', '310', '310', '312', '312', '318', '318', '407', '407', '508', '508', '509', '509',
                            '516', '516', '517', '517', 'B11', 'B11', 'B12', 'B12', 'B13', 'B13', 'B14', 'B14', 'B15', 'B15', 'B16', 'B16',
                            'B17', 'B17', 'B18', 'B18'],
                            ['Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min',
                            'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min',
                            'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min']]

if collage == '공과대학' and hall == '7호관':
    a = datetable('102')
    b = datetable('105')
    c = datetable('110')
    d = datetable('112')
    e = datetable('114')
    f = datetable('124')
    g = datetable('202')
    h = datetable('204')
    i = datetable('206')
    j = datetable('227')
    k = datetable('228')
    l = datetable('301')
    m = datetable('302')
    n = datetable('330')
    o = datetable('403')
    p = datetable('534')
    datetableset = pd.concat([a, b, c, d, e, f, g, h, i ,j ,k ,l ,m, n, o, p], axis=1)

    datetableset.columns = [['102', '102', '105', '105', '110', '110', '112', '112', '114', '114', '124', '124', '202', '202', '204', '204',
                            '206', '206', '227', '227', '228', '228', '301', '301', '302', '302', '330', '330', '403', '403', '534', '534'],
                            ['Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min',
                            'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min',
                            'Hour', 'Min', 'Hour', 'Min']]

if collage == '공과대학' and hall == '8호관':
    a = datetable('208')
    b = datetable('212')
    c = datetable('213')
    d = datetable('301')
    e = datetable('302')
    f = datetable('303')
    g = datetable('304')
    h = datetable('310')
    i = datetable('402')
    j = datetable('403')
    k = datetable('406')
    l = datetable('408')
    datetableset = pd.concat([a, b, c, d, e, f, g, h, i ,j ,k ,l ], axis=1)

    datetableset.columns = [['208', '208', '212', '212', '213', '213', '301', '301', '302', '302', '303', '303', '304', '304', '310', '310',
                            '402', '402', '403', '403', '406', '406', '408', '408'],
                            ['Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min',
                            'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min']]

if collage == '공과대학' and hall == '9호관':
    a = datetable('202')
    b = datetable('203')
    c = datetable('204')
    d = datetable('205')
    e = datetable('206')
    f = datetable('301')
    g = datetable('302')
    h = datetable('303')
    i = datetable('306')
    j = datetable('307')
    k = datetable('913')
    l = datetable('914')
    m = datetable('915')
    n = datetable('916')
    datetableset = pd.concat([a, b, c, d, e, f, g, h, i ,j ,k ,l ,m, n], axis=1)

    datetableset.columns = [['202', '202', '203', '203', '204', '204', '205', '205', '206', '206', '301', '301', '302', '302', '303', '303',
                            '306', '306', '307', '307', '913', '913', '914', '914', '915', '915', '916', '916'],
                            ['Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min',
                            'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min']]

if collage == '공과대학' and hall == '부속공장':
    a = datetable('101')
    b = datetable('103')
    c = datetable('201')
    d = datetable('206')
    datetableset = pd.concat([a, b, c, d], axis=1)

    datetableset.columns = [['101', '101', '103', '103', '201', '201', '206', '206'],
                            ['Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min']]

if collage == '과학관':
    a = datetable('109')
    b = datetable('111')
    c = datetable('127')
    d = datetable('128')
    e = datetable('129')
    f = datetable('131')
    g = datetable('227')
    h = datetable('319')
    i = datetable('401')
    j = datetable('402')
    k = datetable('404')
    l = datetable('408')
    m = datetable('409')
    n = datetable('411')
    o = datetable('413')
    p = datetable('414')
    q = datetable('415')
    r = datetable('PH02')
    datetableset = pd.concat([a, b, c, d, e, f, g, h, i ,j ,k ,l ,m, n, o, p, q, r], axis=1)

    datetableset.columns = [['109', '109', '111', '111', '127', '127', '128', '128', '129', '129', '131', '131', '227', '227', '319', '319',
                            '401', '401', '402', '402', '404', '404', '408', '408', '409', '409', '411', '411', '413', '413', '414', '414',
                            '415', '415', 'PH02', 'PH02'],
                            ['Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min',
                            'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min',
                            'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min']]

if collage == '글로벌인재관':
    a = datetable('107')
    b = datetable('123')
    c = datetable('124')
    d = datetable('125')
    e = datetable('206')
    f = datetable('207')
    g = datetable('217')
    h = datetable('218')
    i = datetable('219')
    j = datetable('220')
    datetableset = pd.concat([a, b, c, d, e, f, g, h, i ,j], axis=1)

    datetableset.columns = [['107', '107', '123', '123', '124', '124', '125', '125', '206', '206', '207', '207', '217', '217', '218', '218',
                            '219', '219', '220', '220'],
                            ['Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min',
                            'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min']]

if collage == '농업생명과학대학' and hall == '1호관':
    a = datetable('209')
    b = datetable('301')
    c = datetable('303')
    d = datetable('309')
    datetableset = pd.concat([a, b, c, d], axis=1)

    datetableset.columns = [['209', '209', '301', '301', '303', '303', '309', '309'],
                            ['Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min']]

if collage == '농업생명과학대학' and hall == '2호관':
    a = datetable('216')
    b = datetable('217')
    c = datetable('219')
    d = datetable('222')
    e = datetable('318')
    f = datetable('326')
    g = datetable('401')
    h = datetable('402')
    i = datetable('403')
    j = datetable('404')
    k = datetable('405')
    l = datetable('411')
    m = datetable('412')
    n = datetable('100')
    datetableset = pd.concat([a, b, c, d, e, f, g, h, i ,j ,k ,l ,m, n], axis=1)

    datetableset.columns = [['216', '216', '217', '217', '219', '219', '222', '222', '318', '318', '326', '326', '401', '401', '402', '402',
                            '403', '403', '404', '404', '405', '405', '411', '411', '412', '412', '강당', '강당'],
                            ['Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min',
                            'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min']]

if collage == '농업생명과학대학' and hall == '3호관':
    a = datetable('312')
    b = datetable('316')
    c = datetable('317')
    d = datetable('402')
    e = datetable('405')
    f = datetable('406')
    g = datetable('408')
    h = datetable('409')
    i = datetable('410')
    j = datetable('411')
    k = datetable('415')
    l = datetable('416')
    datetableset = pd.concat([a, b, c, d, e, f, g, h, i ,j ,k ,l], axis=1)

    datetableset.columns = [['312', '312', '316', '316', '317', '317', '402', '402', '405', '405', '406', '406', '408', '408', '409', '409',
                            '410', '410', '411', '411', '415', '415', '416', '416'],
                            ['Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min',
                            'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min']]

if collage == '농업생명과학대학' and hall == '4호관':
    a = datetable('120')
    b = datetable('224')
    c = datetable('301')
    d = datetable('323')
    e = datetable('324')
    f = datetable('401')
    g = datetable('402')
    h = datetable('403')
    i = datetable('419')
    j = datetable('422')
    k = datetable('423')
    datetableset = pd.concat([a, b, c, d, e, f, g, h, i ,j ,k], axis=1)

    datetableset.columns = [['120', '120', '224', '224', '301', '301', '323', '323', '324', '324', '401', '401', '402', '402', '403', '403',
                            '419', '419', '422', '422', '423', '423'],
                            ['Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min',
                            'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min']]

if collage == '농업생명과학대학' and hall == '본관':
    a = datetable('104')
    b = datetable('106')
    c = datetable('107')
    d = datetable('207')
    e = datetable('217')
    f = datetable('218')
    g = datetable('302')
    h = datetable('402')
    i = datetable('403')
    j = datetable('414')
    k = datetable('423')
    datetableset = pd.concat([a, b, c, d, e, f, g, h, i ,j ,k], axis=1)

    datetableset.columns = [['104', '104', '106', '106', '107', '107', '207', '207', '217', '217', '218', '218', '302', '302', '402', '402',
                            '403', '403', '414', '414', '423', '423'],
                            ['Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min',
                            'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min']]

if collage == '뉴실크로드센터':
    a = datetable('201')
    b = datetable('501')
    c = datetable('502')
    d = datetable('504')
    e = datetable('505')
    f = datetable('506')
    g = datetable('510')
    h = datetable('511')
    i = datetable('512')
    j = datetable('513')
    k = datetable('609')
    l = datetable('610')
    m = datetable('611')
    n = datetable('612')
    datetableset = pd.concat([a, b, c, d, e, f, g, h, i ,j ,k ,l ,m, n], axis=1)

    datetableset.columns = [['201', '201', '501', '501', '502', '502', '504', '504', '505', '505', '506', '506', '510', '510', '511', '511',
                            '512', '512', '513', '513', '609', '609', '610', '610', '611', '611', '612', '612'],
                            ['Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min',
                            'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min']]

if collage == '미술관':
    a = datetable('1020')
    b = datetable('1100')
    c = datetable('1110')
    d = datetable('1230')
    e = datetable('2010')
    f = datetable('2040')
    g = datetable('2050')
    h = datetable('2060')
    i = datetable('2070')
    j = datetable('2090')
    k = datetable('2110')
    l = datetable('3030')
    datetableset = pd.concat([a, b, c, d, e, f, g, h, i ,j ,k ,l], axis=1)

    datetableset.columns = [['1020', '1020', '1100', '1100', '1110', '1110', '1230', '1230', '2010', '2010', '2040', '2040', '2050', '2050',
                            '2060', '2060', '2070', '2070', '2090', '2090', '2110', '2110', '3030', '3030'],
                            ['Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min',
                            'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min']]

if collage == '생활과학대학':
    a = datetable("110")
    b = datetable("116")
    c = datetable("118")
    d = datetable("216")
    e = datetable("308")
    f = datetable("310")
    g = datetable("312")
    h = datetable("314")
    i = datetable("316")
    j = datetable("407")
    k = datetable("408")
    l = datetable("412")
    m = datetable("414")
    n = datetable("415")
    o = datetable("418")
    p = datetable("507")
    q = datetable("508")
    datetableset = pd.concat([a, b, c, d, e, f, g, h, i ,j ,k ,l ,m, n, o, p, q], axis=1)

    datetableset.columns = [['110', '110', '116', '116', '118', '118', '216', '216', '308', '308', '310', '310', '312', '312', '314', '314',
                            '316', '316', '407', '407', '408', '408', '412', '412', '414', '414', '415', '415', '418', '418', '507', '507',
                            '508', '508'],
                            ['Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min',
                            'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min',
                            'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min']]

if collage == '사범대':
    a = datetable("104")
    b = datetable("105")
    c = datetable("109")
    d = datetable("110")
    e = datetable("312")
    f = datetable("315")
    g = datetable("401")
    h = datetable("412")
    i = datetable("415")
    j = datetable("501")
    k = datetable("502")
    l = datetable("503")
    m = datetable("504")
    n = datetable("505")
    o = datetable("506")
    p = datetable("508")
    q = datetable("509")
    datetableset = pd.concat([a, b, c, d, e, f, g, h, i ,j ,k ,l ,m, n, o, p, q, r, s, t], axis=1)

    datetableset.columns = [['104', '104', '105', '105', '109', '109', '110', '110', '312', '312', '315', '315', '401', '401', '412', '412',
                            '415', '415', '501', '501', '502', '502', '503', '503', '504', '504', '505', '505', '506', '506', '508', '508',
                            '509', '509'],
                            ['Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min',
                            'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min',
                            'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min']]

if collage == '사회과학대학':
    a = datetable("102")
    b = datetable("105")
    c = datetable("108")
    d = datetable("111")
    e = datetable("113")
    f = datetable("217")
    g = datetable("219")
    h = datetable("220")
    i = datetable("223")
    j = datetable("315")
    k = datetable("317")
    l = datetable("318")
    m = datetable("319")
    n = datetable("414")
    o = datetable("416")
    p = datetable("418")
    q = datetable("420")
    r = datetable("509")
    s = datetable("510")
    t = datetable("511")
    datetableset = pd.concat([a, b, c, d, e, f, g, h, i ,j ,k ,l ,m, n, o, p, q, r, s, t], axis=1)

    datetableset.columns = [['102', '102', '105', '105', '108', '108', '111', '111', '113', '113', '217', '217', '219', '219', '220', '220',
                            '223', '223', '315', '315', '317', '317', '318', '318', '319', '319', '414', '414', '416', '416', '418', '418',
                            '420', '420', '509', '509', '510', '510', '511', '511'],
                            ['Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min',
                            'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min',
                            'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min']]

if collage == '상과대학' and hall == '1호관':
    a = datetable("110")
    b = datetable("122")
    c = datetable("201")
    d = datetable("202")
    e = datetable("203")
    f = datetable("205")
    g = datetable("206")
    h = datetable("301")
    i = datetable("302")
    j = datetable("402")
    k = datetable("403")
    l = datetable("405")
    m = datetable("406")
    datetableset = pd.concat([a, b, c, d, e, f, g, h, i, j], axis=1)

    datetableset.columns = [['110', '110', '122', '122', '201', '201', '202', '202', '203', '203', '205', '205', '206', '206', '301', '301',
                            '302', '302', '402', '402', '403', '403', '405', '405', '406', '406'],
                            ['Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min',
                            'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min']]

if collage == '상과대학' and hall == '2호관':
    a = datetable("109")
    b = datetable("110")
    c = datetable("111")
    d = datetable("310")
    e = datetable("312")
    f = datetable("313")
    datetableset = pd.concat([a, b, c, d, e, f], axis=1)

    datetableset.columns = [['109', '109', '110', '110', '111', '111', '310', '310', '312', '312', '313', '313'],
                            ['Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min']]

if collage == '상과대학' and hall == '3호관':
    a = datetable("104")
    b = datetable("105")
    c = datetable("201")
    d = datetable("202")
    e = datetable("203")
    f = datetable("204")
    datetableset = pd.concat([a, b, c, d, e, f], axis=1)

    datetableset.columns = [['104', '104', '105', '105', '201', '201', '202', '202', '203', '203', '204', '204'],
                            ['Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min']]

if collage == '법학전문대학원' :
    a = datetable("101")
    datetableset = pd.concat([a], axis=1)

    datetableset.columns = [['101', '101'], ['Hour', 'Min']]

if collage == '예술대학' and hall == '2호관':
    a = datetable("1070")
    b = datetable("1080")
    c = datetable("1081")
    d = datetable("1111")
    e = datetable("1112")
    f = datetable("1121")
    g = datetable("1122")
    h = datetable("1131")
    i = datetable("1132")
    j = datetable("1141")
    k = datetable("1142")
    l = datetable("1181")
    m = datetable("1182")
    n = datetable("1183")
    o = datetable("1184")
    p = datetable("1190")
    q = datetable("2010")
    r = datetable("2090")
    s = datetable("2110")
    t = datetable("3010")
    u = datetable("3070")
    v = datetable("3080")
    w = datetable("3090")
    x = datetable("3100")
    y = datetable("3110")
    z = datetable("3150")
    aa = datetable("3280")
    bb = datetable("4030")
    datetableset = pd.concat([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z, aa, bb ], axis=1)

    datetableset.columns = [['1070', '1070', '1080', '1080', '1081', '1081', '1111', '1111', '1112', '1112', '1121', '1121', '1122', '1122', '1131', '1131',
                            '1132', '1132', '1141', '1141', '1142', '1142', '1181', '1181', '1182', '1182', '1183', '1183', '1184', '1184', '1190', '1190',
                            '2010', '2010', '2090', '2090', '2110', '2110', '3010', '3010', '3070', '3070', '3080', '3080', '3090', '3090', '3110', '3110',
                            '3110', '3110', '3150', '3150', '3280', '3280', '4030', '4030'],
                            ['Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min',
                            'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min',
                            'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min',
                            'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min',
                            'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min']]

if collage == '예술대학' and hall == '본관':
    a = datetable("1030")
    b = datetable("1070")
    c = datetable("1080")
    d = datetable("1090")
    e = datetable("1130")
    f = datetable("1140")
    g = datetable("1160")
    h = datetable("1191")
    i = datetable("1230")
    j = datetable("1260")
    k = datetable("2070")
    l = datetable("2080")
    m = datetable("2090")
    n = datetable("2110")
    o = datetable("2140")
    p = datetable("2180")
    q = datetable("3040")
    r = datetable("3070")
    s = datetable("3080")
    t = datetable("3110")
    u = datetable("3120")
    v = datetable("3170")
    w = datetable("3190")
    x = datetable("4031")
    y = datetable("4051")
    z = datetable("4070")
    aa = datetable("4080")
    bb = datetable("4100")
    cc = datetable("4120")
    dd = datetable("4140")
    ee = datetable("4150")
    ff = datetable("4160")
    gg = datetable("4180")
    hh = datetable("4190")
    ii = datetable("5020")
    jj = datetable("5050")
    kk = datetable("5070")
    ll = datetable("5080")
    mm = datetable("5090")
    nn = datetable("5100")
    datetableset = pd.concat([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z, aa, bb, cc, dd, ee, ff, gg, hh, ii, jj, kk ,ll, mm, nn], axis=1)

    datetableset.columns = [['1030', '1030', '1070', '1070', '1080', '1080', '1090', '1090', '1130', '1130', '1140', '1140', '1160', '1160',
                            '1191', '1191', '1230', '1230', '1260', '1260', '2070', '2070', '2080', '2080', '2090', '2090', '2110', '2110',
                            '2140', '2140', '2180', '2180', '3040', '3040', '3070', '3070', '3080', '3080', '3110', '3110', '3120', '3120',
                            '3170', '3170', '3190', '3190', '4031', '4031', '4051', '4051', '4070', '4070', '4080', '4080', '4100', '4100',
                            '4120', '4120', '4140', '4140', '4150', '4150', '4160', '4160', '4180', '4180', '4190', '4190', '5020', '5020',
                            '5050', '5050', '5070', '5070', '5080', '5080', '5090', '5090', '5100', '5100'],
                            ['Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min',
                            'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min',
                            'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min',
                            'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min',
                            'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min',
                            'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min']]

if collage == '예체능관':
    a = datetable("111")
    b = datetable("114")
    c = datetable("216")
    d = datetable("219")
    e = datetable("301")
    f = datetable("304")
    g = datetable("307")
    h = datetable("309")
    i = datetable("311")
    j = datetable("316")
    k = datetable("318")
    l = datetable("319")
    m = datetable("320")
    n = datetable("321")
    o = datetable("322")
    p = datetable("323")
    q = datetable("324")
    r = datetable("325")
    s = datetable("326")
    t = datetable("328")
    u = datetable("329")
    v = datetable("330")
    w = datetable("331")
    x = datetable("332")
    datetableset = pd.concat([a, b, c, d, e, f, g, h, i ,j ,k ,l ,m, n, o, p, q, r, s, t, u, v, w, x], axis=1)

    datetableset.columns = [['111', '111', '114', '114', '216', '216', '219', '219', '301', '301', '304', '304', '307', '307', '309', '309',
                            '311', '311', '316', '316', '318', '318', '319', '319', '320', '320', '321', '321', '322', '322', '323', '323',
                            '324', '324', '325', '325', '326', '326', '328', '328', '329', '329', '330', '330', '331', '331', '332', '332'],
                            ['Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min',
                            'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min',
                            'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min',
                            'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min']]

if collage == '의과대학' and hall == '2호관':
    a = datetable("407")
    datetableset = pd.concat([a], axis=1)

    datetableset.columns = [['407', '407'], ['Hour', 'Min']]

if collage == '의과대학' and hall == '본관':
    a = datetable("114")
    b = datetable("115")
    c = datetable("116")
    d = datetable("117")
    datetableset = pd.concat([a, b, c, d], axis=1)

    datetableset.columns = [['114', '114', '115', '115', '116', '116', '117', '117'],
                            ['Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min']]

if collage == '치과대학' and hall == '2호관':
    a = datetable("103")
    b = datetable("206")
    c = datetable("207")
    d = datetable("209")
    datetableset = pd.concat([a, b, c, d], axis=1)

    datetableset.columns = [['103', '103', '206', '206', '207', '207', '209', '209'],
                            ['Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min']]

if collage == '치과대학' and hall == '4호관':
    a = datetable("115")
    b = datetable("116")
    c = datetable("209")
    d = datetable("211")
    e = datetable("212")
    f = datetable("214")
    datetableset = pd.concat([a, b, c, d, e, f ], axis=1)

    datetableset.columns = [['115', '115', '116', '116', '209', '209', '211', '211', '212', '212', '214', '214'],
                            ['Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min']]

if collage == '치과대학' and hall == '본관':
    a = datetable("401")
    datetableset = pd.concat([a], axis=1)

    datetableset.columns = [['401', '401'], ['Hour', 'Min']]

if collage == '인문대학' and hall == '1호관':
    a = datetable("101")
    b = datetable("104")
    c = datetable("118")
    d = datetable("201")
    e = datetable("202")
    f = datetable("203")
    g = datetable("205")
    h = datetable("207")
    i = datetable("209")
    j = datetable("212")
    k = datetable("213")
    l = datetable("301")
    m = datetable("302")
    n = datetable("304")
    o = datetable("306")
    p = datetable("307")
    q = datetable("308")
    r = datetable("311")
    s = datetable("401")
    t = datetable("402")
    u = datetable("403")
    v = datetable("404")
    w = datetable("405")
    x = datetable("501")
    datetableset = pd.concat([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x], axis=1)
    
    datetableset.columns = [['101', '101', '104', '104', '118', '118', '201', '201', '202', '202', '203', '203', '205', '205', '207', '207',
                            '209', '209', '212', '212', '213', '213', '301', '301', '302', '302', '304', '304', '306', '306', '307', '307',
                            '308', '308', '311', '311', '401', '401', '402', '402', '403', '403', '404', '404', '405', '405', '501', '501'],
                            ['Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min',
                            'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min',
                            'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min',
                            'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min']]

if collage == '인문대학' and hall == '2호관':
    a = datetable("104")
    b = datetable("105")
    c = datetable("106")
    d = datetable("107")
    e = datetable("109")
    f = datetable("136")
    g = datetable("308")
    h = datetable("309")
    i = datetable("312")
    j = datetable("313")
    k = datetable("412")
    l = datetable("501")
    m = datetable("502")
    n = datetable("504")
    o = datetable("505")
    p = datetable("506")
    datetableset = pd.concat([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p], axis=1)

    datetableset.columns = [['104', '104', '105', '105', '106', '106', '107', '107', '109', '109', '136', '136', '308', '308', '309', '309',
                            '312', '312', '313', '313', '412', '412', '501', '501', '502', '502', '504', '504', '505', '505', '506', '506'],
                            ['Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min',
                            'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min',
                            'Hour', 'Min', 'Hour', 'Min']]

if collage == '자연과학대학' and hall == '1호관':
    a = datetable("108")
    b = datetable("110")
    c = datetable("112")
    d = datetable("118")
    e = datetable("120")
    f = datetable("222")
    g = datetable("309")
    h = datetable("315")
    i = datetable("322")
    datetableset = pd.concat([a, b, c, d, e, f, g, h, i], axis=1)

    datetableset.columns = [['108', '108', '110', '110', '112', '112', '118', '118', '120', '120', '222', '222', '309', '309', '315', '315',
                            '322', '322'],
                            ['Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min',
                            'Hour', 'Min', 'Hour', 'Min']]

if collage == '자연과학대학' and hall == '2호관':
    a = datetable("402")
    b = datetable("405")
    c = datetable("406")
    d = datetable("407")
    e = datetable("409")
    f = datetable("410")
    datetableset = pd.concat([a, b, c, d, e, f ], axis=1)

    datetableset.columns = [['402', '402', '405', '405', '406', '406', '407', '407', '409', '409', '410', '410'],
                            ['Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min']]

if collage == '자연과학대학' and hall == '3호관':
    a = datetable("111")
    b = datetable("113")
    c = datetable("211")
    d = datetable("212")
    e = datetable("301")
    f = datetable("308")
    datetableset = pd.concat([a, b, c, d, e, f ], axis=1)

    datetableset.columns = [['111', '111', '113', '113', '211', '211', '212', '212', '301', '301', '308', '308'],
                            ['Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min']]

if collage == '자연과학대학' and hall == '4호관':
    a = datetable("112")
    b = datetable("114")
    c = datetable("215")
    d = datetable("226")
    e = datetable("312")
    f = datetable("314")
    g = datetable("318")
    datetableset = pd.concat([a, b, c, d, e, f, g], axis=1)

    datetableset.columns = [['112', '112', '114', '114', '215', '215', '226', '226', '312', '312', '314', '314', '318', '318'],
                            ['Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min']]

if collage == '자연과학대학' and hall == '5호관':
    a = datetable("213")
    b = datetable("214")
    c = datetable("216")
    d = datetable("217")
    e = datetable("317")
    f = datetable("320")
    g = datetable("419")
    h = datetable("422")
    datetableset = pd.concat([a, b, c, d, e, f, g, h], axis=1)

    datetableset.columns = [['213', '213', '214', '214', '216', '216', '217', '217', '317', '317', '320', '320', '419', '419', '422', '422'],
                        ['Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min']]

if collage == '자연과학대학' and hall == '본관':
    a = datetable("126")
    b = datetable("221")
    c = datetable("226")
    d = datetable("227")
    e = datetable("328")
    f = datetable("329")
    g = datetable("421")
    h = datetable("426")
    i = datetable("517")
    j = datetable("525")
    datetableset = pd.concat([a, b, c, d, e, f, g, h, i, j], axis=1)

    datetableset.columns = [['126', '126', '221', '221', '226', '226', '227', '227', '328', '328', '329', '329', '421', '421', '426', '426',
                            '517', '517', '525', '525'],
                            ['Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min',
                            'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min']]

if collage == '학술문화관':
    a = datetable('103')
    b = datetable('104')
    c = datetable('105')
    datetableset = pd.concat([a, b, c], axis=1)

    datetableset.columns = [['103', '103', '104', '104', '105', '105'], ['Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min']]

if collage == '정보전산원' :
    a = datetable('203')
    datetableset = pd.concat([a], axis=1)

    datetableset.columns = [['203', '203'], ['Hour', 'Min']]

if collage == '진수당':
    a = datetable('201')
    b = datetable('203')
    c = datetable('205')
    d = datetable('207')
    e = datetable('301')
    f = datetable('302')
    g = datetable('303')
    h = datetable('304')
    i = datetable('351')
    j = datetable('352')
    k = datetable('353')
    l = datetable('401')
    m = datetable('402')
    n = datetable('404')
    o = datetable('501')
    p = datetable('502')
    q = datetable('503')
    r = datetable('504')
    s = datetable('B01')
    datetableset = pd.concat([a, b, c, d, e, f, g, h, i ,j ,k ,l ,m, n, o, p, q, r, s], axis=1)

    datetableset.columns = [['201', '201', '203', '203', '205', '205', '207', '207', '301', '301', '302', '302', '303', '303', '304', '304',
                            '351', '351', '352', '352', '353', '353', '401', '401', '402', '402', '404', '404', '501', '501', '502', '502',
                            '503', '503', '504', '504', 'B01', 'B01'],
                            ['Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min',
                            'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min',
                            'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min']]

if collage == '체육관':
    a = datetable('101')
    b = datetable('121')
    c = datetable('301')
    datetableset = pd.concat([a, b, c], axis=1)

    datetableset.columns = [['101', '101', '121', '121', '301', '301'], ['Hour', 'Min', 'Hour', 'Min', 'Hour', 'Min']]

if collage == '학술림관리사' :
    a = datetable('201')
    datetableset = pd.concat([a], axis=1)

    datetableset.columns = [['201', '201'], ['Hour', 'Min']]

if collage == '학습도서관':
    a = datetable('202')
    b = datetable('203')
    datetableset = pd.concat([a, b], axis=1)

    datetableset.columns = [['202', '202', '203', '203'], ['Hour', 'Min', 'Hour', 'Min']]

st.dataframe(datetableset.T)


# 예약

st.header('Reserve')

st.write('학과번호는 학교 홈페이지에 게시된 학과 전화번호 뒤 4자리수 입니다.')
st.write('전화번호가 두개 이상인 경우 첫번째 전화번호가 학과번호입니다.')
st.write('예약시간은 최대 2시간 입니다. 2시간 이상을 예약하고 싶으시다면 한 번 더 예약해주세요.')

departmentN = [{'간호학과': '4682',
              '융합기술공학부 IT응용시스템공학': '4773',
              'IT지능정보공학과': '2410',
              '건축공학과': '2276',
              '고분자섬유나노공학부 고분자나노공학': '2335',
              '기계공학과': '2316',
              '기계설계공학부 기계설계공학전공': '2452',
              '기계설계공학부 나노바이오기계시스템공학전공': '2339',
              '기계시스템공학부': '2367',
              '도시공학과': '4051',
              '바이오메디컬공학부': '4063',
              '사회기반공학과': '4784',
              '산업정보시스템공학과': '2327',
              '소프트웨어공학과': '4541',
              '신소재공학부 금속시스템공학전공': '2286',
              '신소재공학부 전자재료공학전공': '2378',
              '신소재공학부 정보소재공학전공': '3969',
              '양자시스템공학과': '4997',
              '고분자섬유나노공학부 유기소재섬유공학': '2349',
              '융합기술공학부 IT융합기전공학': '4225',
              '토목환경자원에너지공학부 자원에너지공학': '2358',
              '전기공학과': '2389',
              '전자공학부': '2475',
              '컴퓨터공학부': '3431',
              '토목환경자원에너지공학부 토목공학': '2420',
              '항공우주공학과': '2468',
              '화학공학부': '2431',
              '토목환경자원에너지공학부 환경공학': '2441',
              '국제인문사회학부': '4688',
              '국제이공학부': '5586',
              '공공인재학부': '4704',
              '융합학부': '5604',
              '농경제유통학부 농업경제학전공': '2532',
              '농경제유통학부 식품유통학전공': '4165',
              '농생물학과': '2524',
              '동물생명공학과': '4748',
              '동물자원과학과': '2604',
              '목재응용과학과': '2621',
              '산림환경과학과': '2583',
              '생명자원융합학과': '4956',
              '생물산업기계공학과': '2613',
              '생물환경화학과': '2541',
              '식품공학과': '2565',
              '원예학과': '2574',
              '작물생명과학과': '2506',
              '조경학과': '2594',
              '지역건설공학과': '2515',
              '과학교육학부 물리교육전공': '2774',
              '과학교육학부 생물교육전공': '2782',
              '과학교육학부 지구과학교육전공': '2801',
              '과학교육학부 화학교육전공': '2810',
              '교육학과': '2739',
              '국어교육과': '2711',
              '독어교육과': '2720',
              '수학교육과': '2791',
              '역사교육과': '2765',
              '영어교육과': '2728',
              '윤리교육과': '2753',
              '일반사회교육과': '2765',
              '지리교육과': '2731',
              '체육교육과': '2849',
              '사회복지학과': '2962',
              '사회학과': '2916',
              '신문방송학과': '2952',
              '심리학과': '2925',
              '정치외교학과': '2934',
              '행정학과': '2943',
              '경영학과': '2986',
              '경제학부': '3001',
              '무역학과': '3009',
              '회계학과': '3023',
              '식품영양학과': '3855',
              '아동학과': '3835',
              '의류학과': '3845',
              '주거환경학과': '3632',
              '수의예과': '3425',
              '수의학과': '0911',
              '약학과': '5637',
              '무용학과': '3746',
              '미술학과': '3726',
              '산업디자인학과': '3755',
              '음악과': '3736',
              '한국음악학과': '3716',
              '의예과': '5290',
              '고고문화인류학과': '3283',
              '국어국문학과': '3166',
              '독일학과': '3181',
              '문헌정보학과': '3253',
              '사학과': '3224',
              '스페인중남미학과': '3275',
              '영어영문학과': '3199',
              '일본학과': '3261',
              '중어중문학과': '3215',
              '철학과': '3239',
              '프랑스아프리카학과': '3190',
              '과학학과': '3433',
              '물리학과': '3321',
              '반도체과학기술학과': '3971',
              '분자생물학과': '3338',
              '생명과학과': '3351',
              '수학과': '3364',
              '스포츠과학과': '2819',
              '지구환경과학과': '3393',
              '통계학과': '3380',
              '화학과': '3406',
              '치의예과': '4200',
              '생명공학부': '0848',
              '생태조경디자인학과': '0735',
              '한약자원학과': '0741',
              '스마트팜학과': '2555'}]

data = pd.DataFrame(departmentN)
data = data.T

number = st.text_input('학과번호를 입력하세요', max_chars=4)
if st.button("Login", key='number'):
    if (data[0]==number).any():
        department = data.index[data[0] == number]
        st.success(department + "님 환영합니다!")
    else:
        st.error("해당하는 학과가 없습니다.")

if (data[0]==number).any():
    collage = st.selectbox("원하는 대학을 선택하세요.",
                            ["간호대학",
                            "공과대학",
                            "과학관",
                            "글로벌인재관",
                            "농업생명과학대학",
                            "뉴실크로드센터",
                            "미술관",
                            "생활과학대학",
                            "사범대 본관",
                            "사회과학대학",
                            "상과대학",
                            "법학전문대학원",
                            "예술대학",
                            "예체능관",
                            "의과대학",
                            "치과대학",
                            "인문대학",
                            "자연과학대학",
                            "학술문화관",
                            "정보전산원",
                            "진수당",
                            "체육관",
                            "학술림관리사",
                            "학습도서관"])

    hall = ''

    if collage in '간호대학':
        room = st.selectbox("원하는 호실을 선택하세요.",
                        ["201","202",'303','306','307','312','401','403','405','407','416','422','501'])
    
    if collage in "공과대학":
        hall = st.selectbox("원하는 호관을 선택하세요.",
                        ["1호관",
                        "2호관", 
                        "3호관",
                        "4호관",
                        "5호관",
                        "6호관",
                        "7호관",
                        "8호관",
                        "9호관",
                        "부속공장"])

        if hall == '1호관':
            room = st.selectbox("원하는 호실을 선택하세요.",
                          ["122","123","130","146","147","149","158","161","219","224","225","234","246","249","302","303","315","317","321","322","328","340"])
        elif hall == '2호관':
            room = st.selectbox("원하는 호실을 선택하세요.",
                          ["104","105","116","117","403","404","405","416","417","418" ])
      
        elif hall == '3호관':
            room = st.selectbox("원하는 호실을 선택하세요.",
                          ["103","104","108","306","309","310","311","401","403","404","406","408","409","410","411"])

        elif hall == '4호관':
            room = st.selectbox("원하는 호실을 선택하세요.",
                          ["002","004","126","315","401","402","403","405","418","419"])

        elif hall == '5호관':
            room = st.selectbox("원하는 호실을 선택하세요.",
                          ["302","303","311","312","314","414","503","507","509","513"])

        elif hall == '6호관':
            room = st.selectbox("원하는 호실을 선택하세요.",
                          ["309","310","312","318","407","508","509","516","517","B11","111","B12","B13","B14","B15","B16","B17","B18"])

        elif hall == '7호관':
            room = st.selectbox("원하는 호실을 선택하세요.",
                          ["102","105","110","112","114","124","202","204","206","227","228","301","302","330","403","534"])

        elif hall == '8호관':
            room = st.selectbox("원하는 호실을 선택하세요.",
                          ["208","212","213","301","302","303","304","310","402","403","406","408"])

        elif hall == '9호관':
            room = st.selectbox("원하는 호실을 선택하세요.",
                          ["202","203","204","205","206","301","302","303","306","307","913","914","915","916"])

        elif hall == '부속공장':
            room = st.selectbox("원하는 호실을 선택하세요.",
                          ["101","103","201","206"])

    if collage in '과학관':
        room = st.selectbox("원하는 호실을 선택하세요.",
                        ["109","111","127","128","129","131","227","319","401","402","404","408","409","411","413","414","415","PH02"])

    if collage in '글로벌인재관':
        room = st.selectbox("원하는 호실을 선택하세요.",
                        ["107","123","124","125","206","207","217","218","219","220"])

    if collage in "농업생명과학대학":
        hall = st.selectbox("원하는 호관을 선택하세요.",
                        ["1호관",
                        "2호관", 
                        "3호관",
                        "4호관",
                        "본관"])
        if hall == '1호관':
            room = st.selectbox("원하는 호실을 선택하세요.",
                          ["209","301","303","309"])
      
        if hall == '2호관':
            room = st.selectbox("원하는 호실을 선택하세요.",
                          ["216","217", "219", "222", "318", "326", "401", "402", "403", "404", "405", "411", "412","100"])

        if hall == '3호관':
            room = st.selectbox("원하는 호실을 선택하세요.",
                          ["312","316","317","402","405","406","408","409","410","411","415","416"])

        if hall == '4호관':
            room = st.selectbox("원하는 호실을 선택하세요.",
                          ["120","224","301","323","324","401","402","403","419","422","423"])

        if hall == '본관':
            room = st.selectbox("원하는 호실을 선택하세요.",
                          ["104","106","107","207","217","218","302","402","403","414","423"])

    if collage in '뉴실크로드센터':
        room = st.selectbox("원하는 호실을 선택하세요.",
                        ["201","501","502","504","505","506","510","511","512","513","609","610","611","612"])

    if collage in '미술관':
        room = st.selectbox("원하는 호실을 선택하세요.",
                        ["1020","1100","1110","1230","2010","2040","2050","2060","2070","2090","2110","3030"])

    if collage in '생활과학대학':
        room = st.selectbox("원하는 호실을 선택하세요.",
                        ["110","116","118","216","308","310","312","314","316","407","408","412","414","415","418","507","508"])

    if collage in '사범대':
        room = st.selectbox("원하는 호실을 선택하세요.",
                        ["104","105","109","110","312","315","401","412","415","501","502","503","504","505","506","508","509"])

    if collage in '사회과학대학':
        room = st.selectbox("원하는 호실을 선택하세요.",
                        ["102","105","108","111","113","217","219","220","223","315","317","318","319","414","416","418","420","509","510","511"])

    if collage in "상과대학":
        hall = st.selectbox("원하는 호관을 선택하세요.",
                        ["1호관",
                        "2호관", 
                        "3호관"])

        if hall == '1호관':
            room = st.selectbox("원하는 호실을 선택하세요.",
                          ["110","122","201","202","203","205","206","301","302","402","403","405","406"])
      
        if hall == '2호관':
            room = st.selectbox("원하는 호실을 선택하세요.",
                          ["109","110","111","310","312","313"])
                          
        if hall == '3호관':
            room = st.selectbox("원하는 호실을 선택하세요.",
                          ["104","105","201","202","203","204"])

    if collage in '법학전문대학원':
        room = st.selectbox("원하는 호실을 선택하세요.",
                        ['101'])

    if collage in "예술대학":
        hall = st.selectbox("원하는 호관을 선택하세요.",
                        ["2호관",
                        "본관"])

        if hall == '2호관':
            room = st.selectbox("원하는 호실을 선택하세요.",
                          ["1070","1080","1081","1111","1112","1121","1122","1131","1132","1141","1142","1181","1182","1183","1184","1190","2010","2090","2110","3010","3070","3080","3090","3100","3110","3150","3280","4030"])

        if hall == '본관':
            room = st.selectbox("원하는 호실을 선택하세요.",
                          ["1030","1070","1080","1090","1130","1140","1160","1191","1230","1260","2070","2080","2090","2110","2140","2180","3040","3070","3080","3110","3120","3170","3190","4031","4051","4070","4080","4100","4120","4140","4150","4160","4180","4190","5020","5050","5070","5080","5090","5100"])

    if collage in '예체능관':
        room = st.selectbox("원하는 호실을 선택하세요.",
                        ["111","114","216","219","301","304","307","309","311","316","318","319","320","321","322","323","324","325","326","328","329","330","331","332"])

    if collage in "의과대학":
        hall = st.selectbox("원하는 호관을 선택하세요.",
                        ["2호관",
                        "본관"])

        if hall == '2호관':
            room = st.selectbox("원하는 호실을 선택하세요.",
                          ['407'])
                          
        if hall == '본관':
            room = st.selectbox("원하는 호실을 선택하세요.",
                          ['114','115','116','117'])

    if collage in "치과대학":
        hall = st.selectbox("원하는 호관을 선택하세요.",
                        ["2호관",
                        "4호관",
                        "본관"])
        if hall == '2호관':
            room = st.selectbox("원하는 호실을 선택하세요.",
                          ["103","207","206","209"])

        if hall == '4호관':
            room = st.selectbox("원하는 호실을 선택하세요.",
                          ["115","116","209","211","212","214"])
                          
        if hall == '본관':
            room = st.selectbox("원하는 호실을 선택하세요.",
                          ['401'])

    if collage in "인문대학":
        hall = st.selectbox("원하는 호관을 선택하세요.",
                        ["1호관",
                        "2호관"])

        if hall == '1호관':
            room = st.selectbox("원하는 호실을 선택하세요.",
                          ["101","104","118","201","202","203","205","207","209","212","213","301","302","304","306","307","308","311","401","402","403","404","405","501"])
                          
        if hall == '2호관':
            room = st.selectbox("원하는 호실을 선택하세요.",
                          ["104","105","106","107","109","136","308","309","312","313","412","501","502","504","505","506"])

    if collage in "자연과학대학":
        hall = st.selectbox("원하는 호관을 선택하세요.",
                        ["1호관",
                        "2호관", 
                        "3호관",
                        "4호관",
                        "5호관",
                        "본관"])

        if hall == '1호관':
            room = st.selectbox("원하는 호실을 선택하세요.",
                          ["108","110","112", "118","120","222" ,"309" ,"315" ,"322"])
                          
        if hall == '2호관':
            room = st.selectbox("원하는 호실을 선택하세요.",
                          ["402","405","406", "407","409", "410"])

        if hall == '3호관':
            room = st.selectbox("원하는 호실을 선택하세요.",
                          ["111","113","211","212","301","308"])

        if hall == '4호관':
            room = st.selectbox("원하는 호실을 선택하세요.",
                          ["112","114","215","226","312","314","318"])

        if hall == '5호관':
            room = st.selectbox("원하는 호실을 선택하세요.",
                          ["213","214","216","217","317","320","419","422"])
                          
        if hall == '본관':
            room = st.selectbox("원하는 호실을 선택하세요.",
                          ["126","221","226","227","328","329","421","426","517","525"])

    if collage in '학술문화관':
        room = st.selectbox("원하는 호실을 선택하세요.",
                        ['103','104','105'])

    if collage in '정보전산원':
        room = st.selectbox("원하는 호실을 선택하세요.",
                        ['정보전산원'])

    if collage in '진수당':
        room = st.selectbox("원하는 호실을 선택하세요.",
                        ["201", "203", "205", "207", "301", "302", "303", "304", "351", "352", "353", "401", "402", "404", "501", "502", "503", "504", "B01"])

    if collage in '체육관':
        room = st.selectbox("원하는 호실을 선택하세요.",
                            ['101','121','301'])

    if collage in '학술림관리사':
        room = st.selectbox("원하는 호실을 선택하세요.",
                            ['학술림관리사'])

    if collage in '학습도서관':
        room = st.selectbox("원하는 호실을 선택하세요.",
                            ['202', '203'])
    
    d = st.date_input("날짜를 입력하세요")
    
    def what_day_is_it(date):
        days = ['월', '화', '수', '목', '금', '토', '일']
        day = date.weekday()
        return days[day]

    s_t = st.time_input("시작할 시간을 입력하세요")

    Y_reserve = d.strftime("%Y")
    M_reserve = d.strftime("%m")
    D_reserve = d.strftime("%d")
    whendate = what_day_is_it(d)

    H_s = s_t.strftime("%H")
    M_s = s_t.strftime("%M")

    e_t = st.time_input("끝나는 시간을 입력하세요")

    H_e = e_t.strftime("%H")
    M_e = e_t.strftime("%M")
    
    ddd = Y_reserve + M_reserve + D_reserve

# collage, hall, room, d, s_t, e_t

    uppend = {}

    if st.button("Submit"):
        if ((int(H_s)<8) or (int(H_e)<8)) or ((int(H_s)>=22) or (int(H_e)>=22)):
            st.error("해당 시간에는 예약이 불가능합니다.")
        else:
            if int(H_s) == int(H_e):
                if (int(M_e) > 30) and (int(M_s) < 30): # A B 생성
                    uppend = {'강의실': collage + hall + room, '시간': whendate + ' ' + str(int(H_s)-8) + '-A, ' + whendate + ' ' + str(int(H_s)-8) + '-B',
                    '날짜': ddd}
                elif int(M_s) == int(M_e):
                    st.error("시간을 입력해주세요.")
                elif int(M_e) <= 30: # A
                    uppend = {'강의실': collage + hall + room, '시간': whendate + ' ' + str(int(H_s)-8) + '-A',
                    '날짜': ddd}
                else:
                    uppend = {'강의실': collage + hall + room, '시간': whendate + ' ' + str(int(H_s)-8) + '-B',
                    '날짜': ddd}
            elif (int(H_e) - int(H_s)) == 1:
                if int(M_e) == 0:
                    uppend = {'강의실': collage + hall + room, '시간': whendate + ' ' + str(int(H_s)-8) + '-A, ' + whendate + ' ' + str(int(H_s)-8) + '-B',
                    '날짜': ddd}
                elif int(M_e) <= 30:
                    uppend = {'강의실': collage + hall + room,
                            '시간': whendate+' '+str(int(H_s)-8)+'-A, '+whendate+' '+str(int(H_s)-8)+'-B, '+ whendate+' '+str(int(H_s)-8)+'-A',
                            '날짜': ddd}
                else:
                    uppend = {'강의실': collage + hall + room,
                            '시간': whendate+' '+str(int(H_s)-8)+'-A, '+whendate+' '+str(int(H_s)-8)+'-B, '+ whendate+' '+str(int(H_s)-8)+'-A, '+whendate+' '+str(int(H_e)-8)+'-B',
                            '날짜': ddd}
            elif ((int(H_e) - int(H_s)) == 2) and (int(M_e) == int(M_s)):
                uppend = {'강의실': collage + hall + room,
                        '시간': whendate+' '+str(int(H_s)-8)+'-A, '+whendate+' '+str(int(H_s)-8)+'-B, '+ whendate+' '+str(int(H_s)-7)+'-A, '+whendate+' '+str(int(H_s)-7)+'-B',
                        '날짜': ddd}
            else:
                st.error("2시간 이상 예약은 불가능합니다. 2시간 이내로 선택해주세요.")
            
    if uppend:
        uppend = pd.DataFrame(uppend, index=[0])
        df = pd.concat([df, uppend], ignore_index=True)
        st.dataframe(df.tail(5))
