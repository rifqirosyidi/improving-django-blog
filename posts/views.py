from urllib.parse import quote_plus
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, Http404
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Post
from .forms import PostForm


# Create your views here.
def post_create(request):

    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    if not request.user.is_authenticated:
        raise Http404
    # request files when you have image field / files to upload
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        # or you can use form.cleaned_data.get('field')
        instance.user = request.user
        instance.save()
        messages.success(request, "Successfuly Created")
        return HttpResponseRedirect(f'/posts/{instance.slug}/')

    # Capture The Data From the Form (Not Recommend .. add request.POST to PostForm(...) is sugested)
    # if request.method == 'POST':
    #     print(request.POST.get('title'))
    #     print(request.POST.get('content'))

    button_variables = "Create"
    context = {
        'form': form,
        'button_variables': button_variables
    }
    return render(request, 'post_form.html', context)


def post_detail(request, slug):
    # this instance will raise an error , we dont want that so, use get_object_or_404
    # instance = Post.objects.get(id=99)
    today = timezone.now().date()

    instance = get_object_or_404(Post, slug=slug)  # This will return 404 page default. id not found, not an error
    if instance.publish > timezone.now().date() or instance.draft:
        if not request.user.is_authenticated or not request.user.is_staff or not request.user.is_superuser:
            raise Http404

    share_string = quote_plus(instance.content)
    context = {
        "title": instance.title,
        "instance": instance,
        "share_string": share_string,
        "today": today
    }
    return render(request, 'post_detail.html', context)
    # return HttpResponse('Detail')


def post_list(request):
    # Using Model Manager
    today = timezone.now().date()
    query_list = Post.objects.active()
    # filter(draft=False).filter(publish__lte=timezone.now())  # all().order_by(
    # '-timestamp')

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
