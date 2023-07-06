import json
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse,QueryDict
from .models import Post
from users.models import User
import redis
# Create your views here.

redisClient=redis.Redis()
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
    if request.method == 'GET':
        posts=Post.objects.order_by('-createdAt').values('id','userId','content','createdAt','updatedAt')
        return JsonResponse(list(posts),status=200,safe=False)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
def postDetails(request,postId):
    try:
        post=Post.objects.get(id=postId)
        if request.method=='GET':
            data={
                'postId':post.id,
                'postContent':post.content,
                'createdAt':post.createdAt,
                'updatedAt':post.updatedAt
            }
            return JsonResponse(data,status=200)
        elif request.method=='PUT' or request.method=='PATCH':
            body=QueryDict(request.body)
            content=body.get('content')
            if content:
                post.content=content
            post.save()
            data={
                'postId':post.id,
                'postContent':post.content,
                'createdAt':post.createdAt,
                'updatedAt':post.updatedAt,
                'message':'Sucessfully updated'
            }
            return JsonResponse(data,status=200)
        elif request.method=='DELETE':
            try:
                post.delete()
                return JsonResponse({
                    'message':"Successfully Deleted"
                    },status=200)
            except:
                return JsonResponse({
                    'message':"Something Went Wrong."
                },status=404)
            
        return JsonResponse({'error': 'Invalid request method'}, status=405)
            
        
        
    except Post.DoesNotExist:
        return JsonResponse({'error': 'Post does not exist'}, status=404)