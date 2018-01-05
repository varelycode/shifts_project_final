from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import UpdateView, ListView, DetailView
from django.views.generic.edit import FormMixin
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse
import pdb
from .forms import ShiftForm, RunForm, EmployeeForm
from .models import Run, GroupShift, Shift


class GroupShiftListView(ListView):
    model = GroupShift
    context_object_name = 'groupshifts'
    template_name = 'home.html'


class GroupDetailView(DetailView):
    model = GroupShift
    context_object_name = 'groupshift'
    template_name = "shiftgroups/group_detail.html"


# class ShiftListView(ListView):
#     model = Shift
#     context_object_name = 'shifts'
#     template_name = 'shifts/list_shifts.html'
#     paginate_by = 20

#     def get_context_data(self, **kwargs):
#         kwargs['groupshift'] = self.groupshift
#         return super().get_context_data(**kwargs)

#     def get_queryset(self):
#         self.groupshift = get_object_or_404(GroupShift, pk=self.kwargs.get('pk'))
#         queryset = self.groupshift.shifts.order_by('-last_updated').annotate(replies=Count('runs') - 1)
#         return queryset


class ShiftDetailView(DetailView):
    model = Shift
    context_object_name = 'shift'
    template_name = 'shifts/shift_detail.html'
    pk_url_kwarg = "shift_pk"


class ShiftListView(FormMixin, ListView):
    model = Shift
    context_object_name = "shifts"
    template_name = "all_shifts.html"
    form_class = EmployeeForm

    def get_context_data(self, **kwargs):
        context = super(ShiftListView, self).get_context_data(**kwargs)

        if self.request.method == "POST":
            employee = kwargs['form'].cleaned_data['employee']
            context['shifts'] = Shift.objects.filter(user=employee)

        return context


@login_required
def create_shift_view(request, pk):
    groupshift = get_object_or_404(GroupShift, pk=pk)
    if request.method == 'POST':
        form = ShiftForm(request.POST)
        if form.is_valid():
            shift = form.save(commit=False)
            shift.groupshift = groupshift
            shift.starter = request.user
            shift.save()

            success_url = reverse("shifts:group_detail", kwargs={"pk": groupshift.pk})
            return redirect(success_url)
    else:
        form = ShiftForm()
    return render(request, 'shifts/create_shift.html', {'groupshift': groupshift, 'form': form})


@login_required
def create_run_view(request, pk, shift_pk):
    shift = get_object_or_404(Shift, groupshift__pk=pk, pk=shift_pk)
    if request.method == 'POST':
        form = RunForm(request.POST, shift=shift)
        if form.is_valid():
            run = form.save(commit=False)
            run.shift = shift
            run.created_by = request.user

            employees = form.cleaned_data['employess']
            if employees:
                for emp in employees:
                    run.users.add(emp)
            run.save()
            shift.last_updated = timezone.now()
            shift.save()

            success_url = reverse('shifts:shift_detail', kwargs={'pk': pk, 'shift_pk': shift_pk})

            return redirect(success_url)
    else:
        form = RunForm()
    return render(request, 'runs/create_run.html', {'shift': shift, 'form': form})


'''@login_required
def add_shift(request, pk, run_pk):
    run = get_object_or_404(Run, shift__pk=pk, pk=run_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            run.users = request.user
            run.save()

        topic_url = reverse('topic_posts', kwargs={'pk': pk, 'shift_pk': shift_pk})
        topic_post_url = '{url}?page={page}#{id}'.format(
                url=topic_url,
                id=run.pk,
                page=shift.get_page_count()
            )
        return redirect(topic_post_url)
    else:
       form = PostForm()
    return(request, 'reply_topic.html', {'shift': shift, 'form' : form})  '''





# @method_decorator(login_required, name='dispatch')
# class PostUpdateView(UpdateView):
#     model = Run
#     fields = ('message', )
#     template_name = 'edit_post.html'
#     pk_url_kwarg = 'run_pk'
#     context_object_name = 'run'

#     def get_queryset(self):
#         queryset = super().get_queryset()
#         return queryset.filter(created_by=self.request.user)

#     def form_valid(self, form):
#         run = form.save(commit=False)
#         run.updated_by = self.request.user
#         run.updated_at = timezone.now()
#         run.save()
#         return redirect('topic_posts', pk=run.shift.groupshift.pk, shift_pk=run.shift.pk)
