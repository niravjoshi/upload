# Python
import os

# Django
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Model
from django.contrib.auth.models import User
from upload.forms import UserFileForm, UserForm
from upload.models import Ufile, LinkValidate

# Constants
from upload.constants import FILEPATH

# Utils
from upload.utils import send_mail


def login_page(request):
    params = {}
    #
    # Checking if user is already logged in or not.
    #
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse(upload))
        #return render_to_response('upload.html', params, context_instance=RequestContext(request))
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
                            return HttpResponseRedirect(reverse(upload))
                        else:
                            params ['user_email'] = email
                            params ['not_verified'] = "Your email address is not yet verified"
                    else:
                        params['invalid'] = "Invalid email-id or password"
                else:
                    required = None
                    params['required'] = "Both fields are required"
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
                        new_user.is_active = False
                        new_user.save()
                        print "user saved"
                        print "fname: %s\nlname: %s\nemail: %s\npasswd: %s" %(fname,lname,email,passwd)
                        params['form'] = form
                        user_created = None
                        params['user_created'] = "Your registration is completed"
                        params['user_email'] = new_user.email
                        #
                        # Sending mail to user for email verification.
                        #
                        send_mail(new_user)
                        print "Email sent successfully."
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
            params ['some_error'] = "Something went wrong. Please try again."
            print "Login Error: %s" %str(e)
    else:
        params['form'] = UserForm()

    return render_to_response('login.html', params, context_instance=RequestContext(request))

def validate_email(request, user, key):
    params = {}
    verified, already_verified = False, False
    try:
        #
        # Verfiying whether this user's email address and key exists in database or not.
        #
        validate_user = LinkValidate.objects.get(rand_key=key)
        if validate_user:
            if validate_user.user.is_active:
                params['email'] = validate_user.user.email
                already_verified = True
            else:
                user_name = validate_user.user.first_name + validate_user.user.last_name
                if user_name == user:
                    #
                    # As user exists with given email and key, activate that user
                    #
                    real_user = User.objects.get(email=validate_user.user.email)
                    real_user.is_active = True
                    real_user.save()
                    verified = True
                    params['email'] = real_user.email
                    print "User's email is verified."
        else:
            print "User does not exist."
    except Exception, e:
        print "Validate email error: ", str(e)

    params['verified'] = verified
    params['already_verified'] = already_verified
    return render_to_response('validate_email.html', params, context_instance=RequestContext(request))



@login_required(login_url = '/login/')
def upload(request):
    params = {}
    success = False
    file_exists = False
    file_name = None
    try:
        if request.method == 'POST':
            #
            # Create instance of UserFileForm object
            #
            form = UserFileForm(request.POST, request.FILES)
            if form.is_valid():
                print "form is valid"
                user = User.objects.get(username = request.user)
                file_name = request.FILES['user_file']
                #
                # Setting file name in lowercase for the ease of sorting it.
                #
                file_name._set_name(file_name.name.lower())
                #
                # Verifying whether file with same name exists or not for that user.
                #
                try:
                    file_check = Ufile.objects.get(user_profile=user, file_name=file_name)
                except Exception, e:
                    file_check = None
                    print "File saving error: ", str(e)

                if file_check:
                    params['file_exists'] = True
                else:
                    ufile = Ufile.objects.create(user_file=file_name, user_profile=user, file_name=file_name)
                    ufile.save()
                    print "File saved"
                    success = True
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
    #
    # Fetching all files of this user.
    #
    params['files'] = Ufile.objects.filter(user_profile=request.user)
    params['form'] = form
    params['success'] = success
    params['file_name'] = file_name
    return render_to_response('upload.html', params, context_instance=RequestContext(request))


def file_sort(request):
    params = {}
    sorted_files = []
    unsorted_files = []
    try:
        sorted_files = Ufile.objects.filter(user_profile=request.user).order_by('file_name')
    except Exception, e:
        print "File sorting error: ", str(e)

    params['files'] = sorted_files
    params['form'] = UserFileForm()
    return render_to_response('upload.html', params, context_instance=RequestContext(request))


def upload_file_op(request, id):
    try:
        f = Ufile.objects.get(id=id)
        filename = f.user_file.url.split('/')[-1]
        response = HttpResponse(f.user_file, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename=%s' %filename
    except Exception, e:
        print "File error: ", str(e)
    return response


@login_required(login_url = '/login/')
def upload_delete(request, id):
    params = {}
    del_success = False
    try:
        f = Ufile.objects.get(id=id)
        #
        # Deleting file
        #
        os.remove(FILEPATH + f.user_file.url)
        #
        # Saving file name and as file is actually deleted so removing file entry from database.
        #
        params['file_delete'] = f.file_name
        f.delete()
        del_success = True
    except Exception, e:
        print "File delete error: ", str(e)

    params['form'] = UserFileForm()
    params['files'] = Ufile.objects.filter(user_profile=request.user)
    params['del_success'] = del_success
    return render_to_response('upload.html', params, context_instance=RequestContext(request))

@login_required(login_url = '/login/')
def logout_page(request):
    params = {}
    logout(request)
    return render_to_response('logout.html', params, context_instance=RequestContext(request))
