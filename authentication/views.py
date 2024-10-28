from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views.generic import View
from .forms import signupForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout, get_user_model
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from .utils import generate_token
from django.utils.encoding import force_bytes,force_str, DjangoUnicodeDecodeError
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.urls import reverse

# Create your views here.
def signup(request):
    if request.method=="POST":
        form = signupForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data.get('email')

            if get_user_model().objects.filter(email=email).exists():
                messages.warning(request, "YOU ARE ALREADY REGISTERED WITH THIS EMAIL")
                return redirect('/')

            user = form.save(commit=False)
            user.is_active = False
            user.save()


            email_subject="Activate Your Account"
            message=render_to_string('activate.html',{
                'user':user,
                'domain':'127.0.0.1:8000',
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':generate_token.make_token(user)
            })

            email_message = EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[user.email])
            email_message.send()
            messages.success(request,"ACTIVATE YOUR ACCOUNT BY CLICKING THE LINK IN YOUR GMAIL")
            return redirect('/')
        
        else:
            messages.warning(request,"INVALID PASSWORD")
            return redirect('/')
            
    else:
        form = signupForm()
    
    context={"form":form}
    
    return render(request,'signup.html',context)


class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and generate_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            messages.info(request, "ACCOUNT ACTIVATED AND LOGGED IN SUCCESSFULLY")
            return redirect('/')

        messages.error(request, "ACTIVATION LINK IS INVALID")
        return render(request, 'activatefail.html')

class RequestResetEmailView(View):
    def get(self,request):
        return render(request,'request-reset-email.html')
    
    def post(self,request):
        email=request.POST['email']
        user=User.objects.filter(email=email)

        if user.exists():
            email_subject="Reset Your Password"
            message=render_to_string('reset-user-password.html',{
                'domain':'127.0.0.1:8000',
                'uid':urlsafe_base64_encode(force_bytes(user[0].pk)),
                'token':PasswordResetTokenGenerator().make_token(user[0])
            })

            email_message=EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[email])
            email_message.send()

            messages.info(request,"CHECK YOUR EMAIL")
            return redirect('/')
        else:
            messages.info(request,"YOU ARE NOT REGISTERED")
            return redirect('/')



class SetNewPasswordView(View):
    def get(self,request,uidb64,token):
        context = {
            'uidb64':uidb64,
            'token':token
        }
        try:
            user_id=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=user_id)

            if  not PasswordResetTokenGenerator().check_token(user,token):
                messages.warning(request,"PASSWORD RESET LINK IS INVALID")
                return render(request,'request-reset-email.html')

        except DjangoUnicodeDecodeError as identifier:
            pass

        return render(request,'set-new-password.html',context)

    def post(self,request,uidb64,token):
        context={
            'uidb64':uidb64,
            'token':token
        }
        password=request.POST['pass1']
        confirm_password=request.POST['pass2']
        
        if password!=confirm_password:
            messages.warning(request,"PASSWORD NOT MATCHED")
            return render(request,'set-new-password.html',context)

        try:
            user_id=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=user_id)
            user.set_password(password)
            user.save()
            messages.success(request,"PASSWORD RESET SUCCESS")
            return redirect('/')

        except DjangoUnicodeDecodeError as identifier:
            messages.error(request,"SOMETHING WENT WRONG")
            return render(request,'set-new-password.html',context)
 
def handlelogin(request):
    if request.method=="POST":

        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            username =  form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                if user.is_superuser:
                    messages.success(request, "LOG IN SUCCESS")
                    return redirect(reverse('admin:index'))
                else:
                    messages.success(request, "LOG IN SUCCESS")
                    return redirect('/')
            
        else:
            messages.error(request, "INVALID EMAIL OR PASSWORD")
            return redirect('/')
    
    form = AuthenticationForm()
    return render(request,'login.html')


def handlelogout(request):
    logout(request)
    messages.info(request,"LOG OUT SUCCESS")
    return redirect('/')