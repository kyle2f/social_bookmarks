from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts  import render
# from django.contrib.auth import authenticate, login
# from .forms import LoginForm

from django.contrib.auth.decorators import login_required

from .models import Profile
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm

# # Create your views here.

# def user_login(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             cleaned_data = form.cleaned_data
#             user = authenticate(request, username=cleaned_data['username'], password = cleaned_data['password'])
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     return HttpResponse('Authenticated successfully')
#                 else:
#                     return HttpResponse('Disabl/login/ed Account')
#             else:
#                 return HttpResponse('Invalid Login')    
#     else:
#         form = LoginForm()
#     return render(request, 'account/login.html', {'form':form})


def register(request):
    user_form = None
    if (request.method == 'POST'):
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            #Create a new user object but avoid saving it yet
            new_user = user_form.save(commit= False)
            #set the chosen password
            new_user.set_password(
                user_form.cleaned_data['password']
            )
            #save the User object
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(request, 'account/register_done.html' ,{'new_user':new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html',{'user_form':user_form})

@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user , data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render('request', 'account/edit.html' ,
                        {'user_form':user_form,'profile_form':profile_form})


@login_required
def dashboard(request):
    return render(request,'account/dashboard.html', {'section':'dashboard'})

