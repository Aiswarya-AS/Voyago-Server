from rest_framework.decorators import api_view
from rest_framework.response import Response
from userApp.serializer import UserSerializer, DestinationSerializer, GuideSerializer, OrderSerializer
from userApp.models import User, Destination, Guide, Order
from django.contrib.auth.models import User as AdminUser
import jwt
import datetime
from .models import AdminWallet
from django.db.models import Sum
from django.core.mail import send_mail
from django.db.models import Count, Q
from django.contrib.auth.hashers import check_password

# Create your views here.


@api_view(["GET"])
def users(request):
    users = User.objects.all().order_by("id")
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def destinations(request):
    destination = Destination.objects.all().order_by("id")
    serializer = DestinationSerializer(destination, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def orders(request):
    orders = Order.objects.all().order_by('id')
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def guides(request):
    guide = Guide.objects.all().order_by("id")
    serializer = GuideSerializer(guide, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def admin_login(request):
    email = request.data["email"]
    password = request.data["password"]
    try:
        user = AdminUser.objects.get(email=email)
        print(user)
        if check_password(password, user.password):
            payload = {"email": user.email, "password": user.password}
            jwt_token = jwt.encode(payload, "secret", algorithm="HS256")
            return Response({"status": "true", "admin_jwt": jwt_token})
        else:
            return Response({'status': 'incorrect password'})
    except AdminUser.DoesNotExist:
        return Response({"status": "User Not Found"})


@api_view(["GET"])
def admin_wallet(request):
    wallet = AdminWallet.objects.all()
    total_revenue = AdminWallet.objects.aggregate(Sum("amount"))["amount__sum"]
    print(total_revenue)
    return Response({"total_revenue": total_revenue})


@api_view(["PATCH"])
def block_user(request, id):
    user = User.objects.get(id=id)
    if user.is_blocked:
        print("user is blocked")
        user.is_blocked = False
        user.save()
    else:
        print("user is not blocked")
        user.is_blocked = True
        user.save()

    return Response({"status": "true"})


@api_view(["PATCH"])
def block_guide(request, id):
    guide = Guide.objects.get(id=id)
    if guide.is_blocked:
        print("user is blocked")
        guide.is_blocked = False
        guide.save()
    else:
        print("guide is not blocked")
        guide.is_blocked = True
        guide.save()

    return Response({"status": "true"})


@api_view(["POST"])
def add_destination(request):
    state = request.data["state"]
    country = request.data["country"]
    location = request.data["location"]
    short_desc = request.data["short_desc"]
    description = request.data["description"]
    image = request.data["image"]
    d = Destination.objects.create(
        state=state,
        country=country,
        location=location,
        short_desc=short_desc,
        description=description,
        thumbnail=image,
    )
    return Response({"status": "true"})


@api_view(["GET"])
def edit_destination(request, id):
    d = Destination.objects.get(id=id)
    serializer = DestinationSerializer(d, many=False)
    return Response(serializer.data)


@api_view(["PUT"])
def update_destination(request, id):
    d = Destination.objects.get(id=id)
    state = request.data["state"]
    country = request.data["country"]
    location = request.data["location"]
    short_desc = request.data["short_desc"]
    description = request.data["description"]

    d.state = state
    d.country = country
    d.location = location
    d.short_desc = short_desc
    d.description = description
    d.save()
    return Response({"status": "Updated Successfully"})


@api_view(["PUT"])
def accept_guide(request, id):
    print(id)
    g = Guide.objects.get(id=id)
    # print(g.email)
    g.is_accepted = True
    g.save()
    subject = "Test Email"
    message = "This is a test email"
    email_from = "aiswaryaasubash@gmail.com"
    recipient_list = ["aiswaryaas809@gmail.com"]

    send_mail(subject, message, email_from, recipient_list)
    return Response({"status": "Successfully "})


@api_view(["GET"])
def dashboard(request):
    total_users = User.objects.filter(is_blocked=False).count()
    total_guides = Guide.objects.filter(is_accepted=True).count()
    # completed_journeys = Order.objects.filter(journey_status="ended").count()

    # monthly sales
    today = datetime.datetime.now()
    dates = (
        Order.objects.filter(is_created__month=today.month)
        .values("is_created__date")
        .annotate(items=Count("id"))
        .order_by("is_created__date")
    )
    trip_completed = (
        Order.objects.filter(is_created__month=today.month)
        .values("is_created__date")
        .annotate(completed=Count("id", filter=Q(journey_status="end")))
        .order_by("is_created__date")
    )
    started = (
        Order.objects.filter(is_created__month=today.month)
        .values("is_created__date")
        .annotate(started=Count("id", filter=Q(journey_status="start")))
        .order_by("is_created__date")
    )
    cancelled = (
        Order.objects.filter(is_created__month=today.month)
        .values("is_created__date")
        .annotate(cancelled=Count("id", filter=Q(status="Cancelled")))
        .order_by("is_created__date")
    )
    print(trip_completed)
    print(started)
    print(cancelled)
    print(dates)
    return Response(
        {
            "total_users": total_users,
            "total_guides": total_guides,
            # "completed_journeys": completed_journeys,
            # 'guide_name': guide.firstname,
            # "guide_count": guide_count["count"],
            "dates": dates,
            "trip_completed": trip_completed,
            "started": started,
            "cancelled": cancelled,
        }
    )


@api_view(['DELETE'])
def destination_delete(request, id):
    destination = Destination.objects.get(id=id)
    destination.delete()
    return Response({'status': 'true'})


@api_view(['GET'])
def userSearch(request, query):
    users = User.objects.filter(firstname__icontains=query)
    serilaizer = UserSerializer(users, many=True)
    return Response(serilaizer.data)