from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password,check_password
from .models import * 
from django.urls import reverse
import random
from django.core.mail import EmailMessage 
from django.template.loader import render_to_string 
from django.conf import settings

# Create your views here.

def check_login(view_function):
    def wrapper(request,*args,**kwargs):
        if "email" in request.session:
            try:
                uid = InstaUser.objects.get(email = request.session['email'])
                request.uid = uid
                return view_function(request,*args,**kwargs)
            except InstaUser.DoesNotExist:
                
                return redirect("login")
        return redirect("login")
    return wrapper
        
def login(request):
    print("METHOD:", request.method)
    if request.POST:
        email = request.POST['email']
        password = request.POST['password']
        try:
            uid = InstaUser.objects.get(email = email)
            if not check_password(password,uid.password): 
                return render(request, "myapp/login.html")
            else:
                request.session['email'] = email
                context = {'uid' : uid}
                uid.is_active = True
                uid.save()
                return redirect('index') 
        except:
            print('===========3', password)
            return render(request, "myapp/login.html")
    else:
        print('===========4')
        return render(request, "myapp/login.html")
        
def send_email(email, name, otp,user):

    subject = "OTP Verification"

    html = render_to_string('myapp/email.html',{
        'name': name,
        'otp': otp,
        'user' :user,
    })

    mail = EmailMessage(
        subject,
        html,
        settings.EMAIL_HOST_USER,
        [email]
    )

    mail.content_subtype = "html"
    mail.send()

@check_login
def index(request):
    uid = request.uid
    # post_all = InstaPost.objects.all().order_by('-created_at')
    post_all = InstaPost.objects.exclude(user = uid).order_by('-created_at')
    users = InstaUser.objects.exclude(username = uid.username)
    my_following = FollowUsers.objects.filter(Following = uid ).values_list("Following_person_id",flat=True)
    context = {'uid' : uid,'post_all' : post_all,'users' :  users,'my_following' : my_following}
    return render(request, "myapp/index.html",context)

@check_login
def profile(request):
    uid = request.uid
    user_id = InstaUser.objects.get(username=uid).id
    posts = InstaPost.objects.filter(user = uid).order_by('-created_at')
    followers_count = FollowUsers.objects.filter(Following_person=uid).count()
    following_count = FollowUsers.objects.filter(Following=uid).count()
    context = {'uid' : uid , 'posts' : posts , 'followers_count':followers_count,'following_count':following_count}
    return render(request, "myapp/profile.html",context)


def register(request):
    if request.POST:
        full_name = request.POST['full_name']
        username = request.POST['username']
        email = request.POST['email']
        gender = request.POST['gender']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if InstaUser.objects.filter(email = email).exists():
            return render(request, "myapp/register.html",{'e_msg' : "Email already exists"})
        
        if InstaUser.objects.filter(username = username).exists():
            return render(request, "myapp/register.html",{'e_msg' : "Username already exists"})
        
        if password != confirm_password:
            return render(request, "myapp/register.html",{'e_msg' : "Passwords do not match"})
        
        else:
            if gender == "male":
                img = "images/boy.png"
            elif gender == "female":
                img = "images/girl.png"

            InstaUser.objects.create(
                    name = full_name,
                    username = username,
                    email = email,
                    password = make_password(password),
                    profile_pic = img ,
                    gender = gender
                    )
                    
            return redirect("login")

    return render(request,"myapp/register.html")

@check_login
def logout(request):
    uid = request.uid
    uid.is_active = False
    uid.save()
    del request.session['email']
    return redirect("login")
            
def forgot_password(request):
    if request.POST:
        email = request.POST['email']
        uid = InstaUser.objects.get(email = email)
        otp_ = random.randint(1000,9999)
        user = uid.username
        name = uid.name
        uid.otp = otp_
        uid.save()
        print("----------------->",otp_)
        if email == uid.email:
            # send_email(email,name,otp_,user)
            return render(request,"myapp/otp.html",{'email' : email})
    else:
        return render(request, "myapp/ForgotPassword.html")

def otp(request):
    if request.POST:
        email = request.POST['email']
        otp_ = request.POST['onetime']
        uid = InstaUser.objects.get(email = email)

        if int(otp_) == int(uid.otp):
            return render(request,"myapp/resetpassword.html",{'email' : email })
            
        else:
            return render(request, "myapp/ForgotPassword.html")
    else:
        return render(request, "myapp/ForgotPassword.html")
   
def resetpassword(request): 
    #  Confirm password
    if request.POST:
         email = request.POST['email']
         uid = InstaUser.objects.get(email = email)
         new_password = request.POST['new_password']
         confirm_password = request.POST['confirm_password']

         if new_password == confirm_password:
             uid.password = make_password(new_password)
             uid.save()
             return redirect('login')
         
    else:
     return redirect('forgot_password')
    
    
