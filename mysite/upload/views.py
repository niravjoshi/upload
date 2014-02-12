from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User

from upload.forms import UserFileForm
from upload.models import Ufile, UserProfile

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
