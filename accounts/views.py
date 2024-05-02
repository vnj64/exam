from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, FormView

from .forms import RegistrationForm, AddBalanceForm
from .models import Profile, Transaction


class RegistrationView(CreateView):
    form_class = RegistrationForm
    template_name = 'accounts/register.html'
    success_url = '/accounts/profile/'

    def form_valid(self, form):
        response = super().form_valid(form)
        Profile.objects.create(user=self.object)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(
            self.request,
            username=username,
            password=password
        )
        login(request=self.request, user=user)
        return response


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'

    statuses_reverse = {
        'bronze': 0,
        'silver': 1,
        'gold': 0,
    }

    statuses = {
        0: 0,
        1: 1000,
        2: 5000,
    }

    def get(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=request.user)
        transactions = Transaction.objects.filter(user=request.user).all()
        sum_transactions = sum([trans.transaction for trans in transactions])
        status_id = self.statuses_reverse[profile.status]
        status_next = self.statuses[status_id + 1] - sum_transactions
        return render(request, self.template_name, {'profile': profile,
                                                    'total_paid': sum_transactions,
                                                    'next_status': status_next if status_next > 0 else ''
                                                    })


class AddBalance(LoginRequiredMixin, FormView):
    template_name = 'accounts/add-balance.html'
    form_class = AddBalanceForm
    success_url = reverse_lazy('accounts:profile')

    def form_valid(self, form):
        response = super().form_valid(form)
        profile = Profile.objects.get(user=self.request.user)
        balance = form.cleaned_data.get('balance')
        profile.balance += balance
        profile.save()
        return response
