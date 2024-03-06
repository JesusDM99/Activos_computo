from django.db.models import Count , Q
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.db import IntegrityError
from django.contrib import messages


import json
import os

#PDF
import PyPDF2

# REPORLAB
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics


from io import BytesIO

# Fechas
from django.utils import timezone
from datetime import datetime, date
import locale 
locale.setlocale(locale.LC_ALL, 'es_ES.utf-8')
from django.shortcuts import get_object_or_404

from .models import *
from .forms import *

# LOGIN
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


@login_required 
def activos(request):
    
    # Obtener los tipos de activos y ordenarlos por el campo nombre
    tipos_activos_list = Tipos_Activos.objects.all().order_by('nombre')
    # se optiene el id del tipo seleccionado que viene desde el html
    tipo_id = int(request.POST.get("tipo_id", tipos_activos_list.first().id if tipos_activos_list else 0))
    
    
    # Obtener los tipos de usuarios y ordenarlos por el campo nombre
    user_activos_list = Usuario.objects.all().order_by('nombre')
    # se optiene el id del tipo seleccionado que viene desde el html
    user_id = int(request.POST.get("user_id", user_activos_list.first().id if user_activos_list else 0))

    activos = Activo.objects.all()
        
        
    if 'search_tipo' in request.POST:
        if tipo_id:
            activos = activos.filter(tipos_activos__exact=tipo_id)

    elif 'search_user' in request.POST:
        if user_id:
            activos = activos.filter(usuario__exact=user_id)

    # estado de la garantía para cada activo
    for activo in activos:
        hoy = timezone.now().date()
        garantia = activo.garantia
        if not isinstance(garantia, date):
            
            try:
                garantia = timezone.make_aware(garantia).date()
            except Exception as e:
                garantia = None
        if garantia:
            garantia_expirada = garantia < hoy
            activo.garantia_expirada = garantia_expirada
        else:
            # Indica que no se puede determinar la garantía si garantia es None
            activo.garantia_expirada = None
    
    if 'eliminar_registro' in request.POST:
        # Obtener el ID del registro a eliminar
        registro_id = request.POST.get('registro_id')
        
        # Buscar y eliminar el registro
        try:
            activo = Activo.objects.get(pk=registro_id)
            activo.delete()
            return JsonResponse({'success': True})
        except Activo.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Registro no encontrado'})

    context = {
        'activos':activos,
        'tipos': tipos_activos_list,             
        'tipo_id' : tipo_id,
        'user': user_activos_list,             
        'user_id' : user_id,
    }
    return render(request, 'activos/indexactivos.html', context)


@login_required 
def crear_activos(request):
    # Si se recibe un formulario POST, lo inicializamos con esos datos, de lo contrario, crea un formulario vacío.
    formulario = ActivoForm(request.POST or None, request.FILES or None)
    
    if request.method == 'POST' and formulario.is_valid():
            #Guardar Formulario
            formulario.save()
            # Redirigir a la página de activos 
            return redirect('activos')
    else:
        formulario = ActivoForm()
        return render(request, 'activos/crear.html', {'formulario': formulario})
    
@login_required
def editar_activos(request, id):
    activo_editar = Activo.objects.get(id=id)
    formulario = ActivoForm(request.POST or None, request.FILES or None, instance=activo_editar)

    if request.method == 'POST' and formulario.is_valid(): 
        # Guarda el activo actualizado
        activo_editar = formulario.save()

        usuario_seleccionada = formulario.cleaned_data.get('usuario')
        # Obtén la lista de IDs de licencias seleccionadas desde el formulario
        licencias_ids = request.POST.getlist('licencia') 
        # Asocia las licencias seleccionadas con el activo
        activo_editar.licencia.set(licencias_ids) 

        return redirect('activos')
        
    return render(request, 'activos/editar.html', {'formulario': formulario})


