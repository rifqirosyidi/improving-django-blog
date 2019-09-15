from urllib.parse import quote_plus
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, Http404
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Post
from .forms import PostForm
from comments.models import Comment
from comments.forms import CommentForm


def post_create(request):

    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    if not request.user.is_authenticated:
        raise Http404
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        messages.success(request, "Successfuly Created")
        return HttpResponseRedirect(f'/posts/{instance.slug}/')

    button_variables = "Create"
    context = {
        'form': form,
        'button_variables': button_variables
    }
    return render(request, 'post_form.html', context)


def post_detail(request, slug):
    today = timezone.now().date()
    instance = get_object_or_404(Post, slug=slug)
    if instance.publish > timezone.now().date() or instance.draft:
        if not request.user.is_authenticated or not request.user.is_staff or not request.user.is_superuser:
            raise Http404

    initial_data = {
        "content_type": instance.get_content_type,
        "object_id": instance.id
    }
    comment_form = CommentForm(request.POST or None, initial=initial_data)
    if comment_form.is_valid():
        c_type = comment_form.cleaned_data.get("content_type")

        content_type = ContentType.objects.get(model=c_type)
        object_id = comment_form.cleaned_data.get("object_id")
        content = comment_form.cleaned_data.get("content")

        new_comment, created = Comment.objects.get_or_create(
            user=request.user,
            content_type=content_type,
            object_id=object_id,
            content=content
        )

    comments = instance.comments
    share_string = quote_plus(instance.content)
    context = {
        "title": instance.title,
        "instance": instance,
        "share_string": share_string,
        "today": today,
        "comment_form": comment_form,
        "comments": comments,
    }
    return render(request, 'post_detail.html', context)


def post_list(request):
    today = timezone.now().date()
    query_list = Post.objects.active()

    if request.user.is_staff or request.user.is_superuser:
        query_list = Post.objects.all().order_by('-timestamp')

    search = request.GET.get('search')
    if search:
        query_list = query_list.filter(
            Q(title__icontains=search) or
            Q(content__icontains=search)
        ).distinct()
    paginator = Paginator(query_list, 6)
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    query_set = paginator.get_page(page)

    context = {
            "title": "My User List",
            "object_list": query_set,
            "page_request_var": page_request_var,
            "today": today
        }

    return render(request, 'post_list.html', context)


def post_update(request, slug):

    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    if not request.user.is_authenticated:
        raise Http404

    instance = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Post Updated")
        return HttpResponseRedirect(f'/posts/{instance.slug}/')

    button_variables = "Update"
    context = {
        "title": instance.title,
        "instance": instance,
        "button_variables": button_variables,
        "form": form
    }
    return render(request, 'post_form.html', context)


def post_delete(request, slug):

    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    if not request.user.is_authenticated:
        raise Http404

    instance = get_object_or_404(Post, slug=slug)
    instance.delete()
    messages.success(request, "Successfuly Deleted")
    return redirect('posts:list')
