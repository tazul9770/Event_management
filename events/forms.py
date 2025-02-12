
from django import forms
from events.models import Event, Category

class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()
        
    default_classes = "border border-gray-500 w-full rounded-lg shadow-sm focus:border-rose-500 focus:ring-rose-500"

    def apply_styled_widgets(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput) or isinstance(field.widget, forms.EmailInput):
                field.widget.attrs.update({
                    'class': self.default_classes,
                    'placeholder': f"Enter {field.label.lower()}"
                })
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'class': self.default_classes,
                    'placeholder': f"Enter {field.label.lower()}",
                    'rows': 5
                })
            elif isinstance(field.widget, forms.DateInput) or isinstance(field.widget, forms.TimeInput):
                field.widget.attrs.update({
                    'class': "border border-gray-500 rounded-lg shadow-sm focus:border-rose-500 focus:ring-rose-500",
                    'type': field.widget.input_type
                })
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                    'class': "space-y-2"
                })

# class EventForm(StyleFormMixin, forms.ModelForm):
#     class Meta:
#         model = Event
#         fields = ['name', 'description', 'date', 'time', 'location', 'category', 'participants', 'asset']
#         widgets = {
#             'date': forms.DateInput(attrs={'type': 'date'}),
#             'time': forms.TimeInput(attrs={'type': 'time'}),
#             'participants': forms.CheckboxSelectMultiple()
#         }

#     def save(self, commit=True):
#         event = super().save(commit=False)
#         if commit:
#             event.save()
#             self.save_m2m() 
#         return event

class EventForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'date', 'time', 'location', 'category', 'participants', 'image']  # Added 'asset'
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'participants': forms.CheckboxSelectMultiple()
        }

    def save(self, commit=True):
        event = super().save(commit=False)
        if commit:
            event.save()
            self.save_m2m() 
        return event





