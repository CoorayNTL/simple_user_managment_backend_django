
from base64 import urlsafe_b64decode, urlsafe_b64encode
# from email.message import EmailMessage
from tokenize import generate_tokens
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib import auth
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail,EmailMessage
from user_magement import settings
# from .models import NotificationSettings
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.template.loader import render_to_string
from django.utils.encoding import force_text
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode


# Create your views here.
def home(request):
    return render(request,'authentication/index.html',{})

def signup(request):
   
  if request.method == 'POST': 
    
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        comfirm_password = request.POST['comfirm_password']
    
        # if User.objects.filter(username=username).exists():
        #     messages.error(request,"Username is already taken")
        #     return redirect('signup')
        
        # if User.objects.filter(email=email).exists():
        #     messages.error(request,"Email is already taken")
        #     return redirect('signup')
        
        if password != comfirm_password: 
            messages.error(request,"Password do not match")
            return redirect('signup')
        
        # if len(password)<8:
        #     messages.error(request,"Password is too short")
        #     return redirect('signup')    
        
        if len(username)<3:
            messages.error(request,"Username is too short")
            return redirect('signup')
    
    
        myuser = User.objects.create_user(username,email,password)
        myuser.save()
    
        messages.success(request,"Your account has been successfully created")
        
        #welcome_email.delay(username,email)
        
        subject = "Welcome to CodeWithLakshan"
        message = "Hi, "+myuser.username+" welcome to CodeWithLakshan.\n " + "Thank you for registering in our website. We are happy to have you here."
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject,message,from_email,to_list,fail_silently=True) ##fail_silently=True is used to avoid error when email is not sent
        
        #Email address verification
        current_site = get_current_site(request)
        email_subject = 'Activate your account'
       # messages = 'Hi, '+myuser.username+' please use this link to verify your account\n' + 'http://'+current_site.domain+'/activate/'+str(myuser.id)+'/'+str(myuser.password)
        message2  = render_to_string('email_verification.html',{
            'name':myuser.username,
            "domin":current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            "token":default_token_generator.make_token(myuser),
        })
        
        email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [myuser.email],
        )
        
        email.fail_silently = True
        email.send()
        
        
        return redirect('signin')
    
  return render(request,'authentication/signup.html',{})
 

# def email_settings(request):
#     if request.method == 'POST':
#         user_settings = NotificationSettings.objects.get(user=request.user)
#         user_settings.email_enabled = request.POST.get('email_enabled', False)
#         user_settings.notification_frequency = request.POST.get('notification_frequency', 1)
#         user_settings.save()
#         return redirect('home')

#     return render(request, '')

# def push_settings(request):
#     if request.method == 'POST':
#         user_settings = NotificationSettings.objects.get(user=request.user)
#         user_settings.push_enabled = request.POST.get('push_enabled', False)
#         user_settings.notification_frequency = request.POST.get('notification_frequency', 1)
#         user_settings.save()
#         return redirect('home')

#     return render(request, '')


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(username=username,password=password)
        
        if user is not None:
            login(request,user)
            messages.success(request,"You have successfully logged in")
            return redirect('home')
        else:
            messages.error(request,"Invalid Credentials")
            return redirect('home')
        
    return render(request,'authentication/signin.html',{})


def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('home')

def activate(request,uidb64,token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64)) #force_text is used to convert byte to string check pirticulaer user is exist or not
        user = User.objects.get(pk=uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        user = None
        
    if user is not None and generate_tokens.check_token(user,token):
        user.is_active = True
        user.save()
        messages.success(request,"Your account has been activated successfully")
        return redirect('signin')
    else:
        messages.error(request,"Invalid activation link")
        return redirect('signup')