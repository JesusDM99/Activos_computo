from django import forms
from django.forms.widgets import DateInput
from django_select2.forms import Select2MultipleWidget
from .models import *
from django.db.models import Q


class SeleccionForm(forms.Form):
    usuario = forms.ModelChoiceField(queryset=Usuario.objects.all(), label='Usuario')
    
class ActaForm(forms.ModelForm):
    class Meta:
        model = Acta
        fields = '__all__' 
        
        
class ActivoForm(forms.ModelForm):
    class Meta:
        model = Activo
        fields = '__all__'
        widgets = {
            'garantia': forms.DateInput(attrs={'type': 'date'}),
            'fecha_compra': forms.DateInput(attrs={'type': 'date'}),
        }
 

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = '__all__' 

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = '__all__' 

class LicenciaForm(forms.ModelForm):
    class Meta:
        model = Licencia
        fields = '__all__' 
         
        widgets = {
            'fecha_compra': forms.DateInput(attrs={'type': 'date'}),
            'fecha_vigencia': forms.DateInput(attrs={'type': 'date'}),
            'estado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class Tipos_LicenciaForm(forms.ModelForm):
    class Meta:
        model = Tipos_Licencia
        fields = '__all__'

class Tipos_ActivosForm(forms.ModelForm):
    class Meta:
        model = Tipos_Activos
        fields = '__all__'

class CiudadForm(forms.ModelForm):
    class Meta:
        model = Ciudad
        fields = '__all__'            
            
class UbicacionForm(forms.ModelForm):
    class Meta:
        model = Ubicacion
        fields = '__all__'   

class DireccionForm(forms.ModelForm):
    class Meta:
        model = Direccion
        fields = '__all__'   

class AreaForm(forms.ModelForm):
    class Meta:
        model = Area      
        fields = '__all__'   

class EstadoForm(forms.ModelForm):
    class Meta:
        model = Estado
        fields = '__all__'
    
class MarcaForm(forms.ModelForm):
    class Meta:
        model = Marca
        fields = '__all__'

class CargoForm(forms.ModelForm):
    class Meta:
        model = Cargo
        fields = '__all__'   
    
class CondicionForm(forms.ModelForm):
    class Meta:
        model = Condicion
        fields = '__all__'