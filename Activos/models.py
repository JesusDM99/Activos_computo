from django.db import models
from django.utils import timezone



class Activo(models.Model): 
    
    tic=models.CharField(max_length=30, verbose_name= 'TIC', unique=True, null=True)
    tipos_activos = models.ForeignKey('Tipos_Activos',on_delete=models.SET_NULL,null=True, blank=True)
    usuario = models.ForeignKey('Usuario', on_delete=models.SET_NULL,null=True, blank=True, related_name='activos_usuario')
    estado=models.ForeignKey('Estado',on_delete=models.SET_NULL ,null=True,blank=True)
    ubicacion =models.ForeignKey('Ubicacion', on_delete=models.SET_NULL,null=True, blank=True)
    evento=models.TextField(verbose_name='Evento',null=True,blank=True)
    condicion=models.ForeignKey('Condicion',verbose_name="condicion",on_delete=models.SET_NULL,null=True,blank=True)
    marca=models.ForeignKey('Marca',on_delete=models.SET_NULL ,null=True,blank=True)
    discos=models.CharField(max_length=55,verbose_name='discos',null= True, blank=True)
    acta = models.ForeignKey('Acta',on_delete=models.SET_NULL, null=True, blank=True, related_name= 'activo_acta')
    licencia = models.ManyToManyField('Licencia', blank=True, related_name='activos_licencia')
    proveedor=models.ForeignKey('Proveedor',on_delete=models.SET_NULL,null=True,blank=True)
    modelo = models.CharField(max_length=55, verbose_name= 'Modelo',null=True,blank=True)
    garantia = models.DateField(verbose_name='Vencimiento Garantia',null=True, blank=True)
    serial = models.CharField(max_length=55, verbose_name= 'Serial',null=True,blank=True)
    ram = models.CharField(max_length=55, verbose_name= 'Ram',null=True,blank=True)
    board = models.CharField(max_length=55, verbose_name= 'Board',null=True,blank=True)
    procesador = models.CharField(max_length=55, verbose_name= 'Procesador',null=True,blank=True)
    nombre_equipo = models.CharField(max_length=59, verbose_name= 'Nombre Equipo',null=True,blank=True)
    sistema_operativo= models.CharField(max_length=55,verbose_name='Sistema Operativo' ,null=True,blank=True)    
    ip = models.CharField(max_length=55, verbose_name= 'Ip',null=True,blank=True)
    pulgadas = models.CharField(max_length=55, verbose_name= 'Pulgadas',null=True,blank=True)
    precio_compra = models.DecimalField(max_digits=10,decimal_places=2, verbose_name= 'Precio Compra',null=True,blank=True)
    fecha_compra = models.DateField(verbose_name='Fecha Compra',null=True,blank=True)
    numero_factura = models.CharField(max_length=20, verbose_name= 'Numero Factura',null=True,blank=True)
    
    class Meta:
        verbose_name= 'Activo'
        verbose_name_plural= ' Activos' 
    def __str__(self):
        return self.tic

class Encabezado(models.Model):
    
    imagen = models.ImageField(upload_to='encabezados/', null=True, blank=True)

    def __str__(self):
        return f'Encabezado #{self.id}'

class Acta(models.Model):
    
    usuario = models.ForeignKey('Usuario', on_delete=models.SET_NULL,null=True, blank=True, related_name='acta_usuario')
    ruta = models.FileField(upload_to='static/actas',null=True, blank=True)    
    class Meta:
        verbose_name= 'Acta'
        verbose_name_plural= ' Actas'
    

class Usuario(models.Model):
    
    nombre=models.CharField(max_length=50,verbose_name='Nombre',null=True)
    cedula = models.CharField(max_length=20,verbose_name='Cedula',unique=True,null=True, blank=True)
    telefono = models.CharField(max_length=20,verbose_name='Telefono',null=True, blank=True)
    direccion = models.ForeignKey('Direccion', on_delete=models.SET_NULL, null=True, blank=True)    
    area= models.ForeignKey('Area', on_delete=models.SET_NULL, null=True, blank=True)    
    cargo= models.ForeignKey('Cargo', on_delete=models.SET_NULL, null=True, blank=True)    
    ciudad = models.ForeignKey('Ciudad',on_delete=models.SET_NULL,null=True, blank=True)

    class Meta:
        verbose_name= 'Usuario'
        verbose_name_plural= ' Usuarios'

    def __str__(self):
        return self.nombre

