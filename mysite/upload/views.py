from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt

from upload.forms import UploadFile
from upload.models import Ufile

def demo(request):
    params = {}
    success = False
    file_name = None
    try:
        if request.method == 'POST':
            form = UploadFile(request.POST, request.FILES)
            print "POST method"
            if form.is_valid():
                print "form is valid"
                form.save()
                success = True
                file_name = request.FILES['user_file']
                print "form saved"

            else:
                print "form is not valid"
                print "Error ==> ", form.errors

        else:
            form = UploadFile()
    except Exception, e:
        print "Error is: %s" %str(e)

    params['form'] = form
    params['success'] = success
    params['file_name'] = file_name
    return render_to_response('top.html', params, context_instance=RequestContext(request))
