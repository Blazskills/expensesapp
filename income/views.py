from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import IncomeSerializer
from .models import Income
from authentication.models import User
from rest_framework import permissions
from expenses.permissions import IsVerified
# Create your views here.


# create an expenses using POST method and also and list all or by id of the current user expenses out.
class IncomeListAPIView(ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated,IsVerified]
    serializer_class = IncomeSerializer
    queryset = Income.objects.all()
    # created is_autehticated and also created new auth if the user is the owner of the current expenses (IsOwner), permission should be granted.
    

    # override the create method to update the owner to the current user and  create new expenses(POST)
    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    # to list current user expenses(GET)
    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

###This method works.. You can do it this way 

class IncomeDetailAPIView(RetrieveUpdateDestroyAPIView):
    
    permission_classes = (permissions.IsAuthenticated, IsVerified)
    serializer_class = IncomeSerializer
    queryset = Income.objects.all()
    lookup_field = "id"

    def get_queryset(self):
        return Income.objects.filter(owner=self.request.user )

            
        
    # def get_queryset(self):

    #     return Expenses.objects.filter(owner=self.request.user )
    

### Or do it this way.. either ways, same result
# class ExpenseDetailAPIView(RetrieveUpdateDestroyAPIView):
#     serializer_class = ExpensesSerializer
#     permission_classes = (permissions.IsAuthenticated, IsOwner,)
#     queryset = Expenses.objects.all()
#     lookup_field = "id"

#     def get_queryset(self):
#         return self.queryset.filter(owner=self.request.user)
















#### RetrieveUpdateDestroyAPIView EDITED
# class ExpenseDetailAPIView(RetrieveUpdateDestroyAPIView):
#     serializer_class = ExpensesSerializer
#     permission_classes = (permissions.IsAuthenticated, IsOwnerIsVerifiedOrIsSuper)
#     lookup_field = "id"
#     queryset =Expenses
    
#     def patch(self, request, *args, **kwargs):
        
#         print('testing')
#         print(request.user.is_superuser)
#         if not request.user.is_superuser:
#             db_description=self.get_object().description
#             request.data['description'] = db_description
#         return self.update(request, *args, **kwargs)
            #  print(getuserdata)
            #  print('im super')
            #  ch=Expenses.objects.get(id= (self.kwargs.get('id')))
            #  ch.description = getuserdata
            #  ch.save()
           
        # else:
        #     print('im not super')
        
        # # user_checked = User.objects.get(email = self.get_object().owner)
        # if self.get_object().owner   == request.user:
        #     print(request.user.is_superuser)
        #     # print(request.user)
        #     # print(self.get_object().owner )
        #     # print(self.get_object()) 
        #     checking = User.objects.get(email = self.get_object().owner)
        #     if not checking.is_superuser:
        #         getuserdata= request.data.get('description')
        #         print(getuserdata)
        #         print('im super')
        #     else:
        #         print('im not super')
        #     # print(checking)
        # else:
        #     print('im not the owner.')
        #     print(self.request.user)
        #     print(self.get_object().owner)
