# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponseRedirect, Http404  # HttpResponse
from django.db.models import Q
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from django.shortcuts import (
    render,
    get_object_or_404,
    redirect,
)

from models import Post
from .forms import PostForm


# from urllib import  quote_plus

# Create your views here.


def post_create(request):
    if not (request.user.is_staff or request.user.is_superuser):
        raise Http404
    if not request.user.is_authenticated():
        raise Http404
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        # print form.cleaned_data.get("title")
        instance.save()
        # message success
        messages.success(request, "item Created")
        return HttpResponseRedirect(instance.get_absolute_url())
    else:
        messages.error(request, "Error enter data again")
    # if request.method=='POST':
    # 	print request.POST.get("content")
    # 	title = request.POST.get("title")
    # 	Post.objects.create(title=title)
    context = {
        "form": form,
    }
    return render(request, "post_form.html", context)


def post_detail(request, slug):
    # instance = Post.objects.get(id=1)
    instance = get_object_or_404(Post, slug=slug)
    if instance.draft or instance.publish > timezone.now().date():

        # instance.draft = False  # change in the object
        if not (request.user.is_staff or request.user.is_superuser):
            raise Http404
    # share_string = quote_plus(instance.content)
    content = {
        'title': 'Detail',
        'instance': instance,
        # 'share_string': share_string,
    }
    return render(request, "post_detail.html", content)


def post_list(request):
    today = timezone.now().date()
    # __lte -> less than or equal to
    queryset_list = Post.objects.active()
    #  Post.objects.filter(draf=False).filter(publish__lte=timezone.now())
    #  .all()  # .order_by("-timestamp")
    # queryset_list   = Post.objects.raw('SELECT * FROM posts_post')
    if (request.user.is_staff or request.user.is_superuser):
        queryset_list = Post.objects.all()

    query = request.GET.get("q")
    # print request.GET
    if query:
        queryset_list = Post.objects.filter(
            Q(title__icontains=query) |  # Case-insensitive containment test
            Q(content__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query)
        ).distinct()  # for not duplicate items
    paginator = Paginator(queryset_list, 3)  # Show 25 contacts per page
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)

    content = {
        'object_list': queryset_list,
        'title': 'list',
        'queryset': queryset,
        'page_request_var': page_request_var,
        'today': today,
    }
    # if request.user.is_authenticated():
    # #return HttpResponse("<h1>List</h1>")
    # 	content = {
    # 	    'title':'my  list',
    # 	}
    # else:
    # 	content = {
    # 		'title':'list',
    # 	}
    return render(request, "post_list.html", content)


def post_update(request, slug=None):
    if not (request.user.is_staff or request.user.is_superuser):
        raise Http404
    # instance = Post.objects.get(id=1)
    instance = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        # message success
        messages.success(request, "item saved")
        return HttpResponseRedirect(instance.get_absolute_url())
    content = {
        'title': instance.title,
        'instance': instance,
        'form': form,
    }
    return render(request, "post_form.html", content)


def post_delete(request, slug=None):
    if not request.user.is_staff or request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, slug=slug)
    instance.delete()
    messages.success(request, "item deleted")
    return redirect("post:list")
