from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path("", views.HomeView, name="home"),
    path("profile/<str:username>/", views.ProfileView, name="profile"),
    path("slots/", views.SlotsView, name="slots"),
    path("add-slot/", views.AddSlotView, name="add_slot"),
    path("get-slot/", views.GetSlotView, name="get_slot"),
    path("get-slot2/", views.GetSlotView2, name="get_slot2"),    
    path("delete-slot/", views.DeleteSlotView, name="delete_slot"),


    path("reserve/", views.ReserveView, name="reserve"),
    path('login/', auth_views.LoginView.as_view(template_name='myapp/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),

    path('search-subjects/', views.SearchSubjects, name='search_subjects'),
    path('reserve-slot/', views.ReserveSlotView, name='reserve_slot'),
    path('get-schedules/', views.GetSchedulesView, name='get_schedules'),
]
