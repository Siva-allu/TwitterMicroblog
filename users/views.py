from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
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

        return JsonResponse({'user_id': user.id, 'email': user.email}, status=201)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
