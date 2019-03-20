import django
import os
from os import path
import sys
from builtins import str
from builtins import object
from django.db.models import Count
from django.core.mail import EmailMultiAlternatives

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "soc.settings")

base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_path)

django.setup()
from datetime import date, timedelta, datetime
from soc.config import (FROM_EMAIL, TO_EMAIL, CC_EMAIL, BCC_EMAIL, SITE)


class Cron(object):
    now = datetime.now()
    yesterday = date.today() - timedelta(1)
    log_file_name = yesterday.strftime("%Y-%m-%d")
    print(log_file_name)
    mail_attachment = base_path + '/static/log/' + log_file_name\
        + '.txt'

    def log_exist(mail_attachment):
        if os.path.isfile(mail_attachment):
            mail_body = """<b>Some errors are found on scilab on cloud in """\
                """TBC examples </b><br><br> Check for attachment"""
            sender_email = FROM_EMAIL
            mail_body += "Please do the needful.<br><br>"
            mail_body += """<center><h6>*** This is an automatically """ \
                """generated email, please do not reply***</h6>"""\
                """</center>"""
            subject = "[Scilab On Cloud] - Execution error log report " \
                + log_file_name

            email = EmailMultiAlternatives(
                subject, '',
                sender_email, [TO_EMAIL],
                bcc=[BCC_EMAIL],
                cc=[CC_EMAIL],
                headers={"Content-type": "text/html;charset=iso-8859-1"}
            )
            email.attach_alternative(mail_body, "text/html")
            email.attach_file(mail_attachment)
            email.content_subtype = 'html'  # Main content is text/html
            email.mixed_subtype = 'related'
            email.send(fail_silently=True)
        else:
            return None
    log_exist(mail_attachment)


Cron()
