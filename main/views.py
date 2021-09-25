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
