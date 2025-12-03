from django.db import models
from django.utils.text import slugify

class Course(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    excerpt = models.TextField(blank=True)
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:220]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Lesson(models.Model):
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    video_url = models.URLField(blank=True, null=True)
    duration_minutes = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.course.title} — {self.title}"