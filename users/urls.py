
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [

     path("", views.user_list, name="us_lst"),
    path("about/", views.about, name="about"),
    path('chat/<int:user_id>',views.get_and_send_user_messages,name='member'),
    path("delete/<int:post_id>",views.delete_message,name="delete"),
    
    path('accounts/profile/', views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),

    path('register/', views.register, name='register'),
    # Video call routes (basic HTTP-polling signaling)
    path('video/call/<int:user_id>/', views.video_call_create, name='video_call_create'),
    path('video/join/<uuid:room_id>/', views.video_call_join, name='video_call_join'),
    path('video/offer/<uuid:room_id>/', views.video_offer, name='video_offer'),
    path('video/answer/<uuid:room_id>/', views.video_answer, name='video_answer'),
    path('video/candidate/<uuid:room_id>/', views.video_candidate_post, name='video_candidate_post'),
    path('video/candidates/<uuid:room_id>/', views.video_candidates_get, name='video_candidates_get'),
    path('view_profile/<int:user_id>/', views.view_profile, name='view_profile'),
    path('accept-cookies/', views.accept_cookies_view, name='accept_cookies'),
    
]
