# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.db.models.signals import pre_save, post_save

from django.utils.safestring import mark_safe
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _


from ckeditor.fields import RichTextField

from .functions import *




# USER MANAGER
class UserManager(BaseUserManager):
	use_in_migrations = True

	def _create_user(self, email, password, **extra_fields):
		if not email:
			raise ValueError('The given email must be set')
		email = self.normalize_email(email)
		user = self.model(email=email, **extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_user(self, email, password=None, **extra_fields):
		extra_fields.setdefault('is_staff', False)
		extra_fields.setdefault('is_superuser', False)
		return self._create_user(email, password, **extra_fields)

	def create_superuser(self, email, password, **extra_fields):
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_superuser', True)

		if extra_fields.get('is_staff') is not True:
			raise ValueError('Superuser must have is_staff=True.')
		if extra_fields.get('is_superuser') is not True:
			raise ValueError('Superuser must have is_superuser=True.')

		return self._create_user(email, password, **extra_fields)




# USER MODEL
class User(AbstractUser):
	username = None
	email = models.EmailField(_('email address'), unique=True)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []

	objects = UserManager()







# COUNTY MODEL
class County(models.Model):
    name       = models.CharField(_('Name'), unique=True, max_length=100, blank=False, null=False)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True, editable=False)
    slug 	   = models.SlugField(max_length=75, null=True, blank=True, unique=False, editable=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering 	= ['-created_at']
        verbose_name 	= _('County')
        verbose_name_plural = _('Counties')

def create_county_slug(instance, new_slug=None):
	slug = slugify(instance.name)
	if new_slug is not None:
		slug = new_slug
	ourQuery = County.objects.filter(slug=slug)
	exists   = ourQuery.exists()
	if exists:
		new_slug = '%s-%s' %(slug, ourQuery.first().id)
		return create_county_slug(instance, new_slug=new_slug)
	return slug

def presave_county(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = create_county_slug(instance)
pre_save.connect(presave_county, sender=County)








# USER PROFILE MODEL
class UserProfile(models.Model):
    user 		= models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False, null=False, related_name='user_profile')
    county      = models.ForeignKey(County, blank=True, null=True, on_delete=models.CASCADE)
    photo 		= models.ImageField(_('Photo'), upload_to='User_profile/Photo/%m-%Y', blank=True, null=True)
    created_at  = models.DateTimeField(_('Created at'), auto_now_add=True, editable=False)
    updated_at  = models.DateTimeField(_('Updated at'), auto_now=True, editable=False)
    slug 		= models.SlugField(max_length=75, null=True, blank=True, unique=False, editable=False)

    def __str__(self):
        return self.user.email

    class Meta:
        ordering 	= ['-created_at']
        verbose_name 	= _('User profile')
        verbose_name_plural = _('User profiles')

def create_user_profile_slug(instance, new_slug=None):
    slug = slugify(unique_profile_slug_generator(instance))
    if new_slug is not None:
        slug = new_slug
    ourQuery = UserProfile.objects.filter(slug=slug)
    exists   = ourQuery.exists()
    if exists:
        new_slug = '%s-%s' %(slug, ourQuery.first().id)
        return create_user_profile_slug(instance, new_slug=new_slug)
    return slug

def presave_user_profile(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = create_user_profile_slug(instance)
pre_save.connect(presave_user_profile, sender=UserProfile)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
post_save.connect(create_user_profile, sender=User)




# OUTLET CATEGORY MODEL
class OutletCategory(models.Model):
    name       = models.CharField(_('Name'), unique=True, max_length=100, blank=False, null=False)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True, editable=False)
    slug 	   = models.SlugField(max_length=75, null=True, blank=True, unique=False, editable=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering 	= ['-created_at']
        verbose_name 	= _('Outlet Category')
        verbose_name_plural = _('Outlet Categories')

def create_outlet_category_slug(instance, new_slug=None):
	slug = slugify(instance.name)
	if new_slug is not None:
		slug = new_slug
	ourQuery = OutletCategory.objects.filter(slug=slug)
	exists   = ourQuery.exists()
	if exists:
		new_slug = '%s-%s' %(slug, ourQuery.first().id)
		return create_outlet_category_slug(instance, new_slug=new_slug)
	return slug

def presave_outlet_category(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = create_outlet_category_slug(instance)
pre_save.connect(presave_outlet_category, sender=OutletCategory)






# OUTLET MODEL
class Outlet(models.Model):
    user       = models.ForeignKey(UserProfile, blank=False, null=False, on_delete=models.CASCADE, related_name='user_outlet')
    name 	   = models.CharField(_('Name'), unique=True, max_length=100, blank=False, null=False)
    category   = models.ForeignKey(OutletCategory, on_delete=models.CASCADE, blank=False, null=False)
    outlet_id  = models.CharField(_('Outlet id'), unique=True, max_length=120, blank=True, null=True, editable=False)
    gps 	   = models.CharField(_('GPS'), unique=True, max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True, editable=False)
    slug 	   = models.SlugField(max_length=75, null=True, blank=True, unique=False, editable=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering 	= ['-created_at']
    verbose_name 	= _('Outlet')
    verbose_name_plural = _('Outlets')

def create_outlet_slug(instance, new_slug=None):
	slug = slugify(instance.name)
	if new_slug is not None:
		slug = new_slug
	ourQuery = Outlet.objects.filter(slug=slug)
	exists   = ourQuery.exists()
	if exists:
		new_slug = '%s-%s' %(slug, ourQuery.first().id)
		return create_outlet_slug(instance, new_slug=new_slug)
	return slug

def presave_outlet(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = create_outlet_slug(instance)
	if not instance.outlet_id:
		instance.outlet_id = unique_outlet_id_generator(instance)
pre_save.connect(presave_outlet, sender=Outlet)








# Brand MODEL
class Brand(models.Model):
    name 		 = models.CharField(_('Name'), unique=True, max_length=100, blank=False, null=False)
    created_at   = models.DateTimeField(_('Created at'), auto_now_add=True, editable=False)
    updated_at   = models.DateTimeField(_('Updated at'), auto_now=True, editable=False)
    slug 		 = models.SlugField(max_length=75, null=True, blank=True, unique=False, editable=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering 	= ['-created_at']
        verbose_name 	= _('Brand')
        verbose_name_plural = _('Brands')

def create_brand_slug(instance, new_slug=None):
	slug = slugify(instance.name)
	if new_slug is not None:
		slug = new_slug
	ourQuery = Brand.objects.filter(slug=slug)
	exists   = ourQuery.exists()
	if exists:
		new_slug = '%s-%s' %(slug, ourQuery.first().id)
		return create_brand_slug(instance, new_slug=new_slug)
	return slug

def presave_brand(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = create_brand_slug(instance)
pre_save.connect(presave_brand, sender=Brand)





# Model MODEL
class Model(models.Model):
    brand      = models.ForeignKey(Brand, on_delete=models.CASCADE, blank=False, null=False)
    name 	   = models.CharField(_('Name'), unique=True, max_length=100, blank=False, null=False)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True, editable=False)
    slug 	   = models.SlugField(max_length=75, null=True, blank=True, unique=False, editable=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering 	= ['-created_at']
        verbose_name 	= _('Model')
        verbose_name_plural = _('Models')

def create_model_slug(instance, new_slug=None):
	slug = slugify(instance.name)
	if new_slug is not None:
		slug = new_slug
	ourQuery = Model.objects.filter(slug=slug)
	exists   = ourQuery.exists()
	if exists:
		new_slug = '%s-%s' %(slug, ourQuery.first().id)
		return create_model_slug(instance, new_slug=new_slug)
	return slug

def presave_model(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = create_model_slug(instance)
pre_save.connect(presave_model, sender=Model)







# PRODUCT CATEGORY MODEL
class ProductCategory(models.Model):
    name 	   = models.CharField(_('Name'), unique=True, max_length=100, blank=False, null=False)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True, editable=False)
    slug 	   = models.SlugField(max_length=75, null=True, blank=True, unique=False, editable=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering 	= ['-created_at']
        verbose_name 	= _('Product Category')
        verbose_name_plural = _('Product Categories')

def create_product_category_slug(instance, new_slug=None):
	slug = slugify(instance.name)
	if new_slug is not None:
		slug = new_slug
	ourQuery = ProductCategory.objects.filter(slug=slug)
	exists   = ourQuery.exists()
	if exists:
		new_slug = '%s-%s' %(slug, ourQuery.first().id)
		return create_product_category_slug(instance, new_slug=new_slug)
	return slug

def presave_product_category(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = create_product_category_slug(instance)
pre_save.connect(presave_product_category, sender=ProductCategory)





# PRODUCT MODEL
class Product(models.Model):
    name     = models.CharField(_('Name'), unique=True, max_length=100, blank=False, null=False)
    image 	 = models.ImageField(_('Photo'), upload_to='Products/%m-%Y', blank=True, null=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, blank=False, null=False)
    model 	 = models.ForeignKey(Model, on_delete=models.CASCADE, blank=False, null=False)
    manufacturer = models.CharField(_('Manufacturer'), max_length=100, blank=False, null=False)
    measure = models.CharField(_('Measure'), max_length=100, blank=False, null=False)
    content = RichTextField(_('Content'), blank=True, null=True)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True, editable=False)
    slug 	   = models.SlugField(max_length=75, null=True, blank=True, unique=False, editable=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering 	= ['-created_at']
        verbose_name 	= _('Product')
        verbose_name_plural = _('Products')

def create_product_slug(instance, new_slug=None):
	slug = slugify(instance.name)
	if new_slug is not None:
		slug = new_slug
	ourQuery = Product.objects.filter(slug=slug)
	exists   = ourQuery.exists()
	if exists:
		new_slug = '%s-%s' %(slug, ourQuery.first().id)
		return create_product_slug(instance, new_slug=new_slug)
	return slug

def presave_product(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = create_product_slug(instance)
pre_save.connect(presave_product, sender=Product)












# AUDIT MODEL
class Audit(models.Model):
    user       = models.ForeignKey(UserProfile, blank=False, null=False, on_delete=models.CASCADE)
    outlet 	   = models.ForeignKey(Outlet, on_delete=models.CASCADE, blank=False, null=False)
    product    = models.ForeignKey(Product, on_delete=models.CASCADE, blank=False, null=False)
    price      = models.PositiveIntegerField(_('Price'), default=0, blank=False, null=False)
    measure    = models.CharField(_('Measure'), max_length=100, blank=False, null=False)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True, editable=False)
    slug 	   = models.SlugField(max_length=75, null=True, blank=True, unique=False, editable=False)

    def __str__(self):
        return self.outlet.name

    class Meta:
        ordering 	= ['-created_at']
        verbose_name 	= _('Audit')
        verbose_name_plural = _('Audits')

def create_audit_slug(instance, new_slug=None):
    slug = slugify(unique_audit_slug_generator(instance))
    if new_slug is not None:
        slug = new_slug
    ourQuery = Audit.objects.filter(slug=slug)
    exists   = ourQuery.exists()
    if exists:
        new_slug = '%s-%s' %(slug, ourQuery.first().id)
        return create_audit_slug(instance, new_slug=new_slug)
    return slug

def presave_audit(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = create_audit_slug(instance)
pre_save.connect(presave_audit, sender=Audit)







