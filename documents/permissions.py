from rest_framework import permissions

from .models import Document

class HasDocumentObjectPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        obj = Document.objects.filter(pk=view.kwargs.get('pk')).first()

        if obj is None:
            return False
        
        if obj.owner == request.user:
            return True
        
        if request.method == "DELETE":
            return False
        
        if obj.shared_with.filter(id=request.user.id).exists():
            return True
        return False
    