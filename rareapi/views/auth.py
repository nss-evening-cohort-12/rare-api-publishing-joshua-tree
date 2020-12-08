import json
from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt

from rareapi.models.rare_user import RareUser


@csrf_exempt
def register_user(request):
    req_body = json.loads(request.body.decode())

    new_user = User.objects.create_user(
        first_name=req_body['first_name'],
        last_name=req_body['last_name'],
        email=req_body['email'],
        username=req_body['username'],
        password=req_body['password'],
        is_staff=req_body['is_staff']
    )

    rare_user = RareUser.objects.create(
        user=new_user
    )
    rare_user.save()

    token = Token.objects.create(user=new_user)

    data = json.dumps({"token": token.key})
    return HttpResponse(data, content_type='application/json')
