from django.db import models
from PIL import Image
from slugify import slugify
from io import BytesIO
from django.core.files import File
# Create your models here.


class Product(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False)
    secondtitle = models.CharField(max_length=255, blank=False, null=False)
    firstDisc = models.TextField(max_length=255, blank=False, null=False)
    secondDisc = models.TextField(max_length=255, blank=False, null=False)
    price = models.IntegerField()
    mainDisc = models.TextField(max_length=255, blank=False, null=False)
    firstImage = models.ImageField(upload_to='uploads/', blank=True, null=True)
    secondImage = models.ImageField(upload_to='uploads/', blank=True, null=True)
    thirdImage = models.ImageField(upload_to='uploads/', blank=True, null=True)
    createdAT = models.DateTimeField(auto_now_add=True)
    hrefId = models.SlugField(max_length=255, allow_unicode=True, blank=True, null=True)
    divsId = models.SlugField(max_length=255, allow_unicode=True, blank=True, null=True)
    slug = models.SlugField(max_length=255, allow_unicode=True, blank=True)
    thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True)


    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            self.slug = slugify(self.title)
            self.hrefId = slugify(self.title)
            self.divsId = slugify(self.title)

        super(Product, self).save(*args, **kwargs)

    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        else:
            if self.thirdImage:
                self.thumbnail = self.make_thumbnail(self.thirdImage)
                self.save()

                return self.thumbnail.url

            else:
                return 'https://via.placeholder.com/240x180.jpg'

    def make_thumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=90)

        thumbnail = File(thumb_io, name=image.name)
        return thumbnail

    class Meta:
        verbose_name_plural = 'Product'
        ordering = ['createdAT']

    def __str__(self):
        return self.title


class Order(models.Model):
    email = models.EmailField(unique=True, max_length=100)
    full_name = models.CharField(max_length=100)
    street_address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    paid_amount = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        verbose_name_plural = 'Order'
        ordering = ['-created_at']

    def __str__(self):
        return self.email

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return '%s' % self.id

    def get_total_price(self):
        return self.price * self.quantity