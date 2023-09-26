import random

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, DetailView

from blogs.models import Blog
from mailings.forms import MailingForm, ClientForm
from mailings.models import Mailing, Client, MailingLog
from mailings.services import create_task_mailing, delete_task_mailing, set_active_user, get_caches_object
from users.models import User


class IndexView(TemplateView):
    template_name = 'mailings/index.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        context_data['title'] = 'Сервис управления рассылками'

        mailings_total = Mailing.objects.all()
        mailings_active = Mailing.objects.exclude(status='Завершена')
        clients = Client.objects.all()
        uniq_clients = set(clients)

        blogs = Blog.objects.all()
        pk_blogs = [i.pk for i in blogs]
        random.shuffle(pk_blogs)
        blogs = [Blog.objects.get(pk=i) for i in pk_blogs[:3]]

        print(blogs)

        context_data['mailings_total'] = len(mailings_total)
        context_data['mailings_active'] = len(mailings_active)
        context_data['uniq_clients'] = len(uniq_clients)
        context_data['blogs_list'] = blogs

        return context_data


class MailingListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Mailing
    permission_required = 'mailings.view_mailing'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)

        if not self.request.user.is_staff:
            queryset = queryset.filter(owner=self.request.user)

        return queryset

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        set_active_user(self.request.user)

        context_data['title'] = 'Все рассылки'
        return context_data


class LogsListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = MailingLog
    permission_required = 'mailings.view_mailinglog'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(
            mailing_id=self.kwargs.get('pk')
        )

        return queryset

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)

        mailing = Mailing.objects.get(pk=self.kwargs.get('pk'))
        log_status = 'Успешно' if mailing.status else 'Не успешно'
        clients = ', '.join([str(i) for i in mailing.clients.all()])

        context_data['title'] = f'Логи рассылки - {mailing}'
        context_data['message'] = mailing.message_boby
        context_data['log_status'] = log_status
        context_data['clients'] = clients

        return context_data


class ClientListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Client
    permission_required = 'mailings.view_client'

    extra_context = {
        'title': 'Все клиенты'
    }

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)

        if not self.request.user.is_staff:
            queryset = queryset.filter(owner=self.request.user)
        return queryset


class MailingCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailings:mailings_list')
    permission_required = 'mailings.add_mailing'

    extra_context = {
        'title': 'Создание рассылки'
    }

    def form_valid(self, form):
        created_object = form.save()
        create_task_mailing(created_object)

        created_object.owner = self.request.user
        created_object.save()
        return super().form_valid(form)


class ClientCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailings:clients_list')
    permission_required = 'mailings.add_client'

    extra_context = {
        'title': 'Создание клиента'
    }

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailings:mailings_list')
    permission_required = 'mailings.change_mailing'

    extra_context = {
        'title': 'Изменение рассылки'
    }

    def form_valid(self, form):
        changed_object = form.save()

        create_task_mailing(changed_object)
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailings:clients_list')
    permission_required = 'mailings.change_client'

    extra_context = {
        'title': 'Изменение клиента'
    }


class MailingDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailings:mailings_list')
    permission_required = 'mailings.delete_mailing'

    extra_context = {
        'title': 'Удаление рассылки'
    }

    def form_valid(self, form):
        print(self.object.pk)
        delete_task_mailing(self.object.pk)
        return super().form_valid(form)


class ClientDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('mailings:clients_list')
    permission_required = 'mailings.delete_client'

    extra_context = {
        'title': 'Удаление клиента'
    }


class MailingDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Mailing
    permission_required = 'mailings.view_mailing'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        context_data['title'] = 'Просмотр рассылки'
        context_data['object'] = get_caches_object(self.object.pk)

        return context_data


@login_required
def toggle_activity(request, pk):
    mailing = Mailing.objects.get(pk=pk)
    if mailing.status != 'Завершена':
        delete_task_mailing(pk)
        mailing.status = 'Завершена'
        mailing.save()
    else:
        create_task_mailing(mailing)
    return redirect(reverse('mailings:mailing_detail', args=[pk]))