@login_required
def licencias(request):

    # Obtener los tipos de licencias y ordenarlos por el campo nombre
    tipos_licencias_list = Tipos_Licencia.objects.all().order_by('nombre')
    
    # se optiene el id del tipo seleccionado que viene desde el html
    tipo_id = int(request.POST.get("tipo_id",tipos_licencias_list.first().id if tipos_licencias_list else 0 ))
    
    if request.POST.get("tipo_id"):
        # si por medio del metodo post se selecciona un tipo
        licencias = Licencia.objects.filter(tipos_licencia__exact=tipo_id)
    else:  
        licencias = Licencia.objects.all()

 # estado de la vigencia para cada licencia
    for licencia in licencias:
        hoy = timezone.now().date()
        fecha_vigencia = licencia.fecha_vigencia

        if not isinstance(fecha_vigencia, date):
            
            try:            
                fecha_vigencia = timezone.make_aware(fecha_vigencia).date()
            except Exception as e:
                fecha_vigencia= None
                
        if fecha_vigencia:
            fecha_vigencia_expirada = fecha_vigencia < hoy
            licencia.fecha_vigencia_expirada = fecha_vigencia_expirada
        else:
                # Indica que no se puede determinar la fecha de la vigencia si la fecha vigencia es None
            licencia.fecha_vigencia = None
            
    if 'eliminar_registro' in request.POST:
        # Obtener el ID del registro a eliminar
        registro_id = request.POST.get('registro_id')
        
        # Buscar y eliminar el registro
        try:
            licencia = Licencia.objects.get(pk=registro_id)
            # Verificar si existen activos relacionados con la licencia
            if licencia.activos_licencia.exists():
                return JsonResponse({'success': False, 'error': 'No se puede eliminar la licencia porque está relacionada con al menos un activo.'})
            
            licencia.delete()
            return JsonResponse({'success': True})
        except Licencia.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Registro no encontrado'})

    context = {
        'licencias':licencias,
        'tipos': tipos_licencias_list,
        'tipo_id' : tipo_id,
    }
    return render(request, 'licencias/indexlicencias.html',context)

@login_required
def crear_licencias(request):
    formulario = LicenciaForm(request.POST or None, request.FILES or None )
    if request.method == 'POST' and formulario.is_valid():
        formulario.save()
        return redirect('licencias')
    else:
        formulario = LicenciaForm()
    return render(request, 'licencias/crear.html',{'formulario': formulario})

@login_required
def editar_licencias(request, id):
    licenciaeditar = Licencia.objects.get(id=id)
    formulario = LicenciaForm(request.POST or None, request.FILES or None, instance=licenciaeditar)
   
    if formulario.is_valid() and request.POST:
        
        licencia = formulario.save(commit=False)
        licencia.save()
        return redirect('licencias')
    return render(request, 'licencias/editar.html',{'formulario':formulario})

@login_required
def usuarios(request):
        
    # Obtener las areas y ordenar por el campo nombre
    area_list = Area.objects.all().order_by('nombre')
    
    # se optiene el id del area seleccionada que viene desde el html
    area_id = int(request.POST.get("area_id",area_list.first().id if area_list else 0 ))
    
    if request.POST.get("area_id"):
        # si por medio del metodo post se selecciona un tipo
        usuarios = Usuario.objects.filter(area__exact=area_id)
    else:  
        usuarios = Usuario.objects.all()
    
    if 'eliminar_registro' in request.POST:
        # Obtener el ID del registro a eliminar
        registro_id = request.POST.get('registro_id')
        
        # Buscar y eliminar el registro
        try:
            usuario = Usuario.objects.get(pk=registro_id)
            usuario.delete()
            return JsonResponse({'success': True})
        except Licencia.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Registro no encontrado'})
        
    context = {
        'usuarios':usuarios,
        'area': area_list,
        'area_id' : area_id,
    }
    return render(request, 'usuarios/indexusuarios.html',context)
@login_required
def crear_usuarios(request):
    formulario = UsuarioForm(request.POST or None, request.FILES or None )
    if request.method == 'POST' and formulario.is_valid(): 
        formulario.save()
        return redirect('usuarios')      
    else:
        formulario = UsuarioForm()          
    return render(request, 'usuarios/crear.html',{'formulario': formulario})
@login_required
def editar_usuarios(request, id):
    usuarioeditar = Usuario.objects.get(id=id)
    formulario = UsuarioForm(request.POST or None, request.FILES or None, instance=usuarioeditar)
    if request.method == 'POST' and formulario.is_valid():
        formulario.save() 
        return redirect('usuarios')
    return render(request, 'usuarios/editar.html',{'formulario':formulario})
@login_required
def eliminar_usuarios(request, id):
    usuarioEliminar = Usuario.objects.get(id=id)
    usuarioEliminar.delete()
    return redirect('usuarios')

