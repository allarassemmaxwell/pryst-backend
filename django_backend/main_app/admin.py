# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import *

admin.site.site_header = "Prystins Insights"

# Register your models here.




@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name', 'is_active', 'is_staff')
    ordering = ('email',)
    readonly_fields = ('last_login', 'date_joined',)



# COUNTY ADMIN
class CountyAdmin(admin.ModelAdmin):
    date_hierarchy      = 'created_at'
    list_display        = ['name', 'created_at', 'updated_at']
    list_display_links  = ['name',]
    list_filter         = ['name', 'created_at', 'updated_at']
    search_fields       = ['name', 'created_at']
    list_per_page       = 25
    class Meta:
        model = County

admin.site.register(County, CountyAdmin)



# OUTLET CATEGORY ADMIN
class OutletCategoryAdmin(admin.ModelAdmin):
    date_hierarchy      = 'created_at'
    list_display        = ['name', 'created_at', 'updated_at']
    list_display_links  = ['name',]
    list_filter         = ['name', 'created_at', 'updated_at']
    search_fields       = ['name', 'created_at']
    list_per_page       = 25
    class Meta:
        model = OutletCategory

admin.site.register(OutletCategory, OutletCategoryAdmin)




# OUTLET ADMIN
class OutletAdmin(admin.ModelAdmin):
    date_hierarchy      = 'created_at'
    list_display        = ['name', 'outlet_id', 'user', 'created_at']
    list_display_links  = ['name', 'outlet_id', 'user']
    list_filter         = ['name', 'outlet_id', 'created_at', 'updated_at']
    search_fields       = ['name', 'user__user__email', 'user__user__first_name', 'user__user__last_name', 'outlet_id', 'category__name', 'gps', 'created_at']
    list_per_page       = 25
    class Meta:
        model = Outlet

admin.site.register(Outlet, OutletAdmin)



# BRAND ADMIN
class BrandAdmin(admin.ModelAdmin):
    date_hierarchy      = 'created_at'
    list_display        = ['name', 'created_at']
    list_display_links  = ['name',]
    list_filter         = ['name', 'created_at', 'updated_at']
    search_fields       = ['name', 'created_at']
    list_per_page       = 25
    class Meta:
        model = Brand

admin.site.register(Brand, BrandAdmin)




# MODEL ADMIN
class ModelAdmin(admin.ModelAdmin):
    date_hierarchy      = 'created_at'
    list_display        = ['brand', 'name', 'created_at', 'updated_at']
    list_display_links  = ['name']
    list_filter         = ['name', 'created_at', 'updated_at']
    search_fields       = ['name', 'brand__name', 'created_at']
    list_per_page       = 25
    class Meta:
        model = Model

admin.site.register(Model, ModelAdmin)






# CATEGORY ADMIN
class ProductCategoryAdmin(admin.ModelAdmin):
    date_hierarchy      = 'created_at'
    list_display        = ['name', 'created_at', 'updated_at']
    list_display_links  = ['name']
    list_filter         = ['name', 'created_at', 'updated_at']
    search_fields       = ['name', 'created_at']
    list_per_page       = 25
    class Meta:
        model = ProductCategory

admin.site.register(ProductCategory, ProductCategoryAdmin)





# PG NAME ADMIN
class ProductAdmin(admin.ModelAdmin):
    date_hierarchy      = 'created_at'
    list_display        = ['name', 'category', 'model', 'created_at']
    list_display_links  = ['name', 'category', 'model',]
    list_filter         = ['name', 'category', 'model', 'created_at', 'updated_at']
    search_fields       = ['name', 'category__name', 'model__name', 'manifacturer', 'measure', 'created_at']
    list_per_page       = 25
    class Meta:
        model = Product

admin.site.register(Product, ProductAdmin)




# audit ADMIN
class AuditAdmin(admin.ModelAdmin):
    date_hierarchy      = 'created_at'
    list_display        = ['user', 'outlet', 'product', 'created_at']
    list_display_links  = ['user', 'outlet', 'product']
    list_filter         = ['user__user__email', 'outlet__name', 'product__name', 'created_at']
    search_fields       = ['user__user__email', 'user__user__first_name', 'user__user__last_name', 'outlet__name', 'product__name', 'price', 'measure', 'created_at']
    list_per_page       = 25
    class Meta:
        model = Audit

admin.site.register(Audit, AuditAdmin)




# USER PROFILE ADMIN
class UserProfileAdmin(admin.ModelAdmin):
    date_hierarchy      = 'created_at'
    list_display        = ['user', 'county', 'created_at']
    list_display_links  = ['user',]
    list_filter         = ['user', 'created_at']
    search_fields       = ['user', 'county', 'gender', 'created_at']
    list_per_page       = 25
    class Meta:
        model = UserProfile

admin.site.register(UserProfile, UserProfileAdmin)


