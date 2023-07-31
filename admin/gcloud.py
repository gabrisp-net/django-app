# "core/gcsUtils.py"
import datetime
from storages.backends.gcloud import GoogleCloudStorage

today = datetime.date.today()

year = today.year

Static = lambda: GoogleCloudStorage(location='static')
Media = lambda: GoogleCloudStorage(location='media')