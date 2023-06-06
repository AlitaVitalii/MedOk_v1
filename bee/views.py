from itertools import chain
from operator import attrgetter

from django.core.paginator import Paginator
from environ import environ

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.db.models import Prefetch, Q, Avg, Count, Sum, Max, Min
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic

from bee.forms import RegisterForm
from bee.models import Action, Beehive, Queen, Reminder, Row, Work, Honey

User = get_user_model()
env = environ.Env()

# Create your views here.


def index(request):
    num_hive = Beehive.objects.filter(is_active=True).count()
    num_queen = Queen.objects.filter(is_active=True).count()
    num_action = Action.objects.count()
    num_reminder = Reminder.objects.filter(is_active=True).count()
    aggr_honey = Honey.objects.aggregate(
        Count('quantity'),
        Sum('quantity'),
        Avg('quantity'),
        Max('quantity'),
        Min('quantity'),
    )

    return render(
        request,
        "index.html",
        context={
            'num_hive': num_hive,
            'num_queen': num_queen,
            'num_action': num_action,
            'num_reminder': num_reminder,
            'avg_honey': round(aggr_honey['quantity__avg'], 2),
            'count_honey': aggr_honey['quantity__count'],
            'sum_honey': aggr_honey['quantity__sum'],
            'max_honey': aggr_honey['quantity__max'],
            'min_honey': aggr_honey['quantity__min'],
        }
    )


""" Beehive - Улий или ПС. Можно созать, редактировать, просмотреть"""


class BeehiveListView(generic.ListView):
    model = Beehive
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Beehive.objects.select_related('row', 'queen', ).filter(is_active=True).filter(
                Q(number__icontains=query) | Q(title__icontains=query)
            ).order_by('number')
        else:
            return Beehive.objects.select_related('row', 'queen').filter(is_active=True).order_by('number')


class BeehiveDetailView(generic.DetailView):
    model = Beehive
    template_name = 'bee/beehive_detail.html'
    # context_object_name = 'beehive'
    paginate_by = 10

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #
    #     actions = Action.objects.filter(beehive=self.object)
    #     works = Work.objects.filter(beehive=self.object)
    #
    #     # Объединяем события Action и Work
    #     events = sorted(chain(actions, works), key=attrgetter('post_date'), reverse=True)
    #
    #     context['events'] = events
    #     return context.

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # подсчитываем сумму отобраных рамок
        beehive = self.get_object()
        total_quantity = beehive.honey_set.aggregate(total=Sum('quantity')).get('total')
        context['total_quantity'] = total_quantity

        # beehive = self.get_object()
        actions = Action.objects.filter(beehive=self.get_object())
        works = Work.objects.filter(beehive=self.get_object())

        # Объединяем события из actions и works
        events = sorted(
            list(actions) + list(works),
            key=lambda event: event.post_date,
            reverse=True
        )

        paginator = Paginator(events, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['events'] = page_obj
        return context

    queryset = Beehive.objects.prefetch_related(
        Prefetch('reminder_set', queryset=Reminder.objects.filter(is_active=True)),
    )


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
    queryset = Action.objects.select_related('beehive').order_by('-post_date')


class ActionDetailView(generic.DetailView):
    model = Action


class ActionCreate(LoginRequiredMixin, generic.CreateView):
    model = Action
    fields = ['text', 'post_date']

    def form_valid(self, form):
        # добавляем связь с Beehive
        form.instance.beehive = get_object_or_404(Beehive, pk=self.kwargs['pk'])
        send_mail(
            f"Действие к ПС №{form.instance.beehive}",
            f" Улей: {form.instance.beehive.number}. \nДействие: {form.cleaned_data.get('text')}",
            env('EMAIL'),
            [env('EMAIL2')],
            fail_silently=False,
        )
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
    queryset = Reminder.objects.prefetch_related('beehive').order_by('-is_active')


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
        # после создания возращаемяс на связанный beehive
        return reverse('beehive_detail', kwargs={'pk': self.kwargs['pk'], })


class ReminderCreat(LoginRequiredMixin, generic.CreateView):
    #  для создания напоминалия в журнале
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


"""Дабота с количеством отобраных рамок медовых"""


class HoneyListView(generic.ListView):
    model = Honey
    paginate_by = 10


class HoneyDetailView(generic.DetailView):
    model = Honey


class HoneyCreate(LoginRequiredMixin, generic.CreateView):
    model = Honey
    fields = ['quantity', 'post_date']

    def form_valid(self, form):
        # добавляем связь с Beehive
        form.instance.beehive = get_object_or_404(Beehive, pk=self.kwargs['pk'])
        return super(HoneyCreate, self).form_valid(form)

    def get_success_url(self):
        # после создания возращаемяс на связанный beehive
        return reverse('beehive_detail', kwargs={'pk': self.kwargs['pk'], })



class HoneyUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Honey
    fields = ['beehive', 'quantity', 'post_date']


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

