from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from .models import Comment
from .forms import CommentForm


# Create your views here.
def confirm_delete(request, pk):
    obj = get_object_or_404(Comment, pk=pk)
    if request.method == 'POST':
        parent_url = obj.content_object.get_absolute_url()
        obj.delete()
        messages.success(request, "Comment deleted!")
        return HttpResponseRedirect(parent_url)

    context = {
        'object': obj,
    }
    return render(request, "confirm_delete.html", context)


def comment_thread(request, pk):
    obj = get_object_or_404(Comment, pk=pk)

    initial_data = {
        "content_type": obj.content_type,
        "object_id": obj.object_id
    }

    form = CommentForm(request.POST or None, initial=initial_data)

    if form.is_valid():
        c_type = form.cleaned_data.get("content_type")

        content_type = ContentType.objects.get(model=c_type)
        object_id = form.cleaned_data.get("object_id")
        content = form.cleaned_data.get("content")
        parent_obj = None
        try:
            parent_id = int(request.POST.get("parent_id"))
        except:
            parent_id = None

        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists() and parent_qs.count() == 1:
                parent_obj = parent_qs.first()

        new_comment, created = Comment.objects.get_or_create(
            user=request.user,
            content_type=content_type,
            object_id=object_id,
            content=content,
            parent=parent_obj
        )

        return HttpResponseRedirect(f'/comments/{pk}/')

    context = {
        'comment': obj,
        'form': form
    }
    return render(request, "comment_thread.html", context)
