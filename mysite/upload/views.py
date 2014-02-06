from django.shortcuts import render_to_response
from django.template import RequestContext

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
                    profile_user = UserProfile.objects.get(user_email=pf_user_email)
                except:
                    profile_user = None
                #
                # Store file name and if user exists then add uploaded file to that user's account. 
                #
                file_name = request.FILES['user_file']
                if profile_user:
                    print "Old User"
                    ufile = Ufile.objects.create(user_file=file_name, user_profile = profile_user)
                    ufile.save()
                    print "File saved"
                    success = True
                #
                # If new user arrives.
                #
                else:
                    print "New User"
                    uprofile = UserProfile.objects.create(user_email=pf_user_email)
                    uprofile.save()
                    print "Email saved"
                    ufile = Ufile.objects.create(user_file=file_name,user_profile=uprofile)
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

    params['form'] = form
    params['success'] = success
    params['file_name'] = file_name
    return render_to_response('top.html', params, context_instance=RequestContext(request))
