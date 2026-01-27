from django import forms
from tasks.models import Task,TaskDetail

#django form basic
class TaskForm(forms.Form):
    title = forms.CharField(max_length=250, label="Task Title")
    description = forms.CharField(widget=forms.Textarea, label="Task Description")
    due_date=forms.DateField(widget=forms.SelectDateWidget,label="Due Date")
    assigned_to=forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=[],label="Assigned To")
    def __init__(self,*args, **kwargs):
        
        employees=kwargs.pop("employees",[])
       
        super().__init__(*args,**kwargs)
        # print(self.fields)
        self.fields['assigned_to'].choices=[(emp.id,emp.name) for emp in employees]


class StyledFormMixin:
    """Mixin to apply to form field"""
    default_classes="border-2 border-gray-300  w-full rounded-lg shadow-sm focus:border-red-500 focus:ring-rose-500"

    def apply_styled_widgets(self):
        for field_name,field in self.fields.items():
             if isinstance(field.widget,forms.TextInput ):
                 field.widget.attrs.update ({
                     'class':self.default_classes,
                     'placeholder':f"Enter {field.label.lower()}"
                 })
             elif isinstance(field.widget,forms.Textarea):
                 field.widget.attrs.update({
                     'class':self.default_classes,
                     'placeholder':f"Enter {field.label.lower()}"
                 })    
             elif isinstance(field.widget,forms.SelectDateWidget):
                 field.widget.attrs.update({
                     'class':"border-2 border-gray-300  rounded-lg shadow-sm focus:border-red-500 focus:ring-rose-500 "
                 })
             elif isinstance(field.widget,forms.CheckboxSelectMultiple ):
                 field.widget.attrs.update({
                     'class':"space-y-2"
                 })
             elif isinstance(field.widget, forms.ClearableFileInput):
                   field.widget.attrs.update({
                  'class': self.default_classes
    })
    
             else :
                 print("Inside else")
                 field.widget.attrs.update({
                     'class':self.default_classes
                     
                 })    
                     
                     





#django model form
class TaskModelForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            'title',
            'description',
            'due_date',
            'assigned_to',
            'status',    
            'image',     
        ]
        widgets = {
            'due_date': forms.SelectDateWidget,
            'assigned_to': forms.CheckboxSelectMultiple,
            'status': forms.Select,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()


        '''Manual Widget'''
        # widgets={
        #     'title':forms.TextInput(attrs={
        #          'class':"border-2 border-gray-300  w-full rounded-lg shadow-sm focus:border-red-500 focus:ring-rose-500",
        #           'placeholder':"Enter Task Title"
        #     }),
        #     'description':forms.Textarea(attrs={
        #          'class':"border-2 border-gray-300  w-full rounded-lg shadow-sm focus:border-red-500 focus:ring-rose-500",
        #           'placeholder':"Describe The Task"
        #     }),
        #     'due_date': forms.SelectDateWidget(attrs={
        #          'class':"border-2 border-gray-300    rounded-lg shadow-sm focus:border-red-500 focus:ring-rose-500",
            
        #     }),
        #     'assigned_to':forms.CheckboxSelectMultiple(attrs={
        #         'class':"space-y-2"
        #     })

        # }
        
#widget using mixin 
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.apply_styled_widgets()


class TaskDetailModelForm(StyledFormMixin,forms.ModelForm):
    class  Meta:
        model=TaskDetail
        fields=['notes']

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.apply_styled_widgets()    

