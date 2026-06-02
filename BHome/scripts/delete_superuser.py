import os
import sys
import django

# Ensure project root is on sys.path so Django settings module can be imported
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BHome.settings')
django.setup()

from django.contrib.auth.models import User

username = 'admin'
user = User.objects.filter(username=username).first()
if user:
    uid = user.id
    user.delete()
    print('deleted', uid)
else:
    print('not found')
