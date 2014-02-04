from django.shortcuts import render_to_response
from django.template import RequestContext

from upload.forms import UploadFile

def demo(request):
    print "<==== DATA ===>"
    print request.POST
    print "===== DATA END ======"
    return render_to_response('top.html', {}, context_instance=RequestContext(request))
