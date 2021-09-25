from . import views
from django.urls import path

app_name = 'review'

urlpatterns = [
    path('', views.list, name='list'),
    path('<int:id>/', views.detail, name='detail'),
    path('write/', views.create, name='write'),
    path('<int:id>/edit/', views.edit, name='edit'),
    path('<int:id>/delete/', views.delete, name='delete'),
    path('<int:review_id>/commment_edit/<int:comment_id>/', views.comment_edit, name='comment_edit'),
    path('<int:review_id>/commment_delete/<int:comment_id>', views.comment_delete,name='comment_delete'),
    

]