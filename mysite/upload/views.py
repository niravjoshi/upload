from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from upload.forms import UserFileForm, UserForm
from upload.models import Ufile, UserProfile

def login_page(request):
    params = {}
    if request.method == "POST" :
        try:
            #
            # Checking if its login or signup request.
            #
            if request.POST.get('login'):
                email = request.POST.get('email')
                passwd = request.POST.get('password')
                if email and passwd:
                    #
                    # login request
                    #
                    user = authenticate(email=email, password=passwd)
                    print "user: ", user
                    if user is not None:
                        if user.is_active:
                            login(request, user)
                            logged = None
                            params['logged'] = "Logged in successfully"
                            return render_to_response('top.html', params, context_instance=RequestContext(request))
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
                        new_user = User.objects.create_user(fname, email, password=passwd, last_name=lname)
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

#@login_required
def demo(request):
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
                #
                # Get the user's email ID and check whether user exists or not. 
                #
                pf_user_email = request.POST.get('user_email')
                try:
                    userprofile = UserProfile.objects.get(user_email=pf_user_email)
                    user = User.objects.get(email=pf_user_email)
                except Exception, e:
                    userprofile = None
                    user = None
                    print "Error: ", str(e)
                #
                # Store file name and if user exists then add uploaded file to that user's account. 
                #
                file_name = request.FILES['user_file']
                if userprofile:
                    params['user'] = user.username
                    print "Old User: ", user.username

                    ufile = Ufile.objects.create(user_file=file_name, user_profile=userprofile, file_name=file_name)
                    ufile.save()
                    print "File saved"
                    success = True

                else:
                    #
                    # Creating new user
                    #
                    user = User.objects.create_user(pf_user_email, pf_user_email, None)
                    user.save()

                    params['user'] = user.username
                    print "New User: ", user.username
                    userprofile = UserProfile.objects.create(user_email=pf_user_email)
                    userprofile.save()
                    print "Email saved"

                    ufile = Ufile.objects.create(user_file=file_name,user_profile=userprofile, file_name=file_name)
                    ufile.save()
                    print "File saved"
                    success = True

                #
                # Fetch all file names of this user
                #
                if success:
                    params['files'] = Ufile.objects.filter(user_profile=userprofile)

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
    return render_to_response('top.html', params, context_instance=RequestContext(request))
