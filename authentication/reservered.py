#    def post(self, request):
#         email = request.data['email']
#         user = User.objects.get(email=email)
#         if not user.is_verified:
#             token = RefreshToken.for_user(user).access_token
#             current_site = get_current_site(request).domain
#             relativeLink = reverse('email-verify')
#             absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
#             message = 'Hi ' + user.username + \
#                 ' Use link to verify your email, it expires in 5min \n' + absurl
#             email_from = settings.EMAIL_HOST_USER
#             email_to = user.email
#             data = {
#                     'subject': 'Verify your email', 'message': message, 'email_from': email_from, 'email_to': email_to
#                 }
#             try:
#                 Util.send_email(data)
#             except:
#                 return Response({'error': 'something went wrong with your email. Kindly specify correct and validated email address. Note, this email is not accepted and has been deleted'}, status=status.HTTP_406_NOT_ACCEPTABLE)
#             print (current_site)
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#if not user.is_active:
    #         raise AuthenticationFailed('Account disable, Contact admin.')