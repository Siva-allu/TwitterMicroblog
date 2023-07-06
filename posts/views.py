from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse,QueryDict

from .models import Post
from users.models import User
# Create your views here.

@csrf_exempt
def createPost(request):
    if request.method == 'POST':
        userId = request.POST.get('userId')
        content = request.POST.get('content')
        
        
        if not userId or not content:
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        try:
            user=User.objects.get(id=userId)
        except User.DoesNotExist:
             return JsonResponse({'error': 'User not found'}, status=404)
        
        post = Post.objects.create(userId=user, content=content)
        
        data={
            'postId': post.id,
            'postContent': post.content,
            'createdAt': post.createdAt,
        }

        return JsonResponse(data, status=201)

    return JsonResponse({'error': 'Invalid request method'}, status=405)