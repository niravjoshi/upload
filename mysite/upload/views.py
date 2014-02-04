from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt

from upload.forms import UploadFile

@csrf_exempt
def demo(request):
    print "<==== DATA ===>"
    print request.POST
    print "file", request.FILES
    print "===== DATA END ======"
    params = {}
    params['form'] = UploadFile()
    return render_to_response('top.html', params, context_instance=RequestContext(request))
