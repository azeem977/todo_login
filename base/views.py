# from django.shortcuts import render
# from django.views.generic.list import  ListView
# from django.views.generic.detail import DetailView
# from django.views.generic.edit import  CreateView, UpdateView ,DeleteView , FormView
# from django.urls import reverse_lazy
# from django.contrib.auth.mixins import LoginRequiredMixin
# from .models import Task

# from django.contrib.auth.views import LoginView
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth import login


# # Create your views here.
  
# class TaskList(LoginRequiredMixin, ListView):
#     model = Task
#     context_object_name = 'tasks'

#     def get_queryset(self):
#         return Task.objects.filter(user=self.request.user)

# class TaskDetail(LoginRequiredMixin,DetailView):
#     model= Task
#     context_object_name = 'task'
#     template_name = 'base/task.html'


#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['count'] = context['tasks'].filter(complete=False).count()
#         return context

# class CustomLoginView(LoginView):
#     template_name = 'base/login.html'
#     fields = '__all__'
#     redirect_authenticated_user = True

#     def get_success_url(self):
#         return reverse_lazy('tasks') 


# class RegisterPage(FormView):
#      template_name = 'base/register.html'
#      form_class =UserCreationForm
#      redirect_authenticated_user = True
#      success_url = reverse_lazy('tasks')




# class TaskCreate(LoginRequiredMixin,CreateView): 
#         model = Task
#         fields = ['title','description','complete']
#         success_url = reverse_lazy('tasks')

#         def form_valid(self, form):
#              form.instance.user =self.request.user
#              return super(TaskCreate,self).form_valid(form)

# class TaskUpdate(LoginRequiredMixin,UpdateView):
#      model = Task
#      fields = ['title','description','complete']
#      success_url = reverse_lazy('tasks')


# class ModelDeleteView(LoginRequiredMixin,DeleteView):
#     model =  Task
#     context_object_name = 'task'
#     template_name = 'base/task_conform_delete.html' 
#     success_url = reverse_lazy('tasks')


from django.shortcuts import render ,redirect
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
)

from .models import Task


# ------------------------
# LOGIN VIEW
# ------------------------
class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')


# ------------------------
# REGISTER VIEW
# ------------------------
class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage,self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('task')
        return super(RegisterPage,self).get( *args, **kwargs  )

# ------------------------
# TASK LIST VIEW
# ------------------------
# class TaskList(LoginRequiredMixin, ListView):
#     model = Task
#     context_object_name = 'tasks'

#     def get_queryset(self):
#         return Task.objects.filter(user=self.request.user)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['count'] = context['tasks'].filter(complete=False).count()

#         search_input = self.request.GET.get('search-area') or ''
#         if search_input:
#             context ['tasks'] = context['tasks'].filter(title__icontains=search_input)

#         context['search_input'] = search_input    
#         return context


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'

    def get_queryset(self):
        search_input = self.request.GET.get('search-area') or ''
        queryset = Task.objects.filter(user=self.request.user)
        if search_input:
            queryset = queryset.filter(title__startswith=search_input)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count'] = self.get_queryset().filter(complete=False).count()
        context['search_input'] = self.request.GET.get('search-area') or ''
        return context




# ------------------------
# TASK DETAIL VIEW
# ------------------------
class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count'] = Task.objects.filter(user=self.request.user, complete=False).count()
        return context


# ------------------------
# CREATE TASK VIEW
# ------------------------
class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


# ------------------------
# UPDATE TASK VIEW
# ------------------------
class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')


# ------------------------
# DELETE TASK VIEW
# ------------------------
class ModelDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task_conform_delete.html'
    success_url = reverse_lazy('tasks')


