<<<<<<< HEAD
from .models import CrollData
from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
import threading
import time

def index(request):
    crolldata = CrollData.objects.all()
    crolldata.delete()
    req = requests.get('https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&qvt=0&query=%EC%BD%94%EB%A1%9C%EB%82%9819%EB%B0%B1%EC%8B%A0%ED%98%84%ED%99%A9')
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    data = {}

    datas = soup.select("#_cs_vaccine_info > div > div.main_tab_area > div > div > div > div:nth-child(1) > dl > dd > strong.value")
    for title in datas:
        print(title.text)
        data["accumulate1"] = title.text

    datas = soup.select("#_cs_vaccine_info > div > div.main_tab_area > div > div > div > div:nth-child(2) > dl > dd > strong.value")
    for title in datas:
        print(title.text)
        data["new1"] = title.text

    datas = soup.select("#_cs_vaccine_info > div > div.main_tab_area > div > div > div > div:nth-child(1) > dl > dd > span > span.total > i.num")
    for title in datas:
        print(title.text)
        data["accumulate2"] = title.text
    
    datas = soup.select("#_cs_vaccine_info > div > div.main_tab_area > div > div > div > div:nth-child(2) > dl > dd > span > span.total > i.num")
    for title in datas:
        print(title.text)
        data["new2"] = title.text

    for t, l in data.items():
        CrollData(title=t, link=l).save()

    
    list_object = {}

    crolldata = CrollData.objects.all()
    list_object['crollData'] = crolldata

    return render(request, "main/index.html", list_object)
=======
# -*- coding: utf-8 -*-
from base64 import encode
from re import M
from bokeh.models.scales import LinearScale
from bokeh.util.serialization import encode_base64_dict
from numpy import source
import pandas as pd
import json
from bokeh.models import HoverTool
from bokeh.embed import components
from bokeh.plotting import figure, show
from bokeh.themes import built_in_themes
from bokeh.models import ColumnDataSource
from bokeh.io import curdoc
from django.shortcuts import render
from bokeh.models.annotations import Tooltip


def index(request):
    # # x = [1, 2, 3, 4, 5]
    # # y = [4, 5, 5, 7, 2]
    df = pd.read_excel("./static/data/29.xlsx", sheet_name="이상반응 분류별 신고 현황")
    df1 = pd.read_excel("./static/data/29.xlsx", sheet_name="변경사망 현황")
    legend = list(df.head())
    # p = figure(sizing_mode="stretch_width", max_width=500,
    #            height=250, tooltips=TOOLTIPS)
    # # add a renderer
    # p.line(x, y, legend_label="A")
    # p.circle(x, y, fill_color="white", size=10)

    x = legend[2:]
    y = list(df.iloc[3][2:])

    def vbar(x, y, label, title):
        TOOLTIPS = [
            ("x", "@x"),
            ("y", "@y"),
        ]
        p = figure(x_range=x, height=300, title=f"{label} {title}",
                   toolbar_location=None, tooltips=TOOLTIPS)
        p.vbar(x=x, top=y, width=0.9, legend_label=label)
        p.xgrid.grid_line_color = None
        p.y_range.start = 0

        return p

    y, x = df1.iloc[7][1:], list(df1.head())[1:]
    da = vbar(x, y, "아스트라제네카", "사망 현황")
    y, x = df1.iloc[8][1:], list(df1.head())[1:]
    dp = vbar(x, y, "화이자", "사망 현황")
    y, x = df1.iloc[9][1:], list(df1.head())[1:]
    dm = vbar(x, y, "모더나", "사망 현황")
    y, x = df1.iloc[10][1:], list(df1.head())[1:]
    dj = vbar(x, y, "얀센", "사망 현황")

    da_script, da_div = components(da)
    dp_script, dp_div = components(dp)
    dm_script, dm_div = components(dm)
    dj_script, dj_div = components(dj)

    title = "백신별 사망 현황"
    context = {

        "da_script": da_script, "da_div": da_div,
        "dp_script": dp_script, "dp_div": dp_div,
        "dm_script": dm_script, "dm_div": dm_div,
        "dj_script": dj_script, "dj_div": dj_div,
        "title": title}

    return render(request, "main/index.html", context=context)


def info1(request):
    # # x = [1, 2, 3, 4, 5]
    # # y = [4, 5, 5, 7, 2]
    df = pd.read_excel("./static/data/29.xlsx", sheet_name="이상반응 분류별 신고 현황")
    df1 = pd.read_excel("./static/data/29.xlsx", sheet_name="변경사망 현황")
    legend = list(df.head())
    # p = figure(sizing_mode="stretch_width", max_width=500,
    #            height=250, tooltips=TOOLTIPS)
    # # add a renderer
    # p.line(x, y, legend_label="A")
    # p.circle(x, y, fill_color="white", size=10)

    x = legend[2:]
    y = list(df.iloc[3][2:])

    def vbar(x, y, label, title):
        TOOLTIPS = [
            ("x", "@x"),
            ("y", "@y"),
        ]
        p = figure(x_range=x, height=300, title=f"{label} {title}",
                   toolbar_location=None, tooltips=TOOLTIPS)
        p.vbar(x=x, top=y, width=0.9, legend_label=label)
        p.xgrid.grid_line_color = None
        p.y_range.start = 0

        return p
    a = vbar(x, y, "아스트라제네카", "이상 반응 신고 현황")
    y = list(df.iloc[6][2:])
    p = vbar(x, y, "화이자", "이상 반응 신고 현황")
    y = list(df.iloc[9][2:])
    m = vbar(x, y, "모더나", "이상 반응 신고 현황")
    y = list(df.iloc[12][2:])
    j = vbar(x, y, "얀센", "이상 반응 신고 현황")

    #p.y_range.start = 0

    # show the results
    a_script, a_div = components(a)
    p_script, p_div = components(p)
    m_script, m_div = components(m)
    j_script, j_div = components(j)

    title = "백신별 이상 반응 신고 현황"

    context = {
        "a_script": a_script, "a_div": a_div,
        "p_script": p_script, "p_div": p_div,
        "m_script": m_script, "m_div": m_div,
        "j_script": j_script, "j_div": j_div,
        "title": title
    }

    return render(request, "main/index.html", context=context)
>>>>>>> 3f3d1eab19cb97aeeee8d628f82065f4583599ba
