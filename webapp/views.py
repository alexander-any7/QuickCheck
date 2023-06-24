from ast import literal_eval
from django.views.generic import ListView, DetailView
from webapp.models import HackerNewsPost, TYPES


class PostListView(ListView):
    model = HackerNewsPost
    template_name = 'webapp/home.html'
    context_object_name = 'posts'
    ordering = ['-time']
    paginate_by = '9'
    
    def get_queryset(self):
        # Retrieve the initial queryset
        queryset = super().get_queryset()

        # Exclude posts with type 'comment'
        queryset = queryset.exclude(type='comment')

        # Filter by types specified in the request parameters
        types = self.request.GET.getlist('type')
        if types:
            queryset = queryset.filter(type__in=types)
        
        # Filter by search query specified in the request parameters
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(text__icontains=search_query)
        return queryset
    
    def get_context_data(self, **kwargs):
        # Retrieve the initial context data
        context = super().get_context_data(**kwargs)

        # Add filters to the context for displaying in the template
        context['filters'] = TYPES
        return context
    

class PostDetailView(DetailView):
    model = HackerNewsPost
    template_name = 'webapp/post-detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        # Retrieve the initial context data
        context = super().get_context_data(**kwargs)

        # Get the post object from the context
        post = context['post']      

        # Convert the 'kids' field from a string representation to a list
        post.kids = literal_eval(post.kids)

        # Retrieve and add the comments associated with the post to the context
        comments = []
        for kid in post.kids:

            # Get the first comment with the given 'kid' post_id, ordered by 'time'
            comment = HackerNewsPost.objects.filter(post_id=kid).order_by('time').first()
            if comment:
                comments.append(comment)
        # Add the comments list to the context data
        context['comments'] = comments
        return context