class Proveedor(models.Model):
    
    nit=models.CharField(max_length=50,verbose_name='Nit', null=True, blank=True)
    nombre=models.CharField(max_length=50,verbose_name='Nombre', null=True, blank=True)
    telefono=models.CharField(max_length=15,verbose_name='Telefono', null=True, blank=True)
    nombre_contacto =models.CharField(max_length=50,verbose_name='Contacto', null=True, blank=True)
    correo=models.CharField(max_length=50,verbose_name='correo', null=True, blank=True)
    
    class Meta:
        verbose_name= 'Proveedor'
        verbose_name_plural= ' Proveedores'

    def __str__(self):
        return self.nombre
    
class Licencia(models.Model):    
    
    proveedor = models.ForeignKey('Proveedor',verbose_name= 'Proveedor', on_delete=models.SET_NULL, null=True, blank=True)        
    tipos_licencia = models.ForeignKey('Tipos_Licencia',on_delete=models.SET_NULL,null=True, blank=True)
    nombre=models.CharField(max_length=30,verbose_name='Nombre', null=True, blank=True)
    version=models.CharField(max_length=30,verbose_name='Version', null=True, blank=True)
    key = models.CharField(max_length=40,verbose_name='Key', unique=True, null=True, blank=True)   
    fecha_compra = models.DateField(verbose_name='Fecha Compra', null=True, blank=True)
    numero_factura = models.CharField(max_length=30,verbose_name='Numero Factura',null=True,blank=True)
    precio_compra = models.CharField(max_length=30, verbose_name='Precio Compra', null=True,blank=True)
    fecha_vigencia = models.DateField(verbose_name='Fecha Vigencia',null=True,blank=True)
    estado = models.BooleanField('Estado',default=True, blank=True)

    class Meta:
        verbose_name= 'Licencia'
        verbose_name_plural= ' Licencias'
    def __str__(self):
        return self.nombre


class Tipos_Licencia(models.Model):
    
    nombre = models.CharField(max_length=100, verbose_name='Tipos Licencia', null=True, unique=True)
    
    class Meta:
        verbose_name= 'Tipo_Licencia'
        verbose_name_plural= ' Tipos_Licencias'
    def __str__(self):
        return self.nombre
  
class Tipos_Activos(models.Model):
    
    nombre = models.CharField(max_length=100, verbose_name='Tipos Activos', null=True, unique=True)

    class Meta:
        verbose_name= 'Tipo_Activo'
        verbose_name_plural= ' Tipos_Activos'
    def __str__(self):
        return self.nombre

class Ciudad(models.Model):
    
    nombre = models.CharField(max_length=100, verbose_name='Ciudad', null=True, unique=True)

    def __str__(self):
        return self.nombre

class Ubicacion(models.Model):
    
    nombre = models.CharField(max_length=100, verbose_name='Ubicacion', null=True, unique=True)

    def __str__(self):
        return self.nombre

class Direccion(models.Model):
    
    nombre = models.CharField(max_length=100, verbose_name='Direccion', null=True, unique=True)

    def __str__(self):
        return self.nombre

class Area(models.Model):
    
    nombre = models.CharField(max_length=100, verbose_name='Area', null=True, unique=True)

    def __str__(self):
        return self.nombre

class Estado(models.Model):
    
    nombre = models.CharField(max_length=100, verbose_name='Estado', null=True, unique=True)

    def __str__(self):
        return self.nombre

class Marca(models.Model):
    
    nombre = models.CharField(max_length=100, verbose_name='Marca', null=True, unique=True)

    def __str__(self):
        return self.nombre
    
class Cargo(models.Model):
    
    nombre = models.CharField(max_length=100, verbose_name='Cargos', null=True, unique=True)

    def __str__(self):
        return self.nombre


class Condicion(models.Model):
    
    nombre = models.CharField(max_length=100, verbose_name='Condicion', null=True, unique=True)

    def __str__(self):
        return self.nombre