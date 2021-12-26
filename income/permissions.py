from rest_framework import permissions


class IsOwnerIsVerifiedOrIsSuper(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return  obj.owner.is_verified == True  and obj.owner == request.user or request.user.is_superuser == True 



class IsVerified(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner.is_verified == True



#   def put(self, request, *args, **kwargs):
#         if Expenses.owner == self.request.user:
#             print('IM THE OWNER OO') 
#         else:
#             print('im not the owner.')
#         return self.update(request, *args, **kwargs)