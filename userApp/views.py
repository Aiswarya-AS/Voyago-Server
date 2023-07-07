from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User, Destination, Guide, Request, Order, Rating, UserWallet
import jwt
from .serializer import (
    DestinationSerializer,
    GuideSerializer,
    UserSerializer,
    RequestSerializer,
    LocationSerializer,
    OrderSerializer,
    RatingSerializer,
)
from django.db.models import Q
from django.conf import settings
import razorpay
import uuid
from admin1.models import AdminWallet
from guideApp.models import Otp
from django.db.models import Avg

# Create your views here.


@api_view(["POST"])
def user_register(request):
    try:
        firstname = request.data["firstname"]
        lastname = request.data["lastname"]
        # username = request.data["username"]
        email = request.data["email"]
        phone = request.data["phone"]
        password = request.data["confirmPassword"]
    except Exception:
        return Response({"status": "Please provide all the details.."})
    if User.objects.filter(phone=phone).exists():
        return Response({"status": "Phone number already exists"})
    if User.objects.filter(email=email).exists():
        return Response({"status": "Email already exists"})
    user = User.objects.create(
        firstname=firstname,
        lastname=lastname,
        email=email,
        phone=phone,
        password=password,
    )
    user.save()
    return Response({"status": "true"})


@api_view(["POST"])
def user_login(request):
    try:
        email = request.data["email"]
        password = request.data["password"]
    except Exception:
        return Response({"status": "Please provide all the details.."})
    try:
        user = User.objects.get(
            email=email, password=password, is_blocked=False)
        payload = {
            "email": user.email,
            "password": user.password,
        }
        user_id = user.id
        jwt_token = jwt.encode(payload, "secret", algorithm="HS256")
        return Response({"status": "true", "user_jwt": jwt_token, "user_id": user_id})
    except User.DoesNotExist:
        return Response({"status": "false"})


@api_view(["POST"])
def destination(request):
    query = request.data["search"]
    try:
        destination = Destination.objects.filter(
            Q(country__icontains=query)
            | Q(state__icontains=query)
            | Q(location__icontains=query)
        )
        serializer = DestinationSerializer(destination, many=True)
        return Response(serializer.data)
    except Exception:
        return Response({"Not found any place.."})


@api_view(["GET"])
def destination_details(request, id):
    try:
        destination = Destination.objects.get(id=id)
        serializer = DestinationSerializer(destination, many=False)
        return Response(serializer.data)
    except Exception:
        return Response({"Not found any place.."})


@api_view(["GET"])
def guides(request, place):
    # query = request.data['place']
    # print(place)
    try:
        guides = Guide.objects.filter(country__icontains=place)
        serializer = GuideSerializer(guides, many=True)
        return Response(serializer.data)
    except Exception:
        return Response({"Not found any guide.."})


@api_view(["GET"])
def guide_details(request, id):
    try:
        guides = Guide.objects.get(id=id)
        serializer = GuideSerializer(guides, many=False)
        return Response(serializer.data)
    except Exception:
        return Response({"Not found any guide.."})


@api_view(["GET"])
def user_profile(request, id):
    try:
        user = User.objects.get(id=id)
        try:
            user_wallet = UserWallet.objects.get(user_id=user)
        except UserWallet.DoesNotExist:
            user_wallet = UserWallet.objects.create(user_id=user)

        serializer = UserSerializer(user, many=False)
        return Response({"serdata": serializer.data, "balance": user_wallet.amount})
    except User.DoesNotExist:
        return Response({"status": "User not found"})


@api_view(["POST"])
def request(request):
    try:
        time = request.data["time"]
        print(time)
        date = request.data["date"]
        persons = request.data["persons"]
        guide_id = int(request.data["guide_id"])
        user_id = request.data["user_id"]
        guide_name = request.data["guide_name"]
        guide_place = request.data["guide_place"]
        guide_price = request.data["guide_price"]
        total_amount = int(persons) * int(guide_price)
        print(total_amount)
        location = request.data["select"]
        country = request.data["guide_country"]
        state = request.data["guide_state"]

    except Exception:
        return Response({"status": "Please provide all the details.."})
    if Request.objects.filter(user=user_id, guide=guide_id).exists():
        return Response({"status": "exists"})
    else:
        requested = Request.objects.create(
            guide_id=guide_id,
            user_id=user_id,
            date=date,
            time=time,
            total_peoples=persons,
            guide_name=guide_name,
            guide_place=guide_place,
            price=guide_price,
            total_amount=total_amount,
            location=location,
            country=country,
            state=state,
        )
        requested.save()
        return Response({"status": "true"})


