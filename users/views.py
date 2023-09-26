from random import randint

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, ListView

from users.forms import UserRegisterForm, UserUpdateForm
from users.models import User


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        new_verification_key = ''.join([str(randint(0, 9)) for _ in range(20)])

        self.object = form.save()
        self.object.verification_key = new_verification_key
        self.object.is_active = False
        self.object.save()
        group = Group.objects.get(name='Пользователь')
        self.object.groups.add(group)

        site = 'http://127.0.0.1:8000'
        url = reverse_lazy('users:verify', kwargs={'verification_key': new_verification_key})

        send_mail(
            subject='Верификация пользователя',
            message=f'Подтвердить адрес почты: {site}{url}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.object]
        )

        return super().form_valid(form)


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    success_url = reverse_lazy('users:profile')
    form_class = UserUpdateForm

    def get_object(self, queryset=None):
        return self.request.user


class UserListView(PermissionRequiredMixin, ListView):
    model = User
    permission_required = 'users.view_user'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)

        queryset = queryset.exclude(is_staff=True)
        print(queryset)

        return queryset


def verification(request, verification_key):
    try:
        user = User.objects.filter(verification_key=verification_key).first()
        if user:
            user.is_active = True
            user.save()
            return render(request, 'users/confirm_success.html')
        else:
            return render(request, 'users/confirm_failed.html')
    except Exception:
        pass


def recovery_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            new_password = ''.join([str(randint(0, 9)) for _ in range(12)])
            send_mail(
                subject='Восстановление пароля',
                message=f'Ваш новый пароль: {new_password}',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email]
            )
            user.set_password(new_password)
            user.save()
            return redirect(reverse('users:login'))

        except Exception:
            pass

    return render(request, 'users/recovery_password.html')


def toggle_activity_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if user.is_active:
        user.is_active = False
    else:
        user.is_active = True

    user.save()

    return redirect(reverse('users:users_list'))
