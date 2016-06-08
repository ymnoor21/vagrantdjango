from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
from .forms import PostForm
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def post_list(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 2)

    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)

    context = {
        "title": "Posts List",
        "posts": posts
    }

    return render(request, "posts/list.html", context)


def post_detail(request, slug=None):
    post = get_object_or_404(Post, slug=slug)

    context = {
        "title": "Post Detail",
        "post": post
    }

    return render(request, "posts/detail.html", context)


def post_create(request):
    form = PostForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()

        messages.success(request, "Post created successfully.")
        return HttpResponseRedirect(
            reverse('posts:detail', kwargs={"slug": instance.slug})
        )

    context = {
        "form": form,
        "title": "Create new post",
        "cmd": "create",
    }

    return render(request, "posts/form.html", context)


def post_edit(request, slug=None):
    instance = get_object_or_404(Post, slug=slug)
    form = PostForm(
        request.POST or None,
        request.FILES or None,
        instance=instance
    )

    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()

        messages.success(request, "Post saved successfully.")
        return HttpResponseRedirect(
            reverse('posts:detail', kwargs={"slug": instance.slug})
        )

    context = {
        "form": form,
        "title": instance.title,
        "post": instance,
        "cmd": "edit",
    }

    return render(request, "posts/form.html", context)


def post_delete(request, slug=None):
    instance = get_object_or_404(Post, slug=slug)
    instance.delete()
    messages.success(request, "Post deleted.")
    return redirect("posts:list")
