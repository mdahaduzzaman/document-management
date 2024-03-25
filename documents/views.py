from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet

from django.db.models import Q

from .serializers import *
from .models import *
from .permissions import HasDocumentObjectPermission

class DocumentModelViewSet(ModelViewSet):
    serializer_class = DocumentSerializer
    queryset = Document.objects.all().order_by('-id')
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        documents = Document.objects.filter(
            Q(owner=user)
            | (Q(documentpermission__user=user) & Q(documentpermission__can_view=True))
        ).distinct().order_by('-id')
        return documents
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return DocumentGetSerializer
        return DocumentSerializer

    
    
