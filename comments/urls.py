from django.urls import path, include
from .views import comment_thread, confirm_delete

app_name = 'comments'
urlpatterns = [
    path('<int:pk>/', comment_thread, name='thread'),
    path('<int:pk>/delete/', confirm_delete, name='delete'),
]
