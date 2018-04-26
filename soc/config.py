DB_NAME_DEFAULT = 'scilab_on_cloud_defaultpy3'
DB_USER_DEFAULT = 'root'
DB_PASS_DEFAULT = 'root'
DB_HOST_DEFAULT = ''
DB_PORT_DEFAULT = ''

DB_NAME_SCILAB = 'scilab'
DB_USER_SCILAB = 'root'
DB_PASS_SCILAB = 'root'
DB_HOST_SCILAB = ''
DB_PORT_SCILAB = ''

#SCILAB_BIN = '/home/prashant/scilab_version/scilab-5.4.1/bin/scilab-adv-cli'
#SCILAB_FLAGS = '-noatomsautoload'
# SCILAB_FLAGS = '-noatomsautoload -nogui -nb ' #srikant
#SCIMAX_LOADER = '/home/scilab_test/CLOUD/scilab/scilab-scimax-2.1.4/loader.sce'
#UPLOADS_PATH = '/var/www/html/fossee-sites/scilab_in_2015/uploads'

BIN = '/home/prashant/scilab_version'
#SCILAB_FLAGS = '-noatomsautoload'
SCILAB_FLAGS = '-noatomsautoload -nogui -nb '
SCIMAX_LOADER = '/home/scilab_test/CLOUD/scilab/scilab-scimax-2.1.4/loader.sce'
UPLOADS_PATH = '/var/www/html/fossee-sites/scilab_uploads/uploads'
SCILAB_3 = 'scilab-5.3.3'
SCILAB_4 = 'scilab-5.4.1'
SCILAB_5 = 'scilab-5.5.2'

# Host for sending e-mail.
EMAIL_HOST_SERVER = 'smtp.gmail.com'

# Port for sending e-mail.
EMAIL_PORT_SERVER = 587

# Optional SMTP authentication information for EMAIL_HOST.
EMAIL_HOST_USER_SERVER = 'psin1988@gmail.com'
EMAIL_HOST_PASSWORD_SERVER = 'Mtemp@1988?'
EMAIL_USE_TLS_SERVER = True

FROM_EMAIL = 'prashant@fossee.in'
TO_EMAIL = 'prashantsinalkar@gmail.com'
CC_EMAIL = 'psin1988@gmail.com'
BCC_EMAIL = 'essarmax21@gmail.com'

GITHUB_ACCESS_TOKEN = '2706c4bad278c031f98e1b43e42244dc22ad73ab'
GITHUB_ACCESS_TOKEN_SOCBOT = 'e52410891d9bcf728ed4e8755ee44faff00d34a6'

TEMP_USER = 'fosseeuser'
MAIN_USER = 'psinalkar1988'

# python social auth
#SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/'
SOCIAL_AUTH_LOGIN_URL = '/'
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '316260991637-vd8ag9ffk11pne4cmso4nac0912ag22i.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'ULtTWWQy0BgnDgHFcV9qpTJp'

SITE = 'http://cloud.scilab.in'
