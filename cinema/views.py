from django.views.generic import CreateView, ListView, UpdateView
from cinema.forms import (CreateSessionForm, FilterForm, TicketForm)
from django.utils import timezone
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib import messages
from datetime import timedelta
from django.contrib.auth.mixins import LoginRequiredMixin
from cinema.mixins import AdminRequiredMixin
from django.db.models import Sum

from cinema.models import Session, Hall, Ticket


class SessionListView(ListView):
    model = Session
    template_name = 'cinema/today.html'
    context_object_name = 'sessions'
    extra_context = {'quantity': TicketForm}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['filter'] = FilterForm
        return context

    def get_queryset(self):
        if self.request.user.is_authenticated:
            price = self.request.GET.get('filter_price')
            start_time = self.request.GET.get('filter_start_time')
            if price and start_time:
                return Session.objects.filter(
                    status=True,
                    end_date__gte=timezone.now().date(),
                    start_date__lte=timezone.now().date()).order_by('price', 'start_time').annotate(
                    total=Sum('session_tickets__quantity'))
            elif price:
                return Session.objects.filter(
                    status=True,
                    end_date__gte=timezone.now().date(),
                    start_date__lte=timezone.now().date()).order_by('price').annotate(
                    total=Sum('session_tickets__quantity'))
            elif start_time:
                return Session.objects.filter(
                    status=True,
                    end_date__gte=timezone.now().date(),
                    start_date__lte=timezone.now().date()).order_by('start_time').annotate(
                    total=Sum('session_tickets__quantity'))
        return Session.objects.filter(
            status=True,
            end_date__gte=timezone.now().date(),
            start_date__lte=timezone.now().date()).annotate(total=Sum('session_tickets__quantity'))


class TomorrowSessionListView(ListView):
    model = Session
    template_name = 'cinema/tomorrow.html'
    context_object_name = 'sessions'
    extra_context = {'quantity': TicketForm}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['filter'] = FilterForm
        return context

    def get_queryset(self):
        if self.request.user.is_authenticated:
            price = self.request.GET.get('filter_price')
            start_time = self.request.GET.get('filter_start_time')
            if price and start_time:
                return Session.objects.filter(
                    status=True,
                    end_date__gte=timezone.now().date() + timedelta(days=1),
                    start_date__lte=timezone.now().date() + timedelta(days=1)).order_by('price', 'start_time').annotate(
                    total=Sum('session_tickets__quantity'))
            elif price:
                return Session.objects.filter(status=True,
                                              end_date__gte=timezone.now().date() + timedelta(days=1),
                                              start_date__lte=timezone.now().date() + timedelta(days=1)).order_by(
                    'price').annotate(total=Sum('session_tickets__quantity'))
            elif start_time:
                return Session.objects.filter(
                    status=True,
                    end_date__gte=timezone.now().date() + timedelta(days=1),
                    start_date__lte=timezone.now().date() + timedelta(days=1)).order_by('start_time').annotate(
                    total=Sum('session_tickets__quantity'))
        return Session.objects.filter(
            status=True,
            end_date__gte=timezone.now().date() + timedelta(days=1),
            start_date__lte=timezone.now().date() + timedelta(days=1)).annotate(total=Sum('session_tickets__quantity'))


class CreateHallView(AdminRequiredMixin, CreateView):
    model = Hall
    fields = '__all__'
    success_url = reverse_lazy('cinema:today')


class UpdateHallView(AdminRequiredMixin, UpdateView):
    model = Hall
    success_url = reverse_lazy('cinema:today')
    fields = '__all__'
    template_name = 'cinema/update_hall.html'

    def validation(self):
        sessions = self.get_object().sessions.filter(status=True)
        if sessions:
            for session in sessions:
                if session.session_tickets.exists():
                    return False
        return True


class CreateSessionView(AdminRequiredMixin, CreateView):
    model = Session
    form_class = CreateSessionForm
    success_url = reverse_lazy('cinema:today')


class UpdateSessionView(AdminRequiredMixin, UpdateView):
    model = Session
    fields = ('hall', 'start_time', 'end_time', 'start_date', 'end_date', 'price')
    success_url = reverse_lazy('cinema:today')

    def validation(self):
        session = self.get_object()
        if session.session_tickets.exists():
            return False
        return True


class CreateTicketView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('user:login')
    model = Ticket
    form_class = TicketForm
    success_url = reverse_lazy('cinema:today')
    template_name = 'cinema/today.html'

    def form_valid(self, form):
        ticket = form.save(commit=False)
        quantity = int(form.data['quantity'])
        user = self.request.user
        ticket.customer = user
        session = Session.objects.get(id=self.request.POST['session'])
        ticket.session = session
        hall = session.hall
        total_quantity = session.session_tickets.aggregate(Sum('quantity'))['quantity__sum']
        if not total_quantity:
            total_quantity = 0
        free_places = hall.size - total_quantity
        if free_places < quantity:
            messages.error(self.request, f'Мест не хватает! Свободных мест: {free_places}')
            return HttpResponseRedirect(self.success_url)
        user.balance += quantity * session.price
        user.save()
        return super().form_valid(form=form)
