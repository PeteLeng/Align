from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView,
)

from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

from .forms import NewUserForm, ProjectForm, ActionForm
from .models import Project, Action, File


# Create your views here.
def user_signup(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Signup successful!")
            return redirect(f'../home')
    form = NewUserForm()
    context = {
        'signup_form': form,
        }
    return render(request, 'core/user_signup.html', context)


def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            fdata = form.cleaned_data
            username = fdata.get('username')
            password = fdata.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Logged in as {username}")
                return redirect(f'../home')
            else:
                messages.error(request, "Invaids username or password")
        messages.error(request, "Invaids username or password")
    form = AuthenticationForm()
    context = {
        'login_form': form,
        }
    return render(request, 'core/user_login.html', context)


class HomeView(View):
    template_name = 'core/home_list.html'

    def get(self, request, *args, **kwargs):
        print("Home View\n================")
        print(request.GET)
        user = request.user
        proj_set = user.project_set.all()
        print(proj_set)
        context = {
            'user': user,
            'proj_set': proj_set,
            }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template_name, context)


class ProjectView(View):
    template_name = 'core/proj_detail.html'

    def get(self, request, *args, **kwargs):
        print("Project View\n================")
        print(request.GET)
        user = request.user
        proj_form = ProjectForm()
        context = {
            'user': user,
            'proj_form': proj_form,
            }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')


class ActionView(View):
    template_name = 'core/act_detail.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        act_form = ActionForm()
        context = {
            'user': user,
            'act_form': act_form,
            }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = ActionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')


class ProjectListView(View):
    template_name = 'core/proj_list.html'
    
    def get(self, request, *args, **kwargs):
        user = request.user
        proj_set = user.project_set.all()
        open_proj_set = user.project_set.all().filter(status=True)
        # print(open_act_set)
        closed_proj_set = user.project_set.all().filter(status=False)
        context = {
            'user': user,
            'proj_set': proj_set,
            'open_proj_set': open_proj_set,
            'closed_proj_set' : closed_proj_set,
            }
        return render(request, self.template_name, context)


class ActionListView(View):
    template_name = 'core/act_list.html'
    
    def get(self, request, *arg, **kwargs):
        user = request.user
        open_act_set = Action.objects.filter(user=user).filter(status=True)
        closed_act_set = Action.objects.filter(user=user).filter(status=False)
        context = {
            'user': user,
            'open_act_set': open_act_set,
            'closed_act_set': closed_act_set,
            }
        return render(request, self.template_name, context)


class FileListView(View): 
    template_name = 'core/file_list.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        context = {
            'user': user
            }
        return render(request, self.template_name, context)


class ProjectCreateView(CreateView):
    form_class = ProjectForm
    template_name = 'core/proj_new.html'
    success_url = reverse_lazy('home')


class ProjectUpdateView(UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'core/proj_update.html'
    success_url = reverse_lazy('home')


class ProjectDeleteView(DeleteView):
    model = Project
    template_name = 'core/proj_delete.html'
    success_url = reverse_lazy('home')


class ActionCreateView(CreateView):
    form_class = ActionForm
    template_name = 'core/act_new.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        action = form.save(commit=False)
        action.user = self.request.user
        action.save()
        form.save_m2m()
        return redirect('home')


class ActionUpdateView(UpdateView):
    model = Action
    form_class = ActionForm
    template_name = 'core/act_update.html'
    success_url = reverse_lazy('home')


class ActionDeleteView(DeleteView):
    model = Action
    template_name = 'core/act_delete.html'
    success_url = reverse_lazy('home')

