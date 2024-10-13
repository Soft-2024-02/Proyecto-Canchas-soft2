from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group

class UsuarioManager(BaseUserManager):
    def create_user(self, email, dni, nombre, apellidos, celular, password=None):
        if not email:
            raise ValueError('El usuario debe tener un correo electrónico.')
        if not dni:
            raise ValueError('El usuario debe tener un DNI.')
        if not nombre:
            raise ValueError('El usuario debe tener un nombre.')
        if not apellidos:
            raise ValueError('El usuario debe tener apellidos.')
        if not celular:
            raise ValueError('El usuario debe tener un número de celular.')
        
        # Creación del usuario
        user = self.model(
            email=self.normalize_email(email),
            dni=dni,
            nombre=nombre,
            apellidos=apellidos,
            celular=celular,
            is_active=True,
            is_staff=False,
            is_superuser=False
        )
        
        # Asignación de contraseña
        user.set_password(password)
        user.save(using=self._db)
        
        # Asignar el grupo "Cliente" automáticamente al crear un nuevo usuario
        cliente_group, _ = Group.objects.get_or_create(name='Cliente')
        user.groups.add(cliente_group)
        
        return user
    
    def create_superuser(self, email, dni, nombre, apellidos, celular, password=None):
        # Creación del superusuario
        user = self.create_user(
            email=email,
            dni=dni,
            nombre=nombre,
            apellidos=apellidos,
            celular=celular,
            password=password
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        
        # Asignar el grupo "Administrador" automáticamente
        admin_group, _ = Group.objects.get_or_create(name='Administrador')
        user.groups.add(admin_group)
        
        return user

class Usuario(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('Correo electrónico', max_length=255, unique=True)
    dni = models.CharField('DNI', max_length=8, unique=True)
    nombre = models.CharField('Nombre', max_length=35)
    apellidos = models.CharField('Apellidos', max_length=35)
    celular = models.CharField('Celular', max_length=9, unique=True)
    imagen = models.ImageField('Imagen', upload_to='usuarios/', default='usuarios/default-avatar.jpg')
    is_active = models.BooleanField('Activo', default=True)
    is_staff = models.BooleanField('Staff', default=False)
    is_superuser = models.BooleanField('Superusuario', default=False)
    slug = models.SlugField(max_length=100, unique=False, blank=True)
    
    objects = UsuarioManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['dni', 'nombre', 'apellidos', 'celular']
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        
    def __str__(self):
        return f'{self.nombre} {self.apellidos}'
    
    def save(self, *args, **kwargs):
        if not self.pk or Usuario.objects.get(pk=self.pk).nombre != self.nombre:
            self.slug = slugify(f'{self.nombre} {self.apellidos}')
        
        super(Usuario, self).save(*args, **kwargs)
    
    @property
    def is_responsible(self):
        return self.groups.filter(name='Responsable').exists()
