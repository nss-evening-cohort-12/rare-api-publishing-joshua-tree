import json
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
# from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from rareapi.models import RareUser


@csrf_exempt
def login_user(request):
    req_body = json.loads(request.body.decode())

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':

        # Use the built-in authenticate method to verify
        username = req_body['username']
        password = req_body['password']
        authenticated_user = authenticate(username=username, password=password)

        # If authentication was successful, respond with their token
        if authenticated_user is not None:
            token = Token.objects.get(user=authenticated_user)
            data = json.dumps({"valid": True, "token": token.key})
            return HttpResponse(data, content_type='application/json')

        else:
            # Bad login details were provided. So we can't log the user in.
            data = json.dumps({"valid": False})
            return HttpResponse(data, content_type='application/json')


@csrf_exempt
def register_user(request):
    # Load the JSON string of the request body into a dict
    req_body = json.loads(request.body.decode())
    
    # Create a new user by invoking the `create_user` helper method
    # on Django's built-in User model
    new_user = User.objects.create_user(
        first_name=req_body['first_name'],
        last_name=req_body['last_name'],
        email=req_body['email'],
        username=req_body['username'],
        password=req_body['password'],
        is_staff=req_body['is_staff'],
    )

    # Now save the extra info in the rareapi_rareuser table
    rare_user = RareUser.objects.create(
        user=new_user,
        bio=req_body['bio'],
        display_name=req_body['display_name'],
        profile_image_url=req_body['profile_image_url']
    )

    # Commit the user to the database by saving it
    rare_user.save()

    # Use the REST Framework's token generator on the new user account
    token = Token.objects.create(user=new_user)

    # Return the token to the client
    data = json.dumps({"token": token.key})
    return HttpResponse(data, content_type='application/json')

# @csrf_exempt
# def logout_view(request):
#     logout(request)
#     return HttpResponse()
#     return redirect('/admin')
#     redirect('login')
