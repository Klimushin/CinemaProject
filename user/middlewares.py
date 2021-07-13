from django.contrib.auth import logout
from django.utils.deprecation import MiddlewareMixin
from datetime import timedelta, datetime
from django.utils import timezone
from kino.settings import AUTO_LOGOUT_TIME_MINUTES


class AutoLogOutMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if 'last_touch' in request.session:
            date = datetime.strptime(request.session['last_touch'], '%Y-%m-%d %H:%M:%S.%f')
            if not request.user.is_superuser and (date + timedelta(minutes=AUTO_LOGOUT_TIME_MINUTES)) < timezone.now():
                logout(request)
            else:
                request.session['last_touch'] = str(datetime.now())
