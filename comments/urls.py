from django.urls import path, include
from .views import comment_thread

app_name = 'comments'
urlpatterns = [
    path('<int:pk>/', comment_thread, name='thread'),
    # path('<slug:slug>/delete/', views.post_delete),
]
