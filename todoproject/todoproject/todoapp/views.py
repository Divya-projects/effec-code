from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .forms import TodoForm
from .models import Task
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView,DeleteView

class Tasklistview(ListView):
    model = Task
    template_name = 'add.html'
    context_object_name = 'tasks'

class Taskdetailview(DetailView):
    model = Task
    template_name = 'details.html'
    context_object_name = 'taskdetail'

class Taskupdateview(UpdateView):
    model = Task
    template_name = 'edit.html'
    context_object_name = 'task'
    fields = ('name','priority','date')

    def get_success_url(self):
        #return reverse_lazy('cbvdetail',kwargs={'pk':self.object.id})
        return reverse_lazy('cbvhome')

class Taskdeleteview(DeleteView):
    model = Task
    template_name = 'delete.html'
    # context_object_name = 'task'
    success_url = reverse_lazy('add')


# Create your views here.
def add(request):
    tasks = Task.objects.all()
    if request.method == 'POST':
        name = request.POST.get('task','')
        priority = request.POST.get('prior','')
        date = request.POST.get('date','')
        task = Task(name=name,priority=priority,date=date)
        task.save()

    return render(request,'add.html',{'tasks': tasks})

# def details(request):
#     tasks = Task.objects.all()
#     return render(request,'details.html',{'tasks': tasks})

def delete(request,taskid):
    task=Task.objects.get(id=taskid)
    if request.method == 'POST':
        task.delete()
        return redirect('/')
    return render(request,'delete.html')

def update(request,id):
    task=Task.objects.get(id=id)
    f=TodoForm(request.POST or None, instance=task)
    if f.is_valid():
        f.save()
        return redirect('/')
    return render(request,'edit.html',{'f':f,'task':task})

