# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save
from django.conf import settings

from django.utils.text import slugify
from django.utils import timezone

def upload_location(instance, filename):
    # filebase, extension = filename.split('.')
    # return "%s/%s.%s%(instance.id, filebase, extension)
    return "%s/%s" % (instance.id, filename)

# post.objects.all()
# Post.objects.create(user,user...etc)

class PostManager(models.Manager):
    def active(self, *args, **kwargs):
        #  post.objects.all() = super(PostManager,self).all()
        return super(PostManager,
                      self).filter(draft=False).filter(publish__lte=timezone.now())


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             default=1, )
    # blank=True, null=True)

    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    # image = models.FileField(null=True, blank=True,)

    image = models.ImageField(
        upload_to=upload_location,
        null=True, blank=True,
        height_field='height_field',
        width_field='width_field',
    )
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    content = models.TextField(max_length=120)
    draft = models.BooleanField(default=False)
    publish = models.DateField(auto_now=False, auto_now_add=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    # model_pic = models.ImageField(upload_to=None, height_field=None,
    #   							 width_field=None, max_length=100)
    objects = PostManager()



    # def __str__(self):
    #     return self.title

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        # return "/posts/%s"%(self.id)

        return reverse("post:detail", kwargs={"slug": self.slug})

    def get_edit_url(self):
        return reverse("post:update", kwargs={"slug": self.slug})

    def get_delete_url(self):
        return reverse("post:delete", kwargs={"slug": self.slug})

    class Meta:
        ordering = ['-timestamp', 'updated']


def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


        # slug = slugify(instance.title)
        # # "tesla item 1" -> "tesla-item-1"
        # exists = Post.objects.filter(slug=slug).exists()
        # if exists:
        #     slug = "%s-%s"%(slug, instance.id)
        # instance.slug = slug


pre_save.connect(pre_save_post_receiver, sender=Post)
