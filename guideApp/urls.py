from django.urls import path
from . import views
urlpatterns = [
    path('guide_signup/', views.guideSignup, name='guide_signup'),
    path('guide_login/', views.guideLogin, name='guide_login'),
    path('guide/<int:id>/', views.guide, name='guide'),
    path('guide_requests/<int:id>',
         views.guide_requests, name='guide_requests'),
    path('accept/<int:id>', views.accept, name='accept'),
    path('history/<int:id>/', views.history, name='history'),
    path('sendOtp/<int:id>/<int:guide_id>', views.sendOtp, name='sendOtp'),
    path('guideProfile/<int:id>', views.guideProfile, name='guideProfile'),
    path('withdraw/<int:id>', views.withdraw, name='withdraw')
]
