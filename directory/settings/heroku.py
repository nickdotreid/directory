# Parse database configuration from $DATABASE_URL
import dj_database_url
DATABASES['default'] =  dj_database_url.config()

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

if 'DEBUG' in os.environ:
	DEBUG = True
	TEMPLATE_DEBUG = DEBUG
else:
	DEBUG = False
	TEMPLATE_DEBUG = DEBUG	

if 'SECRET_KEY' in os.environ:
	SECRET_KEY = os.environ['SECRET_KEY']

if False not in ( 'AWS_STATIC_URL', 'AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY', 'AWS_BUCKET_NAME' in os.environ ):
	
	STATIC_URL = os.environ['AWS_STATIC_URL']
	
	STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
	DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
	AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY']
	AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
	AWS_STORAGE_BUCKET_NAME = os.environ['AWS_BUCKET_NAME']
	
if 'GOOGLE_ANALYTICS_ID' in os.environ:
	GOOGLE_ANALYTICS_ID = os.environ['GOOGLE_ANALYTICS_ID']