def wrap_text(text, font_name, font_size, max_width):
    pdfmetrics.registerFont(pdfmetrics.getFont(font_name))

    lines = []
    current_line = []
    current_width = 0

    for word in text.split():
        width = pdfmetrics.stringWidth(' '.join(current_line + [word]), font_name, font_size)

        if current_width + width <= max_width:
            current_line.append(word)
            current_width += width
        else:
            lines.append(' '.join(current_line))
            current_line = [word]
            current_width = width

    lines.append(' '.join(current_line))
    return lines

@login_required 
def  generar_actas(request):  
     
    formulario2 = ActaForm()
    form = SeleccionForm()        
    
    if request.method == 'POST' :
    
        form = SeleccionForm(request.POST)
        form2 = ActaForm(request.POST, request.FILES)

        if 'generar_pdf' in request.POST and form.is_valid():
            usuario_seleccionado = form.cleaned_data['usuario']
            activos_relaconados = Activo.objects.filter(usuario__exact=usuario_seleccionado)
            
            # Crear un objeto BytesIO para almacenar el contenido del PDF
            buffer = BytesIO() 
            
            # Crear el objeto Canvas
            p = canvas.Canvas(buffer) 
            p.setFont("Helvetica", 11)
            
            # Obtener la fecha actual de creación del PDF
            fecha_creacion = datetime.now().strftime('%d de %B de %Y')

            encabezado_inst = Encabezado.objects.first()

            if encabezado_inst and encabezado_inst.imagen:
                imagen_path = encabezado_inst.imagen.path
                p.drawImage(imagen_path, 50, 720, width=500, height=90)
            else:
                default_imagen_path = 'static/img/encabezado.png'
                p.drawImage(default_imagen_path, 50, 720, width=500, height=90)


            # Establecer márgenes para el texto
            margen_izquierdo = 80
            y_position= 690  
            ancho_maximo = 1800
        
            # Agregar el encabezado
            p.drawString(margen_izquierdo, y_position, f'Medellín, {fecha_creacion}')
            y_position -= 20
            p.drawString(margen_izquierdo, y_position, f'Señor(a)')
            y_position-= 25
            p.drawString(margen_izquierdo, y_position, f'{usuario_seleccionado.nombre}  C.C {usuario_seleccionado.cedula}')

            # Agregar el cuerpo del documento
            y_position -= 20
            p.drawString(margen_izquierdo, y_position, 'A continuación le estamos haciendo entrega de los siguientes activos, los cuales estaran')
            y_position -= 15
            p.drawString(margen_izquierdo, y_position, 'bajo su completa responsabilidad y custodia.')
            y_position -= 20

            
            # Agregar la lista de activos
            for activo in activos_relaconados:
                
                texto_activo = f'- {activo.tipos_activos} {activo.marca}  S/N {activo.serial} {activo.tic} Eventos: {activo.evento}'
                lines = wrap_text(texto_activo, "Helvetica", 11 , ancho_maximo)

                for line in lines:
                    p.drawString(margen_izquierdo +30, y_position - 35, line)
                    y_position -= 15

            p.setFont("Helvetica-Bold", 10 )
            p.drawString(80, 580, 'DETALLES')
            
            
            
            p.setFont("Helvetica", 8)
            p.setFillColor(colors.blue)
            p.drawString(margen_izquierdo, y_position -150, 'OBSERVACIONES:')
            
            # Agregar las observaciones 
            p.setFont("Helvetica", 10)
            p.setFillColor(colors.black)
            
            observaciones = [
                '• Vigilar con frecuencia que no le falte el activo o lo tenga en mal estado, ya que usted',
                '  es la única persona responsable.',
                '• Si observa que le quitan o le cambian su activo, informe de inmediato a su jefe para que se',
                '  hagan los cargos y descargos correspondientes y la anotación del estado del mismo.',
                '• Si considera que su activo requiere algún mantenimiento para colocarlo en mejores ',
                '  condiciones, informe a su jefe.',
                '• En el momento de su desvinculación de la empresa es indespensable la presentación de un',
                '  paz y salvo expedido por su jefe, quien temporalmente asumirá la responsabilidad del ',
                '  mismo hasta entregarlos al nuevo empleado.',
                '• Si al momento de la devolución del activo este presenta deterioro por manipulación  como ',
                '  partes rotas, quebradas u otro tipo de avería, el empleado debe asumir el valor de los',
                '  repuestos o reparación',
                '• Exija una copia de la carta donde lo responsabilizan de su activo, para que este al tanto ',
                '  su contenido.',
                '• Fuera del Laboratorio Maria Salome, lo que suceda con el equipo es completamente ',
                '  responsabilidad. En caso de daño o perdida usted deberá asumir el costo de reparacion',
                '  o reposición.'
                
                # ... (otras observaciones)
            ]

            for observacion in observaciones:
                y_position -= 15
                p.drawString(margen_izquierdo +10, y_position - 150, observacion)
                
            # Agregar la firma y cargo
            y_position = 70
            p.drawString(margen_izquierdo, y_position, 'Diana Marcela Quiroz')
            y_position = 57 
            p.drawString(margen_izquierdo, y_position, 'Coordinadora Administrativa')
            
            
            p.drawString(margen_izquierdo +250, y_position +13, f'{usuario_seleccionado.nombre}')
            
            p.drawString(margen_izquierdo +250, y_position, f'{usuario_seleccionado.cargo} - {usuario_seleccionado.area}')
                    
            p.showPage()
            p.save()
            buffer.seek(0)
            
            # Generar el PDF
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="documento.pdf"'
            response.write(buffer.getvalue())
            buffer.close()

            return response
        
        elif 'cargar_archivo' in request.POST and form2.is_valid():
            # Si es válido, se guarda el formulario y se asocia con el usuario seleccionado
            usuario_seleccionado = form2.cleaned_data['usuario']
            acta = form2.save(commit=False)
            acta.usuario = usuario_seleccionado
            acta.save()
                
            # Redirigir a la vista deseada (reemplaza con el nombre real de tu vista)
            return redirect('actas')
        
        elif 'eliminar_registro' in request.POST:
            # Obtener el ID del registro a eliminar
            registro_id = request.POST.get('registro_id')
            
            # Buscar y eliminar el registro
            try:
                acta = Acta.objects.get(pk=registro_id)
                acta.delete()
                return JsonResponse({'success': True})
            except Acta.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Registro no encontrado'})

    # Obtener todas las Actas para mostrar en la tabla
    actas = Acta.objects.all()
    
    context = {
        'form': form,
        'formulario2': formulario2, 
        'actas': actas,
    }
    return render(request, 'actas/indexacta.html',context)

