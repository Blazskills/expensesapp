from rest_framework import permissions
from .models import Expenses

# class IsOwnerIsVerifiedOrIsSuper(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         return  obj.owner.is_verified == True  and obj.owner == request.user or request.user.is_superuser == True 



# class IsVerified(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         return obj.owner.is_verified == True

class IsVerified(permissions.BasePermission):
    """
    Allows access only to verified user.
    """

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.is_verified == True )
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
#   def put(self, request, *args, **kwargs):
#         if Expenses.owner == self.request.user:
#             print('IM THE OWNER OO') 
#         else:
#             print('im not the owner.')
#         return self.update(request, *args, **kwargs)