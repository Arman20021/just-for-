from django.urls import path
from tasks.views import manager_dashboard,user_dashboard,test,create_task,view_task,update_task,delete_task,event_manage,task_detail
urlpatterns = [
     path('manager-dashboard/',manager_dashboard,name='manager-dashboard'),
     path('user-dashboard/',user_dashboard),
     path('test/',test),
     path('create-task/',create_task,name='create-task'),
     path('view_task/',view_task),
     path('update_task/<int:id>/',update_task,name='update-task'),
     path('delete_task/<int:id>/',delete_task,name='delete-task'),
     path('event_manage/',event_manage,name='event_manage'),
     path('task/<int:id>/', task_detail, name='task-detail'),



]
