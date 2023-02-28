from audioop import reverse
from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from myapp.models import Userdata
from myapp.models import Audio,Collection
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template import loader
from django.template.loader import render_to_string
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from six import text_type
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.urls import reverse
# Create your views here.
from validate_email_address import validate_email as va
import re
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

@login_required(login_url="userlogin")
def userdetail(request):
    Detail = Userdata.objects.filter(UserName = request.user)
    return render(request,"userdetail.html",{"Detail":Detail})
    

def usersignup(request):
    #ส่งข้อมูล
    if request.method=="POST":
        # รับค่า
        username = request.POST["username"]
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]
        age = request.POST["age"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmpassword = request.POST["confirmpassword"]
        is_valid = va(email)
        if len(username) < 3:
            messages.warning(request, "Username ต้องมีอย่างน้อย 3 ตัวอักษร")
            return redirect("/usersignup")
        elif username.isdigit():
            messages.warning(request, "Username ต้องประกอบด้วยตัวอักษรและตัวเลข")
            return redirect("/usersignup")
        if firstname.isdigit() :
            messages.warning(request, "FirstName ไม่ควรมีตัวเลข")
            return redirect("/usersignup")
        if lastname.isdigit():
            messages.warning(request, "LastName ไม่ควรมีตัวเลข")
            return redirect("/usersignup")

        if not is_valid:
            messages.warning(request, "Invalid email address")
            return redirect("/usersignup")
        try:
            validate_email(email)
        except ValidationError:
            messages.warning(request, "Invalid email")
            return redirect("/usersignup")
        
        if User.objects.filter(email=email).exists():
            messages.warning(request,"Email นี้มีผู้ใช้งานแล้ว")
            return redirect("/usersignup")
        
        if int(age) < 3 or int(age) > 120:
            messages.warning(request, "Age must be between 3 and 120")
            return redirect("/usersignup")
        if len(password) < 8:
            messages.warning(request, "Password must have at least 8 characters")
            return redirect("/usersignup")

        if not re.search("[0-9]", password):
            messages.warning(request, "Password must include numbers")
            return redirect("/usersignup")

        if username == "" or firstname == "" or lastname == "" or age == "" or password == "" or confirmpassword == "" or email == "":
            messages.warning(request,"กรุณาป้อนข้อมูลให้ครบ")
            return redirect("/usersignup")
        else:
        
            if password == confirmpassword:
                # ตรวจสอบชื่อบัญชีผู้ใช้
                if User.objects.filter(username=username).exists():
                    messages.warning(request,"Username นี้มีคนใช้งานแล้ว")
                    return redirect("/usersignup")
                else:
                    user = User.objects.create_user(
                        username=username,
                        email=email,
                        password=password
                    )
                    user.save()
                    
                    userdata = Userdata.objects.create(
                        UserName = username,
                        FirstName = firstname,
                        LastName = lastname,
                        age = age,
                        email = email,
                       
                    )
                    
                    
                    userdata.save()
                    messages.success(request,"สมัครสมาชิกสำเร็จ")
                    
                    return redirect("userlogin")
                
            else:
                messages.warning(request,"รหัสผ่านไม่ตรงกัน")
                return redirect("/usersignup")
    else:
        return render(request,"usersignup.html")
   
        
    
def userlogin(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        if username == "":
            messages.warning(request,"กรุณากรอก username")
            return redirect("userlogin")
        elif password == "":
            messages.warning(request,"กรุณาใส่ password")
            return redirect("userlogin")
        else:
            # เข้าสู่ระบบ
            user = auth.authenticate(username=username,password=password)
            if user is not None:
                auth.login(request,user)
                return redirect("/mainpage")
            else:
                messages.warning(request,"ไม่มีข้อมูลในระบบ")
                return redirect("userlogin")
             
    else:
        return render(request,"userlogin.html")


def userlogout(request):
    auth.logout(request)
    return redirect("userlogin")

@login_required(login_url="userlogin")
def user_delete(request, user_id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            try:
                user = Userdata.objects.get(id=user_id)
            except Userdata.DoesNotExist:
                return redirect("userlogin")
            username = user.UserName
            related_user = User.objects.get(username=username)
            audio_data = Audio.objects.filter(UserName=related_user)
            collection_data = Collection.objects.filter(UserName=related_user)
            audio_data.delete()
            collection_data.delete()
            user.delete()
            related_user.delete()
            return redirect("userlogin")
    else:
        return redirect("userlogin")



def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return render(request, 'forgotpassword.html', {'error': 'Invalid email'})

        # Generate a password reset token and send it to the user
        token = default_token_generator.make_token(user)
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        reset_url = reverse('reset_password', args=(uidb64, token))
        reset_url = request.build_absolute_uri(reset_url)
        message = render_to_string('password_reset_email.html', {'reset_url': reset_url})
        send_mail('Password reset', message, 'noreply@example.com', [user.email])
        return render(request, 'forgotpassword.html', {'success': 'An email has been sent with instructions to reset your password'})

    return render(request, 'forgotpassword.html')

User = get_user_model()
def reset_password(request, uidb64, token):
    try:
        uid = text_type(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = PasswordChangeForm(user, request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                return redirect('password_reset_done')
        else:
            form = PasswordChangeForm(user)
    else:
        return redirect('password_reset_invalid')

    return render(request, 'reset_password.html', {'form': form})

def password_reset_done(request):
    return render(request, 'password_reset_done.html')

def password_reset_invalid(request):
    return render(request, 'password_reset_invalid.html')


@login_required(login_url="userlogin")
def confirm_delete_user(request, user_id):
    try:
        user = Userdata.objects.get(id=user_id)
    except Userdata.DoesNotExist:
        # Handle the case when the user_id does not exist
        return redirect("userlogin")
    return render(request, 'confirm_delete_user.html', {'user':user})







