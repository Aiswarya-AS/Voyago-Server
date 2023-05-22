from django.urls import path
from . import views

urlpatterns = [
    path("users/", views.users, name="users"),
    path("destinations/", views.destinations, name="destination"),
    path("guides/", views.guides, name="guide"),
    path("orders/", views.orders, name="orders"),
    path("admin_login/", views.admin_login, name="admin_login"),
    path("admin_wallet/", views.admin_wallet, name="admin_wallet"),
    path("block_user/<int:id>", views.block_user, name="block_user"),
    path("block_guide/<int:id>", views.block_guide, name="block_guide"),
    path("add_destination", views.add_destination, name="add_destination"),
    path("edit_destination/<int:id>", views.edit_destination, name="edit_destination"),
    path(
        "update_destination/<int:id>",
        views.update_destination,
        name="update_destination",
    ),
    path("accept_guide/<int:id>", views.accept_guide, name="accept_guide"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path('destination_delete/<int:id>', views.destination_delete, name='destination_delete'),
    path('userSearch/<str:query>', views.userSearch, name='userSearch')
]
