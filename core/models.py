import os

from django.db import models
from django.urls import reverse
from django.utils.text import slugify


def upload_to(instance, filename):
    path_to = ''
    ext = filename.split('.')[-1]
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, 'jpg')
    else:
        Model = instance.__class__
        new_id = Model.objects.order_by("id").last().pk
        new_id += 1
        filename = '{}.{}'.format(new_id, 'jpg')
    #     # filename = '{}.{}'.format(uuid4().int, ext)
    return os.path.join(path_to, filename)


class Person(models.Model):
    name = models.CharField(max_length=200, verbose_name='Ady')
    # surname = models.CharField(max_length=150, verbose_name='Familiyasy')
    slug = models.SlugField(max_length=300, unique=True, verbose_name='Url')
    profession = models.CharField(max_length=255, verbose_name='Wezipesi')
    mail = models.EmailField(verbose_name="Pocta")
    phone_number = models.CharField(max_length=100, verbose_name='Nomer telefon')
    image = models.ImageField(upload_to=upload_to, verbose_name='Surat')

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('person', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Adam'
        verbose_name_plural = 'Adamlar'
        ordering = ['-id']


class Get_In(models.Model):
    person_id = models.ForeignKey(Person, on_delete=models.PROTECT, verbose_name='Adam')
    get_in_date = models.DateField(auto_now_add=True, verbose_name='Giren senesi')
    get_in_time = models.TimeField(auto_now_add=True, verbose_name='Giren wagty')
    slug = models.SlugField(unique=True, max_length=500)
    count = models.IntegerField(default=0)

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.person_id.name+'-'+self.person_id.surname+'-'+self.person_id.profession+'-'+self.get_in)
    #     super().save(*args, **kwargs)

    def __str__(self):
        return str(self.person_id)

    class Meta:
        verbose_name = 'Giris wagty'
        verbose_name_plural = 'Giren wagtlary'
        ordering = ['-person_id']


class Get_Out(models.Model):
    person_id = models.ForeignKey(Person, on_delete=models.PROTECT, verbose_name='Adam')
    get_out_date = models.DateTimeField(auto_now_add=True, verbose_name='Cykan senesi')
    get_out_time = models.TimeField(auto_now_add=True, verbose_name='Cykan wagty')
    slug = models.SlugField(unique=True, max_length=500)
    count = models.IntegerField(default=0)

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(
    #         self.person_id.name + '-' + self.person_id.surname + '-' + self.person_id.profession + '-' + self.get_out)
    #     super().save(*args, **kwargs)

    def __str__(self):
        return str(self.person_id)

    class Meta:
        verbose_name = 'Cykys wagty'
        verbose_name_plural = 'Cykys wagtlary'
        ordering = ['-person_id']