@check_login
def edit_profile(request):
    uid = request.uid 
    if request.POST:
        #uid = InstaUser.objects.get(email = request.session['email'])
        uid.username = request.POST['username']
        uid.name = request.POST['name']
        uid.bio = request.POST['bio']
        uid.description = request.POST['description']
        uid.link = request.POST['link']

        if 'profile_pic' in request.FILES:
            uid.profile_pic = request.FILES['profile_pic']

        uid.save()
        return redirect("profile")
    
    return render(request,"myapp/edit_profile.html",{'uid':uid})


@check_login
def create(request):
    uid = request.uid
    if request.POST:
        caption = request.POST['caption']
        location = request.POST['location']
        tagged_users = request.POST['tagged_users']
        post_image = request.FILES['post_image']

        InstaPost.objects.create(
            user = uid,
            caption = caption,
            location = location,
            image = post_image,
        )
        return redirect("index")
    return render(request, "myapp/create.html",{'uid':uid})

@check_login
def following(request):
    uid = request.uid
    users = InstaUser.objects.exclude(username = uid.username)
    my_following = FollowUsers.objects.filter(Following = uid ).values_list("Following_person_id",flat=True)
    print("------->",uid)
    context ={'uid' : uid , 'users' : users , 'my_following' : my_following , }
    return render(request,"myapp/Following.html",context)
    
@check_login
def follow_unfollow(request,pk):
    uid = request.uid
    target_user = InstaUser.objects.get(id = pk)

    Following_person = FollowUsers.objects.filter(
        Following=uid,
        Following_person= target_user
    )
    notification_ = notification.objects.filter(
        sender = uid,
        reciver = target_user
    )
    if Following_person:
        Following_person.delete()
        notification_.delete()
    else:
        FollowUsers.objects.create(
            Following=uid,
            Following_person= target_user)
        
        notification.objects.create(    
            sender = uid ,
            reciver = target_user,
            message = "Started following you",
            notification_type = 'follow'
        )
    return redirect(request.META.get('HTTP_REFERER', reverse('index')))

# @check_login
# def follow_index(request,pk):
    uid = request.uid
    target_user = InstaUser.objects.get(id = pk)
    FollowUsers.objects.create(
        Following=uid,
        Following_person= target_user)
    notification.objects.create(
            sender = uid ,
            reciver = target_user,
            message = "Started following you" ,
            notification_type = 'follow')
    return redirect(index)

@check_login
def followers(request):
    uid = request.uid
    my_following = FollowUsers.objects.filter(Following = uid ).values_list("Following_person_id",flat=True)
    followers =  FollowUsers.objects.filter(Following_person= uid)
    context = {'uid' : uid , 'followers':followers , 'my_following' : my_following}
    return render(request,"myapp/Followers.html",context)

@check_login
def search(request):
    uid = request.uid
    all_posts = InstaPost.objects.exclude(user = uid)
    all_reels = instrareels.objects.exclude(user = uid)
    reel_post = list(all_posts) + list(all_reels)
    random.shuffle(reel_post)
    all_comments = comments.objects.exclude(user_fk = uid)
    context = {'uid':uid, 'all_posts' : reel_post,'all_comments' : all_comments}
    return render(request, "myapp/search.html",context)

@check_login
def reels(request):
    uid = request.uid
    reels = instrareels.objects.all().order_by('-created_at')
    context = {'uid' : uid , 'reels' : reels}
    return render(request, "myapp/reels.html",context)

@check_login
def messages(request, pk=None):
    uid = request.uid
    my_following = FollowUsers.objects.filter(Following=uid)
    users = [f.Following_person for f in my_following]

    chat_user = None
    chat_room_obj = None
    chat_messages = []

    if pk:
        chat_user = InstaUser.objects.get(id=pk)
        chat_room_obj = chatroom.objects.filter(user=uid, user2=chat_user).first()
        if not chat_room_obj:
            chat_room_obj = chatroom.objects.filter(user=chat_user, user2=uid).first()
        
        if not chat_room_obj:
            chat_room_obj = chatroom.objects.create(user=uid, user2=chat_user)

        if request.POST:
            content = request.POST.get('content')
            if content:
                role = 'sender' if uid == chat_room_obj.user else 'receiver'
                message.objects.create(
                    chat_room=chat_room_obj,
                    role=role,
                    content=content
                )
                return redirect('messages_chat', pk=pk)

        chat_messages = message.objects.filter(chat_room=chat_room_obj).order_by('created_at')

    context = {
        'uid': uid,
        'users': users,
        'chat_user': chat_user,
        'chat_messages': chat_messages,
        'chat_room': chat_room_obj,
    }
    return render(request, "myapp/messages.html", context)

