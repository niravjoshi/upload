# Python
import string, random

# Model
from upload.models import LinkValidate

# Email
from django.core.mail import send_mail, BadHeaderError, EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context

# Constants
from upload.constants import SUBJECT, MESSAGE, FROM, URL

# Send email to user for their email address verification.
def send_mail(user):
    try:
        link = create_link(user)
        text_body = get_template('email.txt')
        html_body = get_template('email.html')
        d = Context({'user': user.first_name, 'link': link})
        text_content = text_body.render(d)
        html_content = html_body.render(d)
        EMAIL_TO = [user.email]
        msg = EmailMultiAlternatives(SUBJECT, text_content, FROM, EMAIL_TO)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    except BadHeaderError:
        return HttpResponse('Invalid Header')
    except Exception, e:
        print "Email error: ", str(e)

# Create url link to be send to user. On clicking this link, user can validate their email address.
def create_link(user):
    try:
        _rand_str = rand_str()
        link = URL + user.first_name + user.last_name + "/" + _rand_str
        link_validate = LinkValidate.objects.create(user=user,rand_key=_rand_str)
        link_validate.save()
        print "link validate details saved"
    except Exception, e:
        print "Link creation error: ", str(e)
        link = None

    return link

# Create random string which is to be send as a part of url link for email verification.
def rand_str():
    try:
        _string = [random.choice(string.ascii_letters + string.digits) for n in xrange(48)]
        rand_str = "".join(_string)
        print "String: ", rand_str
    except Exception, e:
        print "Random string error: ", str(e)
        rand_str = None

    return rand_str

