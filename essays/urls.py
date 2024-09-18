from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.EssayList.as_view()),
    path('detail/<int:pk>', views.EssayDetail.as_view()),
    path('user-views/<int:pk>', views.UserEssayView.as_view()),
]