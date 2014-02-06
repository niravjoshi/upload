from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt

from upload.forms import UserFileForm
from upload.models import Ufile, UserProfile

def demo(request):
    params = {}
    success = False
    file_name = None
    form = UserFileForm()
    try:
        if request.method == 'POST':
            pf_user = request.POST.get('user_email')

            try:
                profile_user = UserProfile.objects.get(user_email=pf_user)
            except Exception, e:
                print "User Error ==> %s" %str(e)
                profile_user=None

            if profile_user:
                form = UserFileForm(request.POST, request.FILES)
                print "POST method"
                if form.is_valid():
                    print "form is valid"
                    #form.save()
                    ufile = Ufile.objects.create(user_file=file_name, user_profile = profile_user)
                    ufile.save()
                    print "form saved"
                    success = True
                    file_name = request.FILES['user_file']

                else:
                    form = UserFileForm(request.POST)
                    print "form is not valid"
                    print "Error ==> ", form.errors

            else:
                form = UserFileForm(request.POST, request.FILES)
                if form.is_valid():
                    user_profile = UserProfile.objects.create(user_email=pf_user)
                    user_profile.save()
                    file_name = request.FILES['user_file']
                    user_file = Ufile.objects.create(user_file=file_name,user_profile=user_profile)
                    user_file.save()
                    success = True
                    file_name = request.FILES['user_file']
                else:
                    form = UserFileForm(request.POST)
                    print "form is not valid"
                    print "Error ==> ", form.errors


        else:
            form = UserFileForm()
            
    except Exception, e:
        print "Error is: %s" %str(e)

    params['form'] = form
    params['success'] = success
    params['file_name'] = file_name
    return render_to_response('top.html', params, context_instance=RequestContext(request))
