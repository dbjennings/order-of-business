import environ
from django.urls import reverse_lazy

# Build paths inside the project like this: BASE_DIR / 'subdir'.
ROOT_DIR = environ.Path(__file__) - 3
BASE_DIR = ROOT_DIR.path('apps')

# Customized Authentication Constants
AUTH_USER_MODEL = 'core.coreuser'
LOGIN_URL = '/login'
LOGIN_REDIRECT_URL = reverse_lazy('landing')
LOGOUT_REDIRECT_URL = '/'
HOME_URL = '/home'

# Initialize and read in the environment
ENV = environ.Env()

if ENV.bool('DJANGO_READ_ENV_FILE', default=True):
    ENV.read_env(env_file=f'{ROOT_DIR}\.env')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ENV('DJANGO_SECRET_KEY', 
                 default="nw@=#2$x6h#fca7)*l#l99@(ve=%!0ou1(t$l2z-8&&60ll5pu")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = ENV.bool('DJANGO_DEBUG', default=False)

ALLOWED_HOSTS = []


# Application definitions separated by source

DJANGO_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

THIRD_PARTY_APPS = (

)

LOCAL_APPS = (
    'apps.core.apps.CoreConfig',
    'apps.oob.apps.OobConfig',
)

# Installed apps as a sum of its parts
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [str(ROOT_DIR.path('templates'))],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': str(ROOT_DIR.path('db.sqlite3')),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = str(ROOT_DIR.path('staticfiles'))

STATICFILES_DIRS = (
    str(ROOT_DIR.path('static').path('app')),
    str(ROOT_DIR.path('static').path('css')),
    str(ROOT_DIR.path('static').path('js')),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)