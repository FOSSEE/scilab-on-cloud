#scilab on cloud database
DB_NAME_DEFAULT = 'scilab'
DB_USER_DEFAULT = 'root'
DB_PASS_DEFAULT = '325898'
DB_HOST_DEFAULT = ''
DB_PORT_DEFAULT = ''

#scilab.in database
DB_NAME_SCILAB = 'scilab'
DB_USER_SCILAB = 'root'
DB_PASS_SCILAB = '325898'
DB_HOST_SCILAB = ''
DB_PORT_SCILAB = ''

#BIN = '/usr/bin/sudo /Temp/Scilab.Bin'
#replace it with according to your path
BIN='/home/vidhan'
# SCILAB_FLAGS = '-noatomsautoload'
SCILAB_FLAGS = '-noatomsautoload -nogui -nb '
SCIMAX_LOADER = '/Sites/CLOUD/scilab/scilab-scimax-2.1.4/loader.sce' #optional
UPLOADS_PATH = '/home/vidhan/Desktop/scilab-on-cloud/uploads' #mandetory
SCILAB_3 = 'scilab-5.3.3'
SCILAB_4 = 'scilab-5.4.1'
SCILAB_5 = 'scilab-5.5.2'

# Host for sending e-mail.
EMAIL_HOST_SERVER = 'smtp server'

# Port for sending e-mail.
EMAIL_PORT_SERVER = 587

# Optional SMTP authentication information for EMAIL_HOST.
EMAIL_HOST_USER_SERVER = 'user'
EMAIL_HOST_PASSWORD_SERVER = 'password'
EMAIL_USE_TLS_SERVER = True

FROM_EMAIL = 'from'
TO_EMAIL = 'to'
CC_EMAIL = 'cc'
BCC_EMAIL = 'bcc'

# github
GITHUB_ACCESS_TOKEN = 'e443502efbd2e89916b0005bb404f192dce858ac'
GITHUB_ACCESS_TOKEN_SOCBOT = '3c0201b0efb748381de6166109dc51caea04edf0'

TEMP_USER = 'fosseeuser'
MAIN_USER = 'psinalkar1988'

# python social auth # replace it with according to your domain.
#SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/'
SOCIAL_AUTH_LOGIN_URL = '/'
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '316260991637-vd8ag9ffk11pne4cmso4nac0912ag22i.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'ULtTWWQy0BgnDgHFcV9qpTJp'
