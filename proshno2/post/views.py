from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from post.models import Post, PostComment
from django.db.models import Q
from post.forms import PostCreateUpdateForm, CommentCreateUpdateForm

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

# def post_list(request, *args, **Kwargs):
#     post_qs = Post.objects.filter(~Q(status='hidden'))
#     response = {
#         "post_qs": post_qs
#     }
#
#     return render(request, 'post/post_list.html', response)

#
# def post_details(request, post_id, *args, **Kwargs):
#     post_obj = Post.objects.filter(~Q(status='hidden') & Q(id=post_id)).first()
#     post_comments = PostComment.objects.filter(post__id= post_id)
#     response = {
#         "post_obj": post_obj,
#         "post_comments": post_comments,
#     }
#
#     return render(request, 'post/post_details.html', response)

# def post_create(request, *args, **kwargs):
#
#     if request.method == 'POST':
#         form = PostCreateUpdateForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('post:post_details', form.instance.id)
#     else:
#         form = PostCreateUpdateForm()
#
#     response = {
#         "form": form,
#         "type": "Create Post"
#     }
#
#     return render(request, 'post/post_create_or_update.html', response)


# def post_update(request, post_id, *args, **kwargs):
#     post_obj = Post.objects.filter(id= post_id).first()
#     if request.method == 'POST':
#         form = PostCreateUpdateForm(request.POST, instance=post_obj)
#         if form.is_valid():
#             form.save()
#             return redirect('post:post_list')
#     else:
#         form = PostCreateUpdateForm(instance=post_obj)
#
#     response = {
#         "form": form,
#         "type": "Update Post"
#     }
#
#     return render(request, 'post/post_create_or_update.html', response)

# def post_delete(request, post_id, *args , **kwargs):
#
#     Post.objects.filter(id=post_id).update(status= 'hidden')
#     return redirect("post:post_list")

class PostListView(ListView):

    queryset = Post.objects.all()
    context_object_name = 'post_qs'
    template_name = 'blog/post_list.html'
    extra_context = {
        'apply_search': True
    }

    def get_queryset(self):
        queryset = self.queryset.filter(~Q(status='hidden')).order_by('-id')
        if self.request.GET.get('search', ''):
            search_keyword = self.request.GET['search']
            queryset = queryset.filter( Q(position__icontains=search_keyword) | Q(companyName__icontains=search_keyword))
        return queryset


    # #model = Post
    #
    # # var1 = 0
    # # var2 = 1
    # #
    # #
    # #
    # # def get_context_data(self, **kwargs):
    # #     context = super(PostListView, self).get_context_data(**kwargs)
    # #     context.update({'var1': self.var1, 'var2': self.var2})
    # #     return context
    #
    # template_name = 'post/post_list.html'
    # context_object_name = 'post_qs'
    # queryset = Post.objects.filter(~Q(status='hidden')).order_by('-id')



def post_details(request, post_id, *args, **Kwargs):
    post_obj = Post.objects.filter(~Q(status='hidden') & Q(id=post_id)).first()
    post_comments = PostComment.objects.filter(post__id= post_id).order_by('-created')

    # if request.method == 'POST':
    #     form = CommentCreateUpdateForm(request.POST)
    #     # body = request.POST['body']
    #     if form.is_valid():
    #         form.save()
    #         return redirect('post:post_details', post_id)

    if request.method == 'POST':
        form = CommentCreateUpdateForm(request.POST)
        if form.is_valid():
            comment = form.save(commit= False)
            comment.author = request.user
            comment.post = post_obj
            comment.save()
            return redirect('post:post_details', post_id)
    else:
        form = CommentCreateUpdateForm()

    response = {
        "post_obj": post_obj,
        "post_comments": post_comments,
        "form": form,
    }

    return render(request, 'post/post_details.html', response)


class PostCreateView(LoginRequiredMixin, CreateView ):
    model = Post
    form_class = PostCreateUpdateForm
    template_name = "post/post_create_or_update.html"
    success_url = reverse_lazy("post:post_list")

    def form_valid(self, form):  #login user will get auto author
        form.instance.author = self.request.user
        return super(PostCreateView, self).form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostCreateUpdateForm
    template_name = "post/post_create_or_update.html"
    success_url = reverse_lazy("post:post_list")

    def form_valid(self, form): #login user is the post creator? | yes? can edit and get auto author no? 403 Forbidden
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self): #editor is the owner or not? | yes? can edit no? 403 Forbidden
        post_obj = self.get_object()
        if self.request.user == post_obj.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy("post:post_list")
    template_name = "post/post_delete.html"
    context_object_name = "post"


    def test_func(self): #deleter is the owner or not? | yes? can delete no? 403 Forbidden
        post_obj = self.get_object()
        if self.request.user == post_obj.author:
            return True
        return False

