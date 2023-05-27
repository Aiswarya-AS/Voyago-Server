from rest_framework.decorators import api_view
from rest_framework.response import Response
from userApp.models import Guide, Order
import jwt
from userApp.serializer import GuideSerializer, OrderSerializer
from userApp.models import Request, User, GuideWallet
from userApp.serializer import RequestSerializer
import random
from twilio.rest import Client
from django.conf import settings
from .models import Otp
from django.core.mail import send_mail
from admin1.models import AdminWallet
from django.db.models import Sum

# Create your views here.


@api_view(["POST"])
def guideSignup(request):
    try:
        first_name = request.data["first_name"]
        last_name = request.data["last_name"]
        email = request.data["email"]
        phone = request.data["phone"]
        place = request.data["place"]
        pincode = request.data["pincode"]
        language = request.data["language"]
        password = request.data["password"]
    except Exception:
        return Response({"status": "Plese provide all the details"})
    guide = Guide.objects.create(
        firstname=first_name,
        lastname=last_name,
        phone=phone,
        email=email,
        pincode=pincode,
        place=place,
        languages_known=language,
        password=password,
    )
    guide.save()
    return Response({"status": "true"})


@api_view(["POST"])
def guideLogin(request):
    try:
        email = request.data["email"]
        password = request.data["password"]
    except Exception:
        return Response({"status": "Please provide all the details.."})
    try:
        guide = Guide.objects.get(email=email, password=password, is_accepted=True)
        payload = {
            "email": guide.email,
            "password": guide.password,
            "username": guide.username,
        }
        guide_id = guide.id
        jwt_token = jwt.encode(payload, "secret", algorithm="HS256")
        return Response(
            {"status": "true", "guide_jwt": jwt_token, "guide_id": guide_id}
        )
    except Guide.DoesNotExist:
        return Response({"status": "false"})


@api_view(["GET"])
def guide(request, id):
    try:
        guide = Guide.objects.get(id=id)
        try:
            guide_wallet = GuideWallet.objects.get(id=guide.id)
        except GuideWallet.DoesNotExist:
            guide_wallet = GuideWallet.objects.create(guide_id=guide)
        serializer = GuideSerializer(guide, many=False)
        return Response({"serdata": serializer.data, "balance": guide_wallet.amount})
    except Guide.DoesNotExist:
        return Response({"status": "User not found"})


@api_view(["GET"])
def guide_requests(request, id):
    requests = Request.objects.filter(guide=id)
    serializer = RequestSerializer(requests, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def accept(request, id):
    request = Guide.objects.get(id=id)
    print(request.email)
    request.is_accepted = True
    request.save()
    subject = "Test Email"
    message = "This is a test email"
    email_from = "aiswaryaasubash@gmail.com"
    recipient_list = [request.email]

    send_mail(subject, message, email_from, recipient_list)
    return Response({"status": "true", "request_status": request.status})


@api_view(["GET"])
def history(request, id):
    order = Order.objects.filter(guide=id)
    serializer = OrderSerializer(order, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def sendOtp(request, id, guide_id):
    user = User.objects.get(id=id)
    guide = Guide.objects.get(id=guide_id)
    # phone_number = str('+', user.phone)
    # print('+', phone_number)
    phone_number = "+918590402457"
    otp_num = random.randint(1000, 9999)
    try:
        print("entered try block")
        otp_exists = Otp.objects.filter(user=id, guide=guide_id)
        print(otp_exists)
        otp_exists.delete()
        print("deleted successfully")
    except:
        print("except block")
        pass

    otp = Otp.objects.create(user=user, guide=guide, otp=otp_num)
    otp.save()
    # account_sid = settings.TWILIO_ACCOUNT_SID
    # auth_token = settings.TWILIO_AUTH_TOKEN
    # client = Client(account_sid, auth_token)

    # message = client.messages.create(
    #     body=f'Your OTP is {otp_num}',
    #     from_=settings.TWILIO_PHONE_NUMBER,
    #     to=phone_number
    # )
    return Response({"status": "true"})


@api_view(["POST"])
def guideProfile(request, id):
    print("Backend athidaaa mwonuseeee")
    firstname = request.data["firstname"]
    lastname = request.data["lastname"]
    email = request.data["email"]
    phone = request.data["phone"]
    place = request.data["place"]
    state = request.data["state"]
    country = request.data["country"]
    pricing = request.data["pricing"]
    languages_known = request.data["languages_known"]
    description = request.data["description"]
    image = request.data["image"]
    video = request.data["video"]
    print(video)

    guide = Guide.objects.get(id=id)
    guide.firstname = firstname
    guide.lastname = lastname
    guide.email = email
    guide.phone = phone
    guide.place = place
    guide.state = state
    guide.country = country
    guide.pricing = pricing
    guide.languages_known = languages_known
    guide.description = description
    guide.image = image
    # guide.video = video
    guide.save()
    print("save aayadda kuttaaa")
    return Response({"status": "true"})


@api_view(["POST"])
def withdraw(request, id):
    order = Order.objects.get(id=id)
    guide_id = request.data["guide_id"]
    guide = Guide.objects.get(id=guide_id)

    guide_wallet = GuideWallet.objects.get(id=guide.id)

    withdraw_amount = order.total_amount * 0.3
    guide_wallet.amount += withdraw_amount
    order.guide_withdraw_status = True
    order.save()
    guide_wallet.save()
    return Response({"status": "true"})