@api_view(["GET"])
def user_requests(request, id):
    requests = Request.objects.filter(user=id)
    serializer = RequestSerializer(requests, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def order_recap(request, id):
    request_data = Request.objects.get(id=id)
    print(request_data.price)
    serializer = RequestSerializer(request_data, many=False)
    return Response(serializer.data)


@api_view(["POST"])
def create_order(request):
    client = razorpay.Client(
        auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET)
    )
    c = request.data
    print(c)
    amount = request.data["amount"]
    transaction_id = str(uuid.uuid4())
    guide_name = c["data"]["orderdata"]["guide_name"]
    # guide_place = c['data']['orderdata']['guide_place']
    location = c["data"]["orderdata"]["location"]
    time = c["data"]["orderdata"]["time"]
    date = c["data"]["orderdata"]["date"]
    total_peoples = c["data"]["orderdata"]["total_peoples"]
    guide = c["data"]["orderdata"]["guide"]
    user = c["data"]["orderdata"]["user"]
    request_id = c["data"]["orderdata"]["id"]
    state = c["data"]["orderdata"]["state"]
    country = c["data"]["orderdata"]["country"]
    order = Order.objects.create(
        guide_name=guide_name,
        location=location,
        date=date,
        time=time,
        total_peoples=total_peoples,
        guide_id=guide,
        user_id=user,
        payment_mode="Razorpay",
        transaction_id=transaction_id,
        state=state,
        country=country,
        total_amount=amount,
    )
    order.save()
    # Admin wallet
    user1 = User.objects.get(id=user)
    guide1 = Guide.objects.get(id=guide)
    admin_wallet = AdminWallet.objects.create(
        guide_id=guide1,
        user_id=user1,
        guide_name=guide_name,
        payment_mode="Razorpay",
        amount=amount,
    )
    admin_wallet.save()
    r = Request.objects.get(id=request_id)
    r.delete()
    return Response({"status": "true"})


@api_view(["PUT"])
def userUpdate(request, id):
    print(request.data)
    user = User.objects.get(id=id)
    first_name = request.data["firstName"]
    last_name = request.data["lastName"]
    email = request.data["email"]
    phone = request.data["phone"]
    user.firstname = first_name
    user.lastname = last_name
    user.email = email
    user.phone = phone
    user.profile_pic = request.data['image']
    user.save()
    return Response({"status": "true"})


@api_view(["GET"])
def location(request):
    location = Destination.objects.all()
    serializer = LocationSerializer(location, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def request_exists(request):
    user_id = request.data["user_id"]
    guide_id = request.data["guide_id"]
    if Request.objects.filter(user=user_id, guide=guide_id).exists():
        return Response({"exists": "true"})
    else:
        return Response({"exists": "false"})


@api_view(["GET"])
def history(request, id):
    history = Order.objects.filter(user=id)
    serializer = OrderSerializer(history, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def comments(request, id):
    comments = Rating.objects.filter(guide_id=id).order_by("-is_created")
    avg_rating = Rating.objects.aggregate(
        avg_field=Avg("rating")).get("avg_field", 0)
    avg_rating = round(avg_rating, 2)
    serializer = RatingSerializer(comments, many=True)
    return Response({"comments": serializer.data, "avg": avg_rating})


@api_view(["POST"])
def addComments(request, guide_id, user_id):
    user = User.objects.get(id=user_id)
    guide_id = Guide.objects.get(id=guide_id)
    comment = Rating.objects.create(
        guide_id=guide_id,
        user_id=user,
        user_name=user.firstname,
        comment=request.data["comment"],
        rating=request.data["rating"],
    )
    comment.save()
    return Response({"status": ""})


@api_view(["PATCH"])
def resetPassword(request, id):
    currentPassword = request.data["currentPassword"]
    newPassword = request.data["newPassword"]
    try:
        user = User.objects.get(id=id, password=currentPassword)
    except User.DoesNotExist:
        return Response({"status": "Your current password is incorrect.."})
    user.password = newPassword
    user.save()
    return Response({"status": "true"})


@api_view(["POST"])
def verifyOtp(request):
    user_id = request.data["u_id"]
    guide_id = request.data["g_id"]
    otp = request.data["otp"]
    try:
        otp = Otp.objects.get(user=user_id, guide=guide_id, otp=otp)
    except:
        return Response({"status": "Invalid Otp"})
    order_id = request.data["o_id"]
    print(order_id)
    order = Order.objects.get(id=order_id)
    order.journey_status = "start"
    order.save()
    print("haaaaiiiii")
    return Response({"status": "true"})


@api_view(["POST"])
def cancelBooking(request, id, user_id):
    order = Order.objects.get(id=id)
    order.status = "Cancelled"
    order.save()
    user = User.objects.get(id=user_id)
    user_wallet = UserWallet.objects.get(user_id=user)
    balance = user_wallet.amount + order.total_amount
    user_wallet.amount = balance
    user_wallet.save()
    return Response({"status": "true"})


@api_view(["PUT"])
def endJourney(request, id):
    order = Order.objects.get(id=id)
    order.journey_status = "end"
    order.save()
    return Response({"status": "true"})


@api_view(['GET'])
def availableDates(request, id):
    pass
