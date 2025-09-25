from django import forms
from django.forms import inlineformset_factory
from .models import Cliente, Direccion
from django.forms.models import BaseInlineFormSet
from django.core.exceptions import ValidationError
from .models import ImportacionLog


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = [
            'tipo_entidad',
            'nombre_razon_social',
            'rut',
            'email',
            'telefono',
            'sitio_web',
            'activo',
            'observacion',
            'agente',
        ]
        widgets = {
            'tipo_entidad':        forms.Select(attrs={'class': 'form-select'}),
            'nombre_razon_social': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'rut':                 forms.TextInput(attrs={'class': 'form-control'}),
            'email':               forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono':            forms.TextInput(attrs={'class': 'form-control'}),
            'sitio_web':           forms.URLInput(attrs={'class': 'form-control'}),
            'activo':              forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'observacion':         forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'agente':              forms.Select(attrs={'class': 'form-select', 'required': True}),
        }

def clean_agente(self):
    agente = self.cleaned_data.get('agente')
    if not agente:
        raise forms.ValidationError("Debes seleccionar un agente.")
    return agente


class DireccionForm(forms.ModelForm):
    class Meta:
        model = Direccion
        exclude = ('cliente',)
        widgets = {
            'tipo':             forms.Select(attrs={'class': 'form-select', 'required': True}),
            'calle':            forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'numero':           forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'comuna':           forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'ciudad':           forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'codigo_postal':    forms.TextInput(attrs={'class': 'form-control'}),
            'pais':             forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'observacion':      forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

class BaseDireccionFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()

        tiene_direccion = False
        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                if form.cleaned_data.get('calle') and form.cleaned_data.get('comuna'):
                    tiene_direccion = True
                    break

        if not tiene_direccion:
            raise ValidationError("Debes ingresar al menos una dirección con calle y comuna.")
        
DireccionFormSet = inlineformset_factory(
    Cliente,
    Direccion,
    form=DireccionForm,
    formset=BaseDireccionFormSet,
    extra=1,
    can_delete=True
)


class ImportacionForm(forms.ModelForm):
    class Meta:
        model = ImportacionLog
        fields = ['archivo']
        widgets = {
            'archivo': forms.ClearableFileInput(attrs={'accept': '.xlsx'}),
        }
