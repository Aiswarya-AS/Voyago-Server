from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.user_register, name="user_register"),
    path("user_login/", views.user_login, name="user_login"),
    path("destinations/", views.destination, name="destinations"),
    path(
        "destination_details/<int:id>/",
        views.destination_details,
        name="destinations_details",
    ),
    path("guides/<str:place>", views.guides, name="guides"),
    path("guide/<int:id>/", views.guide_details, name="guide_details"),
    # path('guide_request/',views.guide_request,name='guide_request'),
    path("request", views.request, name="request"),
    path("location", views.location, name="location"),
    path("request_exists", views.request_exists, name="request_exists"),
    path("bookingHistory/<int:id>", views.history, name="history"),
    path("user_profile/<int:id>/", views.user_profile, name="user_profile"),
    path("user_requests/<int:id>/", views.user_requests, name="request"),
    path("order_recap/<int:id>/", views.order_recap, name="order_recap"),
    path("payment", views.create_order, name="payment"),
    path("userUpdate/<int:id>", views.userUpdate, name="userupdate"),
    path("comments/<int:id>", views.comments, name="comments"),
    path(
        "addComments/<int:guide_id>/<int:user_id>",
        views.addComments,
        name="comments"
    ),
    path("resetPassword/<int:id>", views.resetPassword, name="resetPassword"),
    path("verifyOtp", views.verifyOtp, name="verifyOtp"),
    path(
        "cancelBooking/<int:id>/<int:user_id>",
        views.cancelBooking,
        name="cancelBooking",
    ),
    path('endJourney/<int:id>', views.endJourney, name='endJourney')
]
