from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from emailing.forms import EmailingForm, ClientForm, Text_MessagesForm
from emailing.models import Emailing, Client, Text_Messages


class Text_MessagesListView(ListView):
    model = Text_MessagesForm
    success_url = reverse_lazy('emailing:message_list')
    extra_context = {
        'title': 'Сообщения'
    }

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='manager').exists() or user.is_superuser:
            queryset = super().get_queryset()
        else:
            queryset = super().get_queryset().filter(
                emailing_owner=user.pk
            )
        return queryset


class Text_MessagesCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """Создание сообщения"""
    model = Text_Messages
    form_class = Text_MessagesForm
    extra_context = {
        'title': 'Добавление сообщения'
    }

    def test_func(self):
        user = self.request.user
        if not user.groups.filter(name='manager').exists() and not user.groups.filter(name='content_manager').exists():
            return True
        return False

    def get_success_url(self):
        return reverse('emailing:message_detail', args=[self.object.pk])

    def form_valid(self, form):
        user = self.request.user
        self.object = form.save()
        self.object.emailing_owner = user
        self.object.save()
        return redirect(self.get_success_url())

    def handle_no_permission(self):
        return redirect(reverse_lazy('emailing:message_list'))


class Text_MessagesUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Редактирование рассылки"""
    model = Text_Messages
    form_class = Text_MessagesForm
    extra_context = {
        'title': 'Редактирование сообщения'
    }

    def test_func(self):
        user = self.request.user
        message = self.get_object()

        if message.owner == user or user.groups.filter(name='manager').exists() or user.is_superuser:
            return True
        return False

    def handle_no_permission(self):
        return redirect(reverse_lazy('emailing:message_list'))

    def get_success_url(self):
        return reverse('emailing:message_detail', args=[self.object.pk])


class Text_MessagesDetailView(DetailView, UserPassesTestMixin):
    """Детали сообщения"""
    model = Text_Messages
    extra_context = {
        'title': 'Детали сообщения'
    }

    def test_func(self):
        user = self.request.user
        message = self.get_object()

        if message.owner == user or user.groups.filter(name='manager').exists() or user.is_superuser:
            return True
        return False

    def handle_no_permission(self):
        return redirect(reverse_lazy('emailing:message_list'))


class Text_MessagesDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Удаление сообщения"""
    model = Text_Messages
    success_url = reverse_lazy('emailing:message_list')
    extra_context = {
        'title': 'Удаление рассылки'
    }

    def test_func(self):
        user = self.request.user
        message = self.get_object()

        if message.owner == user or user.is_superuser:
            return True
        return False

    def handle_no_permission(self):
        return redirect(reverse_lazy('emailing:message_list'))


class EmailingListView(ListView):
    model = Emailing
    extra_context = {
        'title': 'Рассылки'
    }

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='manager').exists() or user.is_superuser:
            queryset = super().get_queryset()
        else:
            queryset = super().get_queryset().filter(
                emailing_owner=user.pk
            )
        return queryset


class EmailingCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """Создание рассылки"""
    model = Emailing
    form_class = EmailingForm
    extra_context = {
        'title': 'Добавление рассылки'
    }

    def test_func(self):
        user = self.request.user
        if not user.groups.filter(name='manager').exists() and not user.groups.filter(name='content_manager').exists():
            return True
        return False

    def get_success_url(self):
        return reverse('emailing:emailing_detail', args=[self.object.pk])

    def form_valid(self, form):
        user = self.request.user
        self.object = form.save()
        self.object.emailing_owner = user
        self.object.save()
        return redirect(self.get_success_url())

    def handle_no_permission(self):
        return redirect(reverse_lazy('emailing:emailing_list'))


class EmailingUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Редактирование рассылки"""
    model = Emailing
    form_class = EmailingForm
    extra_context = {
        'title': 'Редактирование рассылки'
    }

    def test_func(self):
        user = self.request.user
        emailing = self.get_object()

        if emailing.emailing_owner == user or user.groups.filter(name='manager').exists() or user.is_superuser:
            return True
        return False

    def handle_no_permission(self):
        return redirect(reverse_lazy('emailing:emailing_list'))

    def get_success_url(self):
        return reverse('emailing:emailing_detail', args=[self.object.pk])


class EmailingDetailView(DetailView, UserPassesTestMixin):
    """Детали рассылки"""
    model = Emailing
    extra_context = {
        'title': 'Детали рассылки'
    }

    def test_func(self):
        user = self.request.user
        emailing = self.get_object()

        if emailing.emailing_owner == user or user.groups.filter(name='manager').exists() or user.is_superuser:
            return True
        return False

    def handle_no_permission(self):
        return redirect(reverse_lazy('emailing:emailing_list'))


class EmailingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Удаление рассылки"""
    model = Emailing
    success_url = reverse_lazy('emailing:emailing_list')
    extra_context = {
        'title': 'Удаление рассылки'
    }

    def test_func(self):
        user = self.request.user
        emailing = self.get_object()

        if emailing.emailing_owner == user or user.is_superuser:
            return True
        return False

    def handle_no_permission(self):
        return redirect(reverse_lazy('emailing:emailing_list'))


class ClientListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Client
    extra_context = {
        'title': 'Мои клиенты'
    }

    def test_func(self):
        user = self.request.user
        if not user.is_staff or user.is_superuser:
            return True
        return False

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            queryset = super().get_queryset()
        else:
            queryset = super().get_queryset().filter(
                client_owner=user.pk
            )
        return queryset

    def handle_no_permission(self):
        return redirect(reverse_lazy('emailing:emailing_list'))


class ClientCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """Создание клиента"""
    model = Client
    form_class = ClientForm
    extra_context = {
        'title': 'Добавление клиента'
    }

    def test_func(self):
        user = self.request.user
        if not user.is_staff or user.is_superuser:
            return True
        return False

    def handle_no_permission(self):
        return redirect(reverse_lazy('emailing:emailing_list'))

    def get_success_url(self):
        return reverse('emailing:client_detail', args=[self.object.pk])

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.client_owner = self.request.user
        self.object.save()
        return redirect(self.get_success_url())


class ClientUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Редактирование клиента"""
    model = Client
    form_class = ClientForm
    extra_context = {
        'title': 'Редактирование клиента'
    }

    def test_func(self):
        user = self.request.user
        mailing = self.get_object()

        if mailing.client_owner == user or user.is_staff:
            return True
        return False

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.client_owner != self.request.user and not self.request.user.is_staff:
            raise Http404
        return self.object

    def handle_no_permission(self):
        return redirect(reverse_lazy('emailing:client_list'))

    def get_success_url(self):
        return reverse('emailing:client_detail', args=[self.object.pk])


class ClientDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """Детали клиента"""
    model = Client
    extra_context = {
        'title': 'Информация о клиенте'
    }

    def test_func(self):
        user = self.request.user
        if not user.is_staff or user.is_superuser:
            return True
        return False

    def handle_no_permission(self):
        return redirect(reverse_lazy('emailing:emailing_list'))


class ClientDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Удаление клиента"""
    model = Client
    success_url = reverse_lazy('emailing:client_list')
    extra_context = {
        'title': 'Удаление клиента'
    }

    def test_func(self):
        user = self.request.user
        if not user.is_staff or user.is_superuser:
            return True
        return False

    def handle_no_permission(self):
        return redirect(reverse_lazy('emailing:emailing_list'))
