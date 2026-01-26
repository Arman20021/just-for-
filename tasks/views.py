from django.shortcuts import render,redirect
from django.http import HttpResponse
from tasks.forms import TaskForm,TaskModelForm,TaskDetailModelForm    
from tasks.models import *
from datetime import date
from django.db.models import Q,Count,Min,Max,Avg
from django.contrib import messages
# Create your views here.
def manager_dashboard(request):
    type_filter = request.GET.get('type', 'all')
    query = request.GET.get('q', '').strip()  # search text

    # Status counts
    counts = Task.objects.aggregate(
        total=Count('id'),
        completed=Count('id', filter=Q(status="COMPLETED")),
        in_progress=Count('id', filter=Q(status="IN_PROGRESS")),
        pending=Count('id', filter=Q(status="PENDING"))
    )

    # Base query
    tasks = Task.objects.select_related('details').prefetch_related('assigned_to')

    # Apply status filter
    if type_filter == 'completed':
        tasks = tasks.filter(status='COMPLETED')
    elif type_filter == 'in-progress':
        tasks = tasks.filter(status='IN_PROGRESS')
    elif type_filter == 'pending':
        tasks = tasks.filter(status='PENDING')

    # Apply search filter only on title
    if query:
        tasks = tasks.filter(title__icontains=query)

    context = {
        'tasks': tasks,
        'counts': counts,
        'query': query,
        'type': type_filter,
    }

    return render(request, "dashboard/manager-dashboard.html", context)

def user_dashboard(request):
    return render (request,"dashboard/user_dashboard.html")

def test(request):
    context={
        "names":["Arman","Islam","Durjoy"],
        "age":23
    }
    return render(request,'test.html',context)
   
def create_task(request): 
    # employees=Employee.objects.all()
    task_form=TaskModelForm()
    task_detail_form=TaskDetailModelForm()


    if request.method == "POST":
        task_form=TaskModelForm(request.POST)
        task_detail_form=TaskDetailModelForm(request.POST)
        if task_form.is_valid() and task_detail_form.is_valid():

            #for django model form data
            task=task_form.save()
            task_detail=task_detail_form.save(commit=False)
            task_detail.task=task
            task_detail.save()
            messages.success(request,"Task Created Successfully")





            return redirect ('manager-dashboard')


           


            """For Django Form Data"""
        #     data=form.cleaned_data
        #     title=data.get('title')
        #     description=data.get('description')
        #     due_date=data.get('due_date')
        #     assigned_to=data.get('assigned_to')


        #     task=Task.objects.create(title=title,description=description,due_date=due_date)
        #    #assign employee task
        #     for emp_id in assigned_to:
        #        employee=Employee.objects.get(id=emp_id)
        #        task.assigned_to.add(employee)
            
            # return HttpResponse("Task Added Succesfully")

    context={"task_form":task_form,'task_detail_form':task_detail_form}
    return render (request,"dashboard/task_form.html",context)

def view_task(request):
    #SHOW THE TASK ARE COMPLETED
    # tasks=Task.objects.filter(status="COMPLETED")

    #SHOW THE TASK WHICH DUE DATE IS TODAY
    # tasks=Task.objects.filter(due_date=date.today())
    '''Show the task which priority is not low'''
    # tasks=TaskDetail.objects.exclude(priority='L')

    """Show the task that contains c and status is pending"""
    # tasks=TaskDetail.objects.filter(title__icontains='c',status='PENDING')

    '''Show the task which are pending or in progress'''
    # tasks=Task.objects.filter(Q(status='PENDING')|Q(status='IN_PROGRESS'))

    # tasks=Task.objects.select_related('details').all()

    task_count=Task.objects.aggregate(num_task=Count('id'))
  

    return render (request,"show_task.html",{"task_count":task_count})


def update_task(request,id): 
    task=Task.objects.get(id=id)
    task_form=TaskModelForm(instance=task)
    if task.details:
        task_detail_form=TaskDetailModelForm(instance=task.details)


    if request.method == "POST":
        task_form=TaskModelForm(request.POST,instance=task)
        task_detail_form=TaskDetailModelForm(request.POST,instance=task.details)
        if task_form.is_valid() and task_detail_form.is_valid():
             
            task=task_form.save()
            task_detail=task_detail_form.save(commit=False)
            task_detail.task=task
            task_detail.save()
            messages.success(request,"Task Updated Successfully")
            return redirect ('update-task',id)

    context={"task_form":task_form,'task_detail_form':task_detail_form}
    return render (request,"dashboard/task_form.html",context)

def delete_task(request,id):
    if request.method == 'POST':
        task=Task.objects.get(id=id)
        task.delete()
        messages.success(request,"Task is Deleted")
        return redirect('manager-dashboard')
    else:
       messages.error(request,"Something went wrong")
       return redirect ('manager-dashboard')


def event_manage(request):
    return render (request,"dashboard/event_manage.html" )

 

def dashboard(request):
    return render(request, 'dashboard/dashboard.html')


def task_detail(request, id):
    task = Task.objects.get(id=id)
    return render(request, 'dashboard/task_detail.html', {'task': task})