@login_required 
#ventanas emergentes
def crear_ciudades(request):
    if request.method == 'POST':
        form = CiudadForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'listas/crear_ciudades.html', {'form': form, 'ciudades_guardado': True})
    else:
        form = CiudadForm()
    return render(request, 'listas/crear_ciudades.html', {'form': form})

@login_required 
def crear_tipos_activos(request):
    if request.method == 'POST':
        form = Tipos_ActivosForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'listas/crear_tipos.html', {'form': form, 'tipos_guardado': True})
    else:
        form = Tipos_ActivosForm()
    return render(request, 'listas/crear_tipos.html', {'form': form})

@login_required 
def crear_ubicacion(request):
    if request.method == 'POST':
        form = UbicacionForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'listas/crear_ubicacion.html', {'form': form, 'ubicacion_guardado': True})
    else:
        form = UbicacionForm()
    return render(request, 'listas/crear_ubicacion.html', {'form': form})

@login_required 
def crear_direccion(request):
    if request.method == 'POST':
        form = DireccionForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'listas/crear_direccion.html', {'form': form, 'direccion_guardado': True})
    else:
        form = DireccionForm()
    return render(request, 'listas/crear_direccion.html', {'form': form})

@login_required 
def crear_area(request):
    if request.method == 'POST':
        form = AreaForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'listas/crear_area.html', {'form': form, 'area_guardado': True})
    else:
        form = AreaForm()
    return render(request, 'listas/crear_area.html', {'form': form})

@login_required 
def crear_cargo(request):
    if request.method == 'POST':
        form = CargoForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'listas/crear_cargo.html', {'form': form, 'cargo_guardado': True})
    else:
        form = CargoForm()
    return render(request, 'listas/crear_cargo.html', {'form': form})

@login_required 
def crear_proveedor(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'listas/crear_proveedor.html', {'form': form, 'proveedor_guardado': True})
    else:
        form = ProveedorForm()
    return render(request, 'listas/crear_proveedor.html', {'form': form})

@login_required 
#logout
def exit (request):
    logout(request)
    return redirect('activos')