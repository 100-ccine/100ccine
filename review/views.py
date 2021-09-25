from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator
from django.utils import timezone
from django.contrib import messages
from .models import Review, Comment, CrollData
from .forms import ReviewForm, CommentForm
import requests
from bs4 import BeautifulSoup
import threading
import time


def list(request):
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

    datas = soup.select("#_cs_vaccine_info > div > div.main_tab_area > div > div > div > div:nth-child(1) > dl > dd > span > span.diff > i.num")
    for title in datas:
        print(title.text)
        data["new1"] = title.text

    datas = soup.select("#_cs_vaccine_info > div > div.main_tab_area > div > div > div > div:nth-child(2) > dl > dd > span > span.total > i.num")
    for title in datas:
        print(title.text)
        data["accumulate2"] = title.text
    
    datas = soup.select("#_cs_vaccine_info > div > div.main_tab_area > div > div > div > div:nth-child(2) > dl > dd > span > span.diff > i.num")
    for title in datas:
        print(title.text)
        data["new2"] = title.text

    for t, l in data.items():
        CrollData(title=t, link=l).save()

    list_object = {}

    crolldata = CrollData.objects.all()
    list_object['crollData'] = crolldata

    
    review_object = Review.objects.all().order_by('-id')
    list_object['objects'] = review_object

    page = int(request.GET.get('p', 1))
    pagenator = Paginator(review_object, 10)
    list_object['page'] = pagenator.get_page(page)

    return render(request, 'review/list.html', list_object)


def detail(request, id):
    review_object = get_object_or_404(Review, pk = id)
    comments = Comment.objects.filter(board=id)

    context={}
    context['review_object']=review_object

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comments = comment_form.save(commit=False)
            text = comment_form.cleaned_data['text']
            comments.board = review_object
            comments.pub_date = timezone.now()
            comments.free_id = id
            comments.writer = request.user
            comments.save()
            print(text)
            return redirect('/review/' + str(review_object.id))
        
    else:
        comment_form = CommentForm()

    context['comments'] = comments
    context['comment_form'] = comment_form


    if request.method == 'POST':
        comment_form = CommentForm(request.POST)

        

    return render(request, "review/detail.html", context)

def write(request):
    return render(request, "review/write.html")

def create(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            online = form.save(commit=False)
            online.writer = request.user #수정
            online.pub_date = timezone.now()
            online.save()
            return redirect('review:list')
        
    else:
        form = ReviewForm()
    
    context = {'form':form}

    return render(request, 'review/write.html', context)

def edit(request, id):
    edit_object = get_object_or_404(Review, pk = id)

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=edit_object)
        if form.is_valid():
            edit_object = form.save(commit=False)
            edit_object.writer = request.user #수정
            edit_object.pub_date = timezone.now()
            edit_object.save()
            return redirect('review:list')
        
    else:
        form = ReviewForm(instance=edit_object)
    
    context = {'form':form}
    return render(request, 'review/write.html', context)

def delete(request, id):
    delete_object = get_object_or_404(Review, pk = id)
    delete_object.delete()
    return redirect('review:list')

def comment_edit(request, review_id, comment_id):
    board = get_object_or_404(Review, id=review_id)
    comments = Comment.objects.filter(board=review_id)
    my_comment = Comment.objects.get(id=comment_id)
    comment_form = CommentForm(instance=my_comment)

    if request.method == "POST":
        update_comment_form = CommentForm(request.POST, instance=my_comment)
        if update_comment_form.is_valid():
            update_comment_form.save()

            return redirect('/review/'+str(board.id))

    context={
        'board':board,
        'comments':comments,
        'comment_form':comment_form,
        'my_comment':my_comment,
    }

    return render(request, 'review/comment_edit.html', context)

def comment_delete(request, review_id, comment_id):
    board = Review.objects.get(id=review_id)
    comment = Comment.objects.get(id=comment_id)

    # if request.session.get('name') != comment.writer :
    #     messages.warning(request, '권한없음')
    #     return redirect('/review/'+str(board.id))
    
    if request.method == "POST":
        comment.delete()
        return redirect('/review/'+str(board.id))
    
    
    context={
        'comment':comment,
        'board':board
    }
    return render(request, 'review/comment_delete.html',context)