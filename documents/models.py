from django.db import models
from django.contrib.auth.models import User

class Document(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_documents')
    shared_with = models.ManyToManyField(User, through='DocumentPermission', related_name='shared_documents')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class DocumentPermission(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    can_edit = models.BooleanField(default=False)
    can_view = models.BooleanField(default=False)


