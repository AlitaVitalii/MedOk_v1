from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Prefetch, Q
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic

from bee.forms import RegisterForm
from bee.models import Action, Beehive, Queen, Reminder, Row, Work

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
    # prefetch_actions = Prefetch('action_set', queryset=Action.objects.only('post_date'))
    # queryset = Beehive.objects.select_related('row', 'queen').filter(is_active=True)
        # .prefetch_related('action_set')
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Beehive.objects.select_related('row', 'queen').filter(is_active=True).filter(
                Q(number__icontains=query) | Q(title__icontains=query)
            )
        else:
            return Beehive.objects.select_related('row', 'queen').filter(is_active=True)

class BeehiveDetailView(generic.DetailView):
    model = Beehive


class BeehiveCreate(LoginRequiredMixin, generic.CreateView):
    model = Beehive
    fields = ['number', 'row', 'type_hive', 'queen', 'title', 'text', 'volume', 'is_active']


class BeehiveUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Beehive
    fields = [
        'number',
        'row',
        'type_hive',
        'queen',
        'title',
        'text',
        'volume',
        'pub_date',
        'is_active'
    ]
    # queryset = Beehive.objects.filter(is_active=True)


""" Queen  - Матка. Можно создать, редактировать, просмотреть"""


class QueenListView(generic.ListView):
    model = Queen
    paginate_by = 10

    queryset = Queen.objects.prefetch_related(
        Prefetch('beehive_set', queryset=Beehive.objects.filter(is_active=True))).filter(is_active=True)


class QueenDetailView(generic.DetailView):
    model = Queen
    # queryset = Queen.objects.prefetch_related('beehive_set')


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
    date_hierarchy = ['post_date']
    queryset = Action.objects.select_related('beehive')


class ActionDetailView(generic.DetailView):
    model = Action


class ActionCreate(LoginRequiredMixin, generic.CreateView):
    model = Action
    fields = ['text', 'post_date']

    def form_valid(self, form):
        # добавляем связь с Beehive
        form.instance.beehive = get_object_or_404(Beehive, pk=self.kwargs['pk'])
        return super(ActionCreate, self).form_valid(form)

    def get_success_url(self):
        # после создания возращаемяс на связанный блог
        return reverse('beehive_detail', kwargs={'pk': self.kwargs['pk'], })


class ActionUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Action
    fields = ['beehive', 'text', 'post_date']


""" Reminder - напоминание к будущему осмотру. Можно создать, редактировать, просмотреть"""


class ReminderListView(generic.ListView):
    model = Reminder
    paginate_by = 10
    queryset = Reminder.objects.prefetch_related('beehive')


class ReminderDetailView(generic.DetailView):
    model = Reminder


class ReminderCreate(LoginRequiredMixin, generic.CreateView):
    model = Reminder
    fields = ['text', 'post_date', 'is_active']

    def form_valid(self, form):
        # добавляем связь с Beehive
        form.instance.beehive = get_object_or_404(Beehive, pk=self.kwargs['pk'])
        return super(ReminderCreate, self).form_valid(form)

    def get_success_url(self):
        # после создания возращаемяс на связанный блог
        return reverse('beehive_detail', kwargs={'pk': self.kwargs['pk'], })


class ReminderCreat(LoginRequiredMixin, generic.CreateView):
    model = Reminder
    fields = ['beehive', 'text', 'post_date', 'is_active']

    # def get_success_url(self):
    #     # после создания возращаемяс на связанный блог
    #     return reverse('reminder_list')


class ReminderUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Reminder
    fields = ['beehive', 'text', 'post_date', 'is_active']


""" Ряр. Можно создать, редактировать, просмотреть"""


class RowListView(generic.ListView):
    model = Row
    paginate_by = 10
    queryset = Row.objects.prefetch_related(
        Prefetch('beehive_set', queryset=Beehive.objects.filter(is_active=True))
    )


class RowDetailView(generic.DetailView):
    model = Row


class RowCreate(LoginRequiredMixin, generic.CreateView):
    model = Row
    fields = ['name']


class RowUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Row
    fields = ['name']


""" Работа с групповыми действиями"""


class WorkListView(generic.ListView):
    model = Work
    paginate_by = 10
    queryset = Work.objects.order_by('-post_date')


class WorkDetailView(generic.DetailView):
    model = Work


class WorkCreate(LoginRequiredMixin, generic.CreateView):
    model = Work
    fields = ['text', 'beehive', 'post_date']


class WorkUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Work
    fields = ['text', 'beehive', 'post_date']


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

