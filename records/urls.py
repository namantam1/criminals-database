from django.urls import path

from records.views import add_new, details, home, login


urlpatterns = [
    path("", home, name="home"),
    path("details/<int:ref_no>", details, name="details"),
    path("add-new/", add_new, name="add-new"),
    path("login/", login, name="login"),
]