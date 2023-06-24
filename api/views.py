from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from webapp.models import HackerNewsPost
from api.serializers import PostSerializer


class GetAllPosts(APIView):
    '''Retrieve all posts from the database'''
    def get(self, request):
        # Get the 'type' and 'search' query parameters from the request
        post_types = request.query_params.getlist('type')
        search_text = request.query_params.get('search')
        
        # Filter the posts by type if the 'type' query parameter is provided
        if post_types:
            posts = HackerNewsPost.objects.filter(type__in=post_types)
        else:
            posts = HackerNewsPost.objects.all()

        # Exclude posts that have a value in the 'parent' field
        # Necessary because we only want to return posts and not their comments
        posts = posts.exclude(parent__isnull=False)
        
        # Filter the posts by search text if the 'search' query parameter is provided
        if search_text:
            posts = posts.filter(text__icontains=search_text)

        # Serialize the posts
        serializer = PostSerializer(posts, many=True)

        # Return the serialized data in the response
        return Response(serializer.data, status.HTTP_200_OK)


class OnePost(APIView):
    '''# Retrieve a single post based on the post_id'''
    def get(self, request, post_id):
        post = get_object_or_404(HackerNewsPost, post_id=post_id)

        # Serialize the post
        serializer = PostSerializer(post)

         # Return the serialized data in the response
        return Response(serializer.data, status.HTTP_200_OK)
    

class AddPost(APIView):
    '''Add a post to the database'''
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data

        # Create a serializer instance with the request context
        serializer = PostSerializer(data=data, context={'request':request})
        if serializer.is_valid():
            # If the data is valid, save the serialized data as a new post
            serializer.save()

            # Return the serialized data in the response
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        
        # Return any serializer errors in the response
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class MangePost(APIView):
    '''Update and delete a post'''

    permission_classes = [IsAuthenticated] # Only authenticated users can access this endpoint
    serializer_class = PostSerializer

    def put(self, request, post_id):
        data = request.data
        user = request.user

        # Retrieve the post based on the post_id
        post = get_object_or_404(HackerNewsPost, post_id=post_id)

        # Check if the authenticated user is the owner of the post
        if post.user_id != user.id:
            return Response({"message": "Not Found"}, status.HTTP_404_NOT_FOUND)
        
        # Create a serializer instance with the request data and existing post instance
        serializer = self.serializer_class(data=data, instance=post, partial=True)
        
        if serializer.is_valid():
            # Update the post with the validated serializer data
            serializer.update(post, serializer.validated_data)

            # Return the updated serialized data in the response
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        
        # Return any serializer errors in the response
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, post_id):
        user = request.user

        # Retrieve the post based on the post_id
        post = get_object_or_404(HackerNewsPost, post_id=post_id)

        # Check if the authenticated user is the owner of the post
        if post.user_id != user.id:
            return Response({"message": "Not Found"}, status.HTTP_404_NOT_FOUND)
        
        # Delete the post
        post.delete()

        # Return a success message in the response
        return Response({"message":"post deleted"}, status.HTTP_204_NO_CONTENT)

