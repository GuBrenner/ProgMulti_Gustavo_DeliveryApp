import uuid
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
CATEGORY_CHOICES=(
    ('BG', 'Burgers'),
    ('PF', 'Pratos Feitos'),
    ('LC', 'Lanches'),
    ('BB', 'Bebidas'),
    ('SM', 'Sobremesas'),

)

STATE_CHOICES=(
    ('AC', 'Acre'),
        ('AL', 'Alagoas'),
        ('AP', 'Amapá'),
        ('AM', 'Amazonas'),
        ('BA', 'Bahia'),
        ('CE', 'Ceará'),
        ('DF', 'Distrito Federal'),
        ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'),
        ('MA', 'Maranhão'),
        ('MT', 'Mato Grosso'),
        ('MS', 'Mato Grosso do Sul'),
        ('MG', 'Minas Gerais'),
        ('PA', 'Pará'),
        ('PB', 'Paraíba'),
        ('PR', 'Paraná'),
        ('PE', 'Pernambuco'),
        ('PI', 'Piauí'),
        ('RJ', 'Rio de Janeiro'),
        ('RN', 'Rio Grande do Norte'),
        ('RS', 'Rio Grande do Sul'),
        ('RO', 'Rondônia'),
        ('RR', 'Roraima'),
        ('SC', 'Santa Catarina'),
        ('SP', 'São Paulo'),
        ('SE', 'Sergipe'),
        ('TO', 'Tocantins'),
)

STATUS_CHOICES=(
    ('Aceito', 'Aceito'),
    ('Embalado', 'Embalado'),
    ('A caminho', 'A caminho'),
    ('Entregue', 'Entregue'),
    ('Cancelado', 'Cancelado'),
    ('Pendente', 'Pendente'),

)

class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models. TextField()
    composition = models.TextField(default = '')
    prodapp = models.TextField(default= '')
    category = models.CharField(choices = CATEGORY_CHOICES, max_length=2)
    product_image = models.ImageField(upload_to='product')
    def __str__(self):
        return self.title
    

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    name = models.CharField(max_length = 200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length= 50 )
    mobile = models.IntegerField(default=0)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES, max_length= 100)
    def __str__(self):
        return self.name
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_cost(self):
       return self.quantity * self.product.discounted_price
    
    class Meta:
        unique_together = ('user', 'product')


class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default = 1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pendente')
    order_id = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price
