from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.views.decorators.cache import cache_control
from django.core.mail import send_mail
from datetime import datetime, timedelta
from django.conf import settings
from .models import Job_Seeker, Recruiter, AppliedPost, Job_Post, Feedback, User, ChatMessage
from .forms import UserForm, JobSeekerProfileForm, RecruiterProfileForm

def home(request):
    feeds = Feedback.objects.all()
    jobs = list(Job_Post.objects.all())
    today = datetime.now().strftime("%Y-%m-%d")
    today = datetime.date(datetime.strptime(today, "%Y-%m-%d"))
    users = User.objects.all()
    for i in jobs:
        if today - i.upto >= timedelta(2): 
            print(i.post)
            i.delete()

    # print(today)
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        password = request.POST.get('password')


        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email ID already used.')
            return HttpResponseRedirect('/')
        
        if len(password) < 8:
            messages.error(request, 'Password must be 8 character long.')
            return HttpResponseRedirect('/')

        if not any(x.isdigit() for x in password):
            messages.error(request, 'Password must contain at least one digit.')
            return HttpResponseRedirect('/')

        if not any(x.islower() for x in password):
            messages.error(request, 'Password must contain at least one small letter.')
            return HttpResponseRedirect('/')

        if not any(x.isupper() for x in password):
            messages.error(request, 'Password must contain at least one capital letter.')
            return HttpResponseRedirect('/')

        else:
            usr = User.objects.create_user(username=email, email=email, password=password)
            usr.first_name = fname
            usr.last_name = lname
            usr.save()

            user = Job_Seeker(user=usr, phone=mobile)
            user.save()
            messages.success(request, 'Candidate Registered successfully.')
            return HttpResponseRedirect('/')


    return render(request, 'home.html', {'users': users, 'jobs' : jobs, 'feedbacks' : feeds, 'today' : today})


