from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse,QueryDict

from .models import User
# Create your views here.

@csrf_exempt
def createUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Perform any necessary validation and error handling
        if not username or not email or not password:
            return JsonResponse({'error': 'Missing required fields'}, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': 'User with this email already exists'}, status=400)
        
        # Create the user
        user = User.objects.create(username=username, email=email, password=password)
        
        data={
            'user_id': user.id,
            'email': user.email
            }

        return JsonResponse(data, status=201)

    return JsonResponse({'error': 'Invalid request method'}, status=405)



@csrf_exempt
def userDetails(request,userId):
    try:
        user=User.objects.get(id=userId)
        if request.method == 'PUT' or request.method == 'PATCH':
            body=QueryDict(request.body)
            username = body.get('username')
            email = body.get('email')
            password = body.get('password')
            if username:
                user.username = username
            if email:
                user.email = email
            if password:
                user.password = password
            
            user.save()
            data = {
                'user_id': user.id,
                'username': user.username,
                'email': user.email,
                'message':'Sucessfully Updated'
                
            }
            return JsonResponse(data,status=200)
        
        elif request.method=='GET':
            data = {
                'userId': user.id,
                'username': user.username,
                'email': user.email,
            }
            return JsonResponse(data,status=200)
        
    
    except User.DoesNotExist():
        return JsonResponse({'error': 'User not found'}, status=404)
        
        