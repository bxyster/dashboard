from django.conf import settings

STAFF_ONLY = getattr(settings, 'STAFF_ONLY', False)

REPO_DIR = '/data/allrepo/{0}'
TEMPLATE_DIR = '/root/django_dashboard/dashboard_git/dashboard/gitdashboard/templates/gitdashboard/{0}'
