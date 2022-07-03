from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.contrib.auth import login as login_user
from records.models import Record
from records.serializer import RecordSerializer, FindImageSerializer
from rest_framework.decorators import api_view

User = get_user_model()


@login_required(login_url=reverse_lazy("login"))
@api_view(["GET", "POST"])
def home(request):
    context = {}
    if request.method == "POST":
        serializer = FindImageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        context["data"] = serializer.validated_data
        # print(serializer.validated_data)
    return render(request, "records/home.html", context=context)


@login_required(login_url=reverse_lazy("login"))
@api_view(["POST"])
def add_new(request):
    serializer = RecordSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return HttpResponseRedirect(reverse("home"))


@login_required(login_url=reverse_lazy("login"))
@api_view(["GET"])
def details(request, ref_no):
    try:
        record = Record.objects.get(id=ref_no)
    except Record.DoesNotExist:
        return HttpResponseNotFound("Record not found with reference no. " + str(ref_no))

    print(record.images)
    return render(request, "records/details.html", context=dict(record=record))


def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("home"))

    context = {}
    if request.method == "POST":
        data = request.POST
        username_or_email = data.get("username_or_email", "")
        password = data.get("password", "")
        remember_me = data.get("remember_me", False)

        try:
            user = User.objects.get(
                Q(email=username_or_email) | Q(username=username_or_email)
            )
            if user.check_password(password):
                login_user(request, user)
                if not remember_me:
                    request.session.set_expiry(0)
                return HttpResponseRedirect(reverse("home"))
        except User.DoesNotExist:
            pass

        context["error_message"] = "Invalid credentials provided"

    return render(request, "records/login.html", context=context)
