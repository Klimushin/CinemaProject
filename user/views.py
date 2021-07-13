from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, ListView

from cinema.models import Ticket
from user.forms import SignUpForm
from user.models import Customer


class UserSignUpView(CreateView):
    model = Customer
    form_class = SignUpForm
    template_name = "registration/sign-up.html"
    success_url = reverse_lazy('user:login')


class UserLoginView(LoginView):
    template_name = 'registration/login.html'
    success_url = reverse_lazy('cinema:today')

    def form_valid(self, form):
        self.request.session['last_touch'] = str(timezone.now())
        return super().form_valid(form=form)


class UserPurchaseListView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('user:login')
    template_name = 'cinema/purchases.html'
    model = Ticket

    def get_queryset(self):
        return super().get_queryset().filter(customer=self.request.user)
