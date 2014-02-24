from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from upload.forms import UserFileForm, UserForm
from upload.models import Ufile

def login_page(request):
    params = {}
    #
    # Checking if user is already logged in or not.
    #
    if request.user.is_authenticated():
        return render_to_response('upload.html', params, context_instance=RequestContext(request))
    #
    # If post request
    #
    if request.method == "POST" :
        try:
            #
            # Checking if its login or signup request.
            #
            if request.POST.get('login_page'):
                #
                # Login request
                #
                email = request.POST.get('email')
                passwd = request.POST.get('password')
                if email and passwd:
                    #
                    # login request, authenticate user then active and log the user in current session.
                    #
                    user = authenticate(username=email, password=passwd)
                    if user is not None:
                        if user.is_active:
                            login(request, user)
                            params['user'] = User.objects.get(username=user)
                            return render_to_response('upload.html', params, context_instance=RequestContext(request))
                    else:
                        invalid = None
                        params['invalid'] = "Invalid email-id or password"
                        return render_to_response('login.html', params, context_instance=RequestContext(request))
                else:
                    required = None
                    params['required'] = "Both fields are required"
                    return render_to_response('login.html', params, context_instance=RequestContext(request))
            #
            # Signup request
            #
            else:
                form = UserForm(request.POST)
                if form.is_valid():
                    email = form.cleaned_data['email']
                    #
                    # Check if user exists with given email-id.
                    #
                    try:
                        user = User.objects.get(email=email)

                    except Exception, e:
                        print "User Error: %s" %str(e)
                        user = None
                    #
                    # Check if user's email-id is already used and if used give an error.
                    #
                    if user:
                        user_exists = None
                        params['user_exists'] = "User with %s email-id already exists." %email
                    #
                    # New user registration
                    #
                    else:
                        passwd = form.cleaned_data['password']
                        fname = form.cleaned_data['first_name']
                        lname = form.cleaned_data['last_name']
                        new_user = User.objects.create_user(email, email, password=passwd, first_name=fname, last_name=lname)
                        new_user.save()
                        print "user saved"
                        print "fname: %s\nlname: %s\nemail: %s\npasswd: %s" %(fname,lname,email,passwd)
                        params['form'] = form
                        user_created = None
                        params['user_created'] = "Congrats!!! Account created successfully."
                #
                # Form is invalid
                #
                else:
                    if "@" and ".com" not in request.POST.get('email') and request.POST.get('first_name'):
                        valid_email = None
                        params['valid_email'] = "Please enter a valid email address."
                    else:
                        valid_input = None
                        params['valid_input'] = "All fields are required."



        except Exception, e:
            params['form'] = form
            some_error = None
            params ['some_error'] = "Oh snap! Something went wrong!!!\n Please try again."
            print "Login Error: %s" %str(e)
    else:
        params['form'] = UserForm()

    return render_to_response('login.html', params, context_instance=RequestContext(request))

@login_required(login_url = '/login/')
def upload(request, id):
    params = {}
    success = False
    file_name = None
    try:
        if request.method == 'POST':
            #
            # Create instance of UserFileForm object
            #
            form = UserFileForm(request.POST, request.FILES)
            if form.is_valid():
                print "form is valid"
                file_name = request.FILES['user_file']
                user = User.objects.get(username = request.user)
                ufile = Ufile.objects.create(user_file=file_name, user_profile=user, file_name=file_name)
                ufile.save()
                print "File saved"
                success = True
                #
                # Fetch all file names of this user
                #
                if success:
                    params['files'] = Ufile.objects.filter(user_profile=user)
            #
            # Form is invalid.
            #
            else:
                form = UserFileForm(request.POST)
                print "form is not valid"
                print "Form Error : ", form.errors
        #
        # Get method
        #
        else:
            form = UserFileForm()
            
    except Exception, e:
        print "Error is: ", str(e)

    params['form'] = form
    params['success'] = success
    params['file_name'] = file_name
    return render_to_response('upload.html', params, context_instance=RequestContext(request))

@login_required(login_url = '/login/')
def logout_page(request):
    params = {}
    logout(request)
    return render_to_response('logout.html', params, context_instance=RequestContext(request))
