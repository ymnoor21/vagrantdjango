from __future__ import unicode_literals
from django.db.models.signals import pre_save
from django.db import models
from django.utils.text import slugify


def upload_location(instance, filename):
    return "images/posts/%s/%s" % (instance.slug, filename)


class Post(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    image = models.ImageField(
        null=True,
        blank=True,
        upload_to=upload_location,
        width_field="width_field",
        height_field="height_field",
    )

    width_field = models.IntegerField(default=0)
    height_field = models.IntegerField(default=0)

    content = models.TextField()
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at", "-updated_at"]


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
        slug = create_slug(instance)
        instance.slug = slug


pre_save.connect(
    pre_save_post_receiver,
    sender=Post
)