def registerRecruiter(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        cname = request.POST.get('cname')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(email=email).exists():
            print("Email ID already used.")
            messages.error(request, 'Email ID already used.')
            return HttpResponseRedirect('/registerRecruiter')
        
        if len(password) < 8:
            messages.error(request, 'Password must be 8 character long.')
            return HttpResponseRedirect('/')

        if not any(x.isdigit() for x in password):
            messages.error(request, 'Password must contain at least one digit.')
            return HttpResponseRedirect('/')

        if not any(x.islower() for x in password):
            messages.error(request, 'Password must contain at least one small letter.')
            return HttpResponseRedirect('/')

        if not any(x.isupper() for x in password):
            messages.error(request, 'Password must contain at least one capital letter.')
            return HttpResponseRedirect('/')

        else:
            usr = User.objects.create_user(username=email, email=email, password=password)
            usr.first_name = fname
            usr.last_name = lname
            usr.is_staff = True
            usr.save()

            user = Recruiter(user=usr, phone=mobile, company=cname)
            user.save()
            messages.success(request, 'Recruiter Registered successfully.')
            return HttpResponseRedirect('/')
    return render(request, 'registerRecruiter.html')


@cache_control(no_cache=True, must_revalidade=True, no_store=True)
def loginUser(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')
        # print(username, password)
        
        if User.objects.filter(username=username):  
            usr = authenticate(username=username, password=password)
            if usr:
                login(request, usr)
                messages.success(request, 'Login successful.')
                return HttpResponseRedirect('/')
            else:
                messages.error(request, 'Wrong username or password.')
                return HttpResponseRedirect('loginUser')
        else:
            messages.error(request, 'No user found.')
            return HttpResponseRedirect('/')

@login_required(login_url='loginUser')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def profile(request):
    try:
        user = request.user
        profile = None
        applied_posts = None
        profile_type = None

        if hasattr(user, 'job_seeker'):
            profile = user.job_seeker
            applied_posts = AppliedPost.objects.filter(applied_by=profile).select_related('job__user')
            profile_type = 'job_seeker'
        elif hasattr(user, 'recruiter'):
            profile = user.recruiter
            applied_posts = AppliedPost.objects.filter(job__user=profile).select_related('applied_by__user')
            profile_type = 'recruiter'

        context = {
            'profile': profile,
            'applied_posts': applied_posts,
            'profile_type': profile_type,
            'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
        }
        return render(request, 'profile.html', context)

    except Exception as e:
        print("Error in profile view: ", e)
        messages.error(request, 'An error occurred while loading the profile.')
        return redirect('/')


@login_required(login_url='loginUser')
def edit_profile(request):
    try:
        user = request.user
        profile = None
        profile_form = None

        if hasattr(user, 'job_seeker'):
            profile = user.job_seeker
            profile_form = JobSeekerProfileForm(instance=profile)
        elif hasattr(user, 'recruiter'):
            profile = user.recruiter
            profile_form = RecruiterProfileForm(instance=profile)

        if request.method == 'POST':
            user_form = UserForm(request.POST, instance=user)
            if hasattr(user, 'job_seeker'):
                profile_form = JobSeekerProfileForm(request.POST, request.FILES, instance=profile)
            elif hasattr(user, 'recruiter'):
                profile_form = RecruiterProfileForm(request.POST, request.FILES, instance=profile)

            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()

                address = request.POST.get('address')
                latitude = request.POST.get('latitude')
                longitude = request.POST.get('longitude')

                if hasattr(user, 'job_seeker'):
                    profile.address = address
                    profile.latitude = latitude
                    profile.longitude = longitude
                elif hasattr(user, 'recruiter'):
                    profile.address = address
                    profile.latitude = latitude
                    profile.longitude = longitude
                
                profile.save()
                messages.success(request, 'Profile updated successfully.')
                return redirect('profile')

        else:
            user_form = UserForm(instance=user)

        context = {
            'user_form': user_form,
            'profile_form': profile_form,
            'profile': profile,
            'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,  # Pass your API key to the template
        }
        return render(request, 'edit_profile.html', context)

    except Exception as e:
        print("Error in edit_profile view: ", e)
        messages.error(request, 'An error occurred while updating the profile.')
        return redirect('/')
    
# @login_required(login_url='loginUser')
# @cache_control(no_cache=True, must_revalidade=True, no_store=True)
# def profile(request):
#     applied = 0
#     appliers = []
#     applied_list = []
    
#     if Job_Seeker.objects.filter(user=request.user):
#         user_detaile = Job_Seeker.objects.get(user=request.user)
#         applied = len(AppliedPost.objects.filter(applied_by=user_detaile))
#         applied_list = list(AppliedPost.objects.filter(applied_by=user_detaile))
#     elif Recruiter.objects.filter(user=request.user):
#         user_detaile = Recruiter.objects.get(user=request.user)

#         for i in AppliedPost.objects.all():
#             if i.job.user == user_detaile:
#                 appliers.append(Job_Seeker.objects.get(user=i.applied_by.user))
                
#     return render(request, 'profile.html', {'userDetail' : user_detaile, 'applied': applied, 'applied_to' : applied_list, 'appliers' : appliers})

@cache_control(no_cache=True, must_revalidade=True, no_store=True)
def logoutuser(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return HttpResponseRedirect('/')

def apply(request, job_id):
    post = Job_Post.objects.get(id=job_id)
    applier = Job_Seeker.objects.get(user=request.user)

    if AppliedPost.objects.filter(applied_by=applier):
        for i in AppliedPost.objects.filter(applied_by=applier):
            if i.job == post:
                messages.error(request, 'Already applied')
                return HttpResponseRedirect('/')

    
    job_obj = AppliedPost(applied_by=applier, job=post, applied_on=datetime.now())
    job_obj.save()
        
    from_mail = settings.EMAIL_HOST_USER
    to_mail = [request.user.email]
    try:
        send_mail('About apply to job', f'You have applied for the Post of {post.post} on JobPortal.com . Congrats! you will here from recruiter soon.', from_mail, to_mail)
    except:
        print('Email not found.')
    messages.success(request, 'Congrats Applied successfully.')
    return HttpResponseRedirect('/')

@login_required(login_url='loginUser')
def addPost(request):
    if request.method == 'POST':
        user = Recruiter.objects.get(user=request.user)
        post = request.POST.get('post')
        salary = int(request.POST.get('salary'))
        description = request.POST.get('description')
        posted_on = datetime.now()
        upto = request.POST.get('upto')

        job_obj = Job_Post(user=user, post=post, salary=salary, description=description, posted_on=posted_on, upto=upto)
        job_obj.save()
        messages.success(request, 'Posted Successfully.')
        return HttpResponseRedirect('/')

def feedback(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        feedback = request.POST.get('feedback')

        feedback_obj = Feedback(name=name, email=email, feedback=feedback)
        feedback_obj.save()
        messages.success(request, 'Thanks for feedback !')
        return HttpResponseRedirect('/')

def about(request):
    return render(request, 'aboutus.html')

def searched(request):
    feeds = Feedback.objects.all()
    today = datetime.now().strftime("%Y-%m-%d")

    if request.method == 'POST':
        searchType = request.POST.get('query')

        matched = list()
        for i in Job_Post.objects.all():
            if (str(searchType).lower()) in str(i.post).lower():
                matched.append(i)
        if len(matched) == 0:
            
            messages.error(request, 'No job till now.')
            return HttpResponseRedirect('/')
        else:
            return render(request, 'home.html', {'jobs' : matched, 'feedbacks' : feeds, 'today' : today})
        

def manage_applications(request):
    if request.method == 'POST':
        application_id = request.POST.get('application_id')
        action = request.POST.get('action')

        try:
            application = AppliedPost.objects.get(id=application_id)
            if action == 'accept':
                application.status = 'selected'
                application.save()
                messages.success(request, 'Application selected successfully.')
            elif action == 'reject':
                application.status = 'rejected'
                application.save()
                messages.success(request, 'Application rejected successfully.')
            else:
                messages.error(request, 'Invalid action.')
        except AppliedPost.DoesNotExist:
            messages.error(request, 'Application not found.')

        return redirect('manage_applications')

    # Fetch all applications for GET request
    applications = AppliedPost.objects.all()
    return render(request, 'manage_applications.html', {'applications': applications})


@login_required(login_url='loginUser')
def accept_application(request, application_id):
    try:
        application = get_object_or_404(AppliedPost, id=application_id)
        application.status = 'Selected'
        application.save()
        messages.success(request, 'Application selected.')
    except Exception as e:
        messages.error(request, f'An error occurred: {str(e)}')
    return redirect('manage_applications')

@login_required(login_url='loginUser')
def reject_application(request, application_id):
    try:
        application = get_object_or_404(AppliedPost, id=application_id)
        application.status = 'Rejected'
        application.save()
        messages.success(request, 'Application rejected.')
    except Exception as e:
        messages.error(request, f'An error occurred: {str(e)}')
    return redirect('manage_applications')

@login_required(login_url='loginUser')
@cache_control(no_cache=True, must_revalidade=True, no_store=True)
def update_application_status(request, application_id):
    if request.method == 'POST':
        application = AppliedPost.objects.get(id=application_id)
        status = request.POST.get('status')
        application.status = status
        application.save()
        messages.success(request, f'Application status updated to {status}.')
        return redirect('profile')

@login_required(login_url='loginUser')
def chat_view(request, email=None):
    users = User.objects.exclude(id=request.user.id)
    active_user = None
    chat_messages = []

    if email:
        try:
            active_user = get_object_or_404(User, email=email)
            chat_messages = list(ChatMessage.objects.filter(
                sender=request.user, receiver=active_user
            ).union(
                ChatMessage.objects.filter(sender=active_user, receiver=request.user)
            ).order_by('timestamp').values(
                'sender__email', 'message', 'timestamp', 'sender__first_name', 'sender__last_name'
            ))
        except User.DoesNotExist:
            active_user = None

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'messages': chat_messages})

    return render(request, 'chat.html', {
        'users': users,
        'active_user': active_user,
        'chat_messages': chat_messages
    })

@login_required(login_url='loginUser')
def send_message(request):
    if request.method == 'POST':
        receiver_email = request.POST.get('receiver_email')
        message = request.POST.get('message')

        if receiver_email and message:
            try:
                receiver = get_object_or_404(User, email=receiver_email)
                ChatMessage.objects.create(sender=request.user, receiver=receiver, message=message)
                return JsonResponse({'status': 'success'})
            except User.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Receiver not found'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})