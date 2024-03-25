from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from users.serializers import UserSerializer
from .models import Document, DocumentPermission

        
class DocumentPermissionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True, required=False)
    # adding extra field for capture user_id
    user_id = serializers.CharField(max_length=255, write_only=True)
    class Meta:
        model = DocumentPermission
        fields = ['id', 'document', 'user', 'can_edit', 'can_view', 'user_id']
        depth = 1
    
    def to_representation(self, instance):
        # Call the superclass to get the initial representation
        data = super().to_representation(instance)
        
        # Return the representation
        return data
    


class DocumentGetSerializer(serializers.ModelSerializer):
    """This serializer is for only get request"""
    shared_with = DocumentPermissionSerializer(many=True)
    owner = UserSerializer(read_only=True)
    class Meta:
        model = Document
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request_user = self.context['request'].user

        # Check if the request user is the owner of the document
        if instance.owner == request_user:
            # If the request user is the owner, return all fields
            if data['shared_with']:
                shared_data = data['shared_with']
                for i, shared in enumerate(shared_data):
                    obj = DocumentPermission.objects.filter(document=instance, user_id=shared.get('id')).first()
                    # updating the can_edit and can_view with saved object. 
                    # I don't need to do this if this gives the current result but it doesn't
                    # I can't find why it produce this result
                    shared["can_edit"] = obj.can_edit
                    shared["can_view"] = obj.can_view
            return data
        else:
            # if the document owner isn't the request.user remove extra permission from this object except request.user
            user_id = request_user.pk
            if data['shared_with']:
                shared_data = data['shared_with']
                for i, shared in enumerate(shared_data):
                    obj = DocumentPermission.objects.filter(user_id=shared.get('id'), document=instance).first()
                    if shared.get('id') != user_id:
                        # current user id and shared_with id isn't same then remove the object
                        data['shared_with'].pop(i)
                    else:
                        # updating the can_edit and can_view with saved object. 
                        # I don't need to do this if this gives the current result but it doesn't
                        # I can't find why it produce this result
                        shared["can_edit"] = obj.can_edit
                        shared["can_view"] = obj.can_view
            return data

class DocumentSerializer(serializers.ModelSerializer):
    shared_with = DocumentPermissionSerializer(many=True, required=False)
    owner = UserSerializer(read_only=True)
    class Meta:
        model = Document
        fields = '__all__'
        read_only_fields = ['owner']

    def create(self, validated_data):
        permissions_data = validated_data.pop('shared_with', [])
        user = self.context['request'].user

        document = Document.objects.create(**validated_data, owner=user)
        for permission_data in permissions_data:

            DocumentPermission.objects.create(document=document, **permission_data)
        return document
    
    def update(self, instance, validated_data):
        user = self.context['request'].user
        permission = DocumentPermission.objects.filter(document=instance, user=user, can_edit=True).first()


        if instance.owner == user:
            instance.title = validated_data.get('title', instance.title)
            instance.content = validated_data.get('content', instance.content)
            # Handle shared_with update if provided
            shared_with_data = validated_data.get('shared_with')
            if shared_with_data is not None:
                # Assuming shared_with_data is a list of dictionaries
                instance.shared_with.clear()  # Clear existing shared_with relationships
                for permission_data in shared_with_data:
                    # Create new shared_with relationships
                    DocumentPermission.objects.create(document=instance, **permission_data)
            instance.save()
        elif instance.owner != user and permission:
            # if the user have permission to edit then update the field
            if 'shared_with' in validated_data:
                raise serializers.ValidationError({"shared_with": ["You can't update shared with"]})
            instance.title = validated_data.get('title', instance.title)
            instance.content = validated_data.get('content', instance.content)
            instance.save()
        else:
            raise PermissionDenied("You don't have permission to update this document")
        return instance
    