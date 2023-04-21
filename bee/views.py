from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Prefetch
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from bee.forms import RegisterForm
from bee.models import Action, Beehive, Queen, Reminder

User = get_user_model()
# Create your views here.


def index(request):
    num_hive = Beehive.objects.filter(is_active=True).count()
    num_queen = Queen.objects.filter(is_active=True).count()
    num_action = Action.objects.count()
    num_reminder = Reminder.objects.filter(is_active=True).count()

    return render(
        request,
        "index.html",
        context={
            'num_hive': num_hive,
            'num_queen': num_queen,
            'num_action': num_action,
            'num_reminder': num_reminder,
        }
    )

""" Beehive - Улий или ПС. Можно созать, редактировать, просмотреть"""


class BeehiveListView(generic.ListView):
    model = Beehive
    paginate_by = 10


class BeehiveDetailView(generic.DetailView):
    model = Beehive


class BeehiveCreate(LoginRequiredMixin, generic.CreateView):
    model = Beehive
    fields = ['number', 'row_num', 'type_hive', 'queen', 'title', 'text', 'volume', 'is_active']


class BeehiveUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Beehive
    fields = [
        'number',
        'row_num',
        'type_hive',
        'queen',
        'title',
        'text',
        'volume',
        'pub_date',
        'is_active'
    ]


""" Queen  - Матка. Можно создать, редактировать, просмотреть"""


class QueenListView(generic.ListView):
    model = Queen
    paginate_by = 10


class QueenDetailView(generic.DetailView):
    model = Queen


class QueenCreate(LoginRequiredMixin, generic.CreateView):
    model = Queen
    fields = ['year', 'title', 'is_active']


class QueenUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Queen
    fields = ['year', 'title', 'is_active']


""" Action - оперция с ПС. Можно создать, редактировать, просмотреть"""


class ActionListView(generic.ListView):
    model = Action
    paginate_by = 10


class ActionDetailView(generic.DetailView):
    model = Action


class ActionCreate(LoginRequiredMixin, generic.CreateView):
    model = Action
    fields = ['text', 'post_date']


class ActionUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Action
    fields = ['text', 'post_date']


""" Reminder - напоминание к будущему осмотру. Можно создать, редактировать, просмотреть"""


class ReminderListView(generic.ListView):
    model = Reminder
    paginate_by = 10


class ReminderDatailView(generic.DetailView):
    model = Reminder


class ReminderCreate(LoginRequiredMixin, generic.CreateView):
    model = Reminder
    fields = ['text', 'post-date', 'is_active']


class ReminderUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Reminder
    fields = ['text', 'post-date', 'is_active']


""" Работа с User-ом"""


class UserListView(generic.ListView):
    model = User
    template_name = 'bee/user_list.html'
    paginate_by = 10



class UserDetailView(generic.DetailView):
    template_name = 'bee/user_detail.html'
    model = User


class RegisterFormView(generic.FormView):
    template_name = "registration/register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("index")

    # def form_valid(self, form):
    #     user = form.save()
    #     user = authenticate(self.request, username=user.username, password=form.cleaned_data.get("password1"))
    #     login(self.request, user)
    #     return super(RegisterFormView, self).form_valid(form)


class UserProfile(LoginRequiredMixin, generic.DetailView):
    model = User
    template_name = "registration/profile.html"

    def get_object(self, queryset=None):
        user = self.request.user
        return user


class UpdateProfile(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = User
    fields = ["first_name", "last_name", "email"]
    template_name = "registration/update_profile.html"
    success_url = reverse_lazy("index")
    success_message = "Profile updated"

    def get_object(self, queryset=None):
        user = self.request.user
        return user