@check_login
def notifications(request):
    uid = request.uid
    my_following = FollowUsers.objects.filter(Following = uid ).values_list("Following_person_id",flat=True)
    all_notifications = notification.objects.filter(reciver=uid).order_by("-created_at")
    context = {'uid' : uid , 'all_notifications' : all_notifications,'my_following' : my_following}
    return render(request, "myapp/notifications.html",context)

@check_login
def upload_reels(request):
    uid = request.uid
    if request.POST:
        caption = request.POST['caption']
        video = request.FILES['reel_video']

        instrareels.objects.create(
            user = uid,
            caption = caption,
            video = video,
        )
        return redirect("index")
    return render(request, "myapp/upload_reel.html",{'uid':uid})

@check_login
def post_like(request,pk):
    uid = request.uid

    try:
        post = InstaPost.objects.get(id=pk)
        is_post = True
    except:
        post = instrareels.objects.get(id=pk)
        is_post = False

    target_user = post.user

    notification_ = notification.objects.filter(
        sender=uid,
        reciver=target_user
    )

    if is_post:
        liked_post = like_unlike.objects.filter(user_fk=uid, post_fk=post)

        if liked_post.exists():
            liked_post.delete()
            notification_.delete()
        else:
            like_unlike.objects.create(
                user_fk=uid,
                post_fk=post
            )

            if uid != target_user:
                if is_post:
                    notification.objects.create(
                        sender=uid,
                        reciver=target_user,
                        post_fk=post,
                        message="Liked your post",
                        notification_type='like'
                    )

    else:
        liked_reel = like_unlike.objects.filter(user_fk=uid, reel_fk=post)

        if liked_reel.exists():
            liked_reel.delete()
            notification_.delete()
        else:
            like_unlike.objects.create(
                user_fk=uid,
                reel_fk=post
            )

            if uid != target_user:
                notification.objects.create(
                    sender=uid,
                    reciver=target_user,
                    reel_fk=post,
                    message="Liked your reel",
                    notification_type='like'
                )

    return redirect(request.META.get('HTTP_REFERER', reverse('index')))

@check_login
def post_comment(request,pk):
    uid = request.uid
    comment = request.POST.get('comment')
    print('--->',comment)
    print("POST:", request.POST)
    try:
        post = InstaPost.objects.get(id=pk)
        is_post = True
    except:
        reel = instrareels.objects.get(id=pk)
        is_post = False
    
    target_user = post.user
    notification_ = notification.objects.filter(
        sender=uid,
        reciver=target_user,
        notification_type = 'comment'
    )
    if is_post:
        comments.objects.create(
            user_fk=uid,
            post_fk=post,
            comment =comment
        )       
        if uid != target_user:
            if is_post:
                notification.objects.create(
                    sender=uid,
                    reciver=target_user,
                    post_fk=post,
                    message ="commented in yor post",
                    notification_type='comment'
                )

    else:
        pass

    return redirect(request.META.get('HTTP_REFERER', reverse('index')))

@check_login
def comment_view(request,pk):
    uid = request.uid
    post = InstaPost.objects.get(id=pk)
    post_comments = comments.objects.filter(post_fk=post).order_by('-created_at')
    context = {'post': post,'comments': post_comments}

    return render(request,"myapp/comment_view.html",context)
    #  return redirect(request.META.get('HTTP_REFERER', reverse('index')))
@check_login
def user_profile(request,pk):
    profile_user = InstaUser.objects.get(id=pk)
    user_following = FollowUsers.objects.filter(Following = pk ).values_list("Following_person_id",flat=True)
    followers =  FollowUsers.objects.filter(Following_person= pk)
    posts = InstaPost.objects.filter(user = pk).order_by('-created_at')
    followers_count = FollowUsers.objects.filter(Following_person=pk).count()
    following_count = FollowUsers.objects.filter(Following=pk).count()
    context = {'profile_user' : profile_user , 'posts' : posts , 'followers_count':followers_count,'following_count':following_count,'followers':followers,'user_following':user_following}

    return render(request,"myapp/user_profile.html",context)

def user_following(request,pk):
    profile_user = InstaUser.objects.get(id=pk)
    users = InstaUser.objects.exclude(username = profile_user.username)
    user_following = FollowUsers.objects.filter(Following = pk ).values_list("Following_person_id",flat=True)
    # user_following = InstaUser.objects.filter(id__in=following_ids)
    print("==============>",profile_user,user_following)

    context = {'profile_user' : profile_user ,'user_following' : user_following,'users':users}
    return render(request,"myapp/user_following.html",context)

@check_login
def user_followers(request,pk):
    uid = request.uid
    profile_user = InstaUser.objects.get(id=pk)
    followers =  FollowUsers.objects.filter(Following_person = profile_user)
    my_following = FollowUsers.objects.filter(Following = uid ).values_list("Following_person_id",flat=True)
    context = {'profile_user' : profile_user,'followers' : followers,'my_following':my_following}
    return render(request,"myapp/user_followers.html",context)

