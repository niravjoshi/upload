from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt

from upload.forms import UploadFile
from upload.models import Ufile

@csrf_exempt
def demo(request):
    params = {}
    try:
        if request.method == 'POST':
            form = UploadFile(request.POST, request.FILES)
            print "POST method"
            if form.is_valid():
                print "form is valid"
                form.save()
                print "form saved"

            else:
                print "form is not valid"
                print "Error ==> ", form.errors

        else:
            form = UploadFile()
    except Exception, e:
        print "Error is: %s" %str(e)

    params['form'] = form
    return render_to_response('top.html', params, context_instance=RequestContext(request))
