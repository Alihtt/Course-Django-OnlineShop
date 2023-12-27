from django.db import models
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,unique=True)
    
    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'categories'
    
    def __str__(self) -> str:
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='products')
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,unique=True)
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to=r'products/%Y/%m/%d/')
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('name',)
        
    def __str__(self) -> str:
        return self.name
    
    def get_absolute_url(self):
        return reverse('home:product_detail',args=(self.slug,))
    