from django.shortcuts import render
from .models import Review

def list(request):
    list_object = {}
    
    review_object = Review.objects.all().order_by('-id')
    list_object['objects'] = review_object

    return render(request, 'review/list.html', list_object)