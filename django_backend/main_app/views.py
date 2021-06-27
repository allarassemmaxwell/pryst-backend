# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User

import re
from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse, Http404, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


from django.urls import reverse
from django.contrib.auth.decorators import login_required

from django.template import loader
from .models import *

from django.contrib.auth import get_user_model

from .forms import *


User = get_user_model()



# HOME
@login_required
def home(request):
    template        = "index.html"
    users_number    = User.objects.all().count()
    outlets_number  = Outlet.objects.all().count()
    products_number = Product.objects.all().count()
    audits_number   = Audit.objects.all().count()
    audits          = Audit.objects.all()[:20]
    context = { 
        "users_number": users_number,
        "audits": audits,
        "outlets_number": outlets_number,
        "products_number": products_number,
        "audits_number": audits_number
    }
    return render(request, template, context)






# AUDIT
@login_required
def audit_view(request):
    audits   = Audit.objects.all()
    template = "audit.html"
    context  = { "audits": audits }
    return render(request, template, context)







# EDIT AUDIT
@login_required
def audit_edit_view(request, slug=None):
    template = "audit-edit.html"
    data     = get_object_or_404(Audit, slug=slug)
    outlets  = Outlet.objects.all()
    products = Product.objects.all() 
    users    = User.objects.all() 

    if request.method == "POST":
        outlet_slug  = request.POST.get('outlet_slug', '')
        product_slug = request.POST.get('product_slug', '')
        user         = request.POST.get('user', '')
        price        = request.POST.get('price', '')
        measure      = request.POST.get('measure', '')

        if clean_data(outlet_slug) == '' or clean_data(product_slug) == '' or clean_data(user) == '' or clean_data(price) == '' or clean_data(measure) == '':
            messages.error(request, "All fields are required.")
        else:
            check_outlet = Outlet.objects.filter(slug=outlet_slug).count()
            if check_outlet == 0:
                messages.error(request, "This outlet does not exist.")
            else:
                outlet_instance = Outlet.objects.get(slug=outlet_slug)
                check_product = Product.objects.filter(slug=product_slug).count()
                if check_product == 0:
                    messages.error(request, "This product does not exist.")
                else:
                    product_instance = Product.objects.get(slug=product_slug)
                    check_user = UserProfile.objects.filter(user__email=user).count()
                    if check_user == 0:
                        messages.error(request, "This user does not exist.")
                    else:
                        user_instance = UserProfile.objects.get(user__email=user)
                        data.outlet   = outlet_instance
                        data.product  = product_instance
                        data.user     = user_instance
                        data.price    = price
                        data.measure  = measure
                        data.save()
                        messages.success(request, "Data updated Successfully.")
                        return redirect('main_app:audit')
    context = { 
        "data": data,
        "outlets": outlets,
        "products": products,
        "users": users
    }
    return render(request, template, context)





# DELETE AUDIT
@login_required
def audit_delete_view(request, slug=None):
    audit = get_object_or_404(Audit, slug=slug)
    audit.delete()
    messages.success(request, "Data deleted Successfully.")
    return redirect('main_app:audit')






# BRAND VIEW
@login_required
def brand_view(request):
    brands   = Brand.objects.all()
    template = "brand.html"
    context  = { "brands": brands }
    return render(request, template, context)




# BRAND VIEW
@login_required
def brand_add_view(request):
    template = "brand-add.html"
    if request.method == "POST":
        name = request.POST.get('name', '')
        if clean_data(name) == '':
            messages.error(request, "All fields are required.")
        else:
            check_name = Brand.objects.filter(name=name).count()
            if check_name == 1:
                messages.error(request, "The brand with this name already exists.")
            else:
                Brand.objects.create(name=name).save()
                messages.success(request, "Brand created Successfully.")
                return redirect('main_app:brand')
    return render(request, template, {})






# DELETE BRAND
@login_required
def brand_delete_view(request, slug=None):
    audit = get_object_or_404(Brand, slug=slug)
    audit.delete()
    messages.success(request, "Data deleted Successfully.")
    return redirect('main_app:brand')




# EDIT BRAND
@login_required
def brand_edit_view(request, slug=None):
    template_name = "brand-edit.html"
    data = get_object_or_404(Brand, slug=slug)

    if request.method == "POST":
        name = request.POST.get('name', '')
        if clean_data(name) == '':
            messages.error(request, "All fields are required.")
        else:
            check_name = Brand.objects.filter(name=name).exclude(slug=data.slug).count()
            if check_name == 1:
                messages.error(request, "The brand with this name already exists.")
            else:
                data.name = name
                data.save()
                messages.success(request, "Data updated Successfully.")
                return redirect('main_app:brand')
    return render(request, template_name, {"data": data})




# MODEL VIEW
@login_required
def model_view(request):
    models   = Model.objects.all()
    template = "model.html"
    context  = { "models": models }
    return render(request, template, context)



# ADD NEW MODEL VIEW
@login_required
def model_add_view(request):
    template = "model-add.html"
    brands = Brand.objects.all()
    
    if request.method == "POST":
        name       = request.POST.get('name', '')
        brand_slug = request.POST.get('brand_slug', '')
        
        if clean_data(name) == '' or clean_data(brand_slug) == '':
            messages.error(request, "All fields are required.")
        else:
            check_name = Model.objects.filter(name=name).count()
            if check_name == 1:
                messages.error(request, "The model with this name already exists.")
            else:
                check_brand_slug = Brand.objects.filter(slug=brand_slug).count()
                if check_brand_slug == 0:
                    messages.error(request, "This brand does not exist")
                else:
                    brand_instance = Brand.objects.get(slug=brand_slug)
                    Model.objects.create(name=name, brand=brand_instance).save()
                    messages.success(request, "Model created Successfully.")
                    return redirect('main_app:model')
    return render(request, template, {"brands": brands})




# EDIT MODEL
@login_required
def model_edit_view(request, slug=None):
    template = "model-edit.html"
    data     = get_object_or_404(Model, slug=slug)
    brands   = Brand.objects.all()

    if request.method == "POST":
        name       = request.POST.get('name', '')
        brand_slug = request.POST.get('brand_slug', '')
        if clean_data(name) == '' or clean_data(brand_slug) == '':
            messages.error(request, "All fields are required.")
        else:
            check_name = Model.objects.filter(name=name).exclude(slug=data.slug).count()
            if check_name == 1:
                messages.error(request, "The model with this name already exists.")
            else:
                check_brand = Brand.objects.filter(slug=brand_slug).count()
                if check_brand == 0:
                    messages.error(request, "This brand does not exist.")
                else:
                    brand_instance = Brand.objects.get(slug=brand_slug)
                    data.name = name
                    data.brand = brand_instance
                    data.save()
                    messages.success(request, "Data updated Successfully.")
                    return redirect('main_app:model')
    return render(request, template, {"data": data, "brands": brands})





# DELETE MODEL
@login_required
def model_delete_view(request, slug=None):
    data = get_object_or_404(Model, slug=slug)
    data.delete()
    messages.success(request, "Data deleted Successfully.")
    return redirect('main_app:model')






# COUNTY VIEW
@login_required
def county_view(request):
    counties = County.objects.all()
    template = "county.html"
    context  = { "counties": counties }
    return render(request, template, context)





# ADD COUNTY
@login_required
def county_add_view(request):
    template = "county-add.html"
    if request.method == "POST":
        name = request.POST.get('name', '')
        
        if clean_data(name) == '':
            messages.error(request, "All fields are required.")
        else:
            check_name = County.objects.filter(name=name).count()
            if check_name == 1:
                messages.error(request, "The county with this name already exists.")
            else:
                County.objects.create(name=name).save()
                messages.success(request, "County created Successfully.")
                return redirect('main_app:county')

    return render(request, template, {})







# EDIT COUNTY
@login_required
def county_edit_view(request, slug=None):
    template = "county-edit.html"
    data     = get_object_or_404(County, slug=slug)

    if request.method == "POST":
        name = request.POST.get('name', '')
        if clean_data(name) == '':
            messages.error(request, "All fields are required.")
        else:
            check_name = County.objects.filter(name=name).exclude(slug=data.slug).count()
            if check_name == 1:
                messages.error(request, "The county with this name already exists.")
            else:
                data.name = name
                data.save()
                messages.success(request, "County updated Successfully.")
                return redirect('main_app:county')
    return render(request, template, {"data": data})





# DELETE COUNTY
@login_required
def county_delete_view(request, slug=None):
    data = get_object_or_404(County, slug=slug)
    data.delete()
    messages.success(request, "Data deleted Successfully.")
    return redirect('main_app:county')






# OUTLET VIEW
@login_required
def outlet_view(request):
    outlets  = Outlet.objects.all()
    template = "outlet.html"
    context  = { "outlets": outlets }
    return render(request, template, context)





@login_required
def outlet_add_view(request):
    template   = "outlet-add.html"
    users      = User.objects.all()
    categories = OutletCategory.objects.all()

    if request.method == "POST":
        user_email    = request.POST.get('user_email', '')
        name          = request.POST.get('name', '')
        category_slug = request.POST.get('category_slug', '')
        
        if clean_data(user_email) == '' or clean_data(name) == '' or clean_data(category_slug) == '':
            messages.error(request, "All fields are required.")
        else:
            check_user = UserProfile.objects.filter(user__email=user_email).count()
            if check_user == 0:
                messages.error(request, "This user does not exist")
            else:
                user_instance = UserProfile.objects.get(user__email=user_email)
                check_outlet_name = Outlet.objects.filter(name=name).count()
                if check_outlet_name == 1:
                    messages.error(request, "The outlet with this name already exists")
                else:
                    check_outlet_category = OutletCategory.objects.filter(slug=category_slug).count()
                    if check_outlet_category == 0:
                        messages.error(request, "This Category does not exist")
                    else:
                        outlet_category_instance = OutletCategory.objects.get(slug=category_slug)
                        
                        Outlet.objects.create(user=user_instance, name=name, category=outlet_category_instance).save()
                        messages.success(request, "Outlet created Successfully.")
                        return redirect('main_app:outlet')
    return render(request, template, {'users': users, 'categories': categories})






# EDIT OUTLET
@login_required
def outlet_edit_view(request, slug=None):
    template   = "outlet-edit.html"
    data       = get_object_or_404(Outlet, slug=slug)
    users      = User.objects.all()
    categories = OutletCategory.objects.all()

    if request.method == "POST":
        name          = request.POST.get('name', '')
        user          = request.POST.get('user_email', '')
        category_slug = request.POST.get('category_slug', '')

        if clean_data(name) == '' or clean_data(user) == '' or clean_data(category_slug) == '':
            messages.error(request, "All fields are required.")
        else:
            check_user = UserProfile.objects.filter(user__email=user).count()
            if check_user == 0:
                messages.error(request, "This user does not exist.")
            else:
                user_instance = UserProfile.objects.get(user__email=user)
            check_name = Outlet.objects.filter(name=name).exclude(slug=data.slug).count()
            if check_name == 1:
                messages.error(request, "The model with this name already exists.")
            else:
                check_category = OutletCategory.objects.filter(slug=category_slug).count()
                if check_category == 0:
                    messages.error(request, "This Category does not exist.")
                else:
                    category_instance = OutletCategory.objects.get(slug=category_slug)
                    data.user = user_instance
                    data.name = name
                    data.category = category_instance
                    data.save()
                    messages.success(request, "Data updated Successfully.")
                    return redirect('main_app:outlet')
    context = {
        "data": data, 
        "users": users, 
        "categories": categories
    }
    return render(request, template, context)





# DELETE OUTLET
@login_required
def outlet_delete_view(request, slug=None):
    data = get_object_or_404(Outlet, slug=slug)
    data.delete()
    messages.success(request, "Data deleted Successfully.")
    return redirect('main_app:outlet')




# OUTLET CATEGORY VIEW
@login_required
def outlet_category_view(request):
    categories = OutletCategory.objects.all()
    template   = "outlet-category.html"
    context    = { "categories": categories }
    return render(request, template, context)




# OUTLET ADD CATEGORY VIEW
@login_required
def outlet_category_add_view(request):
    template = "outlet-category-add.html"
    if request.method == "POST":
        name = request.POST.get('name', '')
        
        if clean_data(name) == '':
            messages.error(request, "All fields are required.")
        else:
            check_name = OutletCategory.objects.filter(name=name).count()
            if check_name == 1:
                messages.error(request, "The category with this name already exists.")
            else:
                OutletCategory.objects.create(name=name).save()
                messages.success(request, "Outlet Category created Successfully.")
                return redirect('main_app:outlet-category')
    return render(request, template, {})





# EDIT OUTLET CATEGORY
@login_required
def outlet_category_edit_view(request, slug=None):
    template = "outlet-category-edit.html"
    data = get_object_or_404(OutletCategory, slug=slug)

    if request.method == "POST":
        name = request.POST.get('name', '')
        if clean_data(name) == '':
            messages.error(request, "All fields are required.")
        else:
            check_name = OutletCategory.objects.filter(name=name).exclude(slug=data.slug).count()
            if check_name == 1:
                messages.error(request, "The category with this name already exists.")
            else:
                data.name = name
                data.save()
                messages.success(request, "Category updated Successfully.")
                return redirect('main_app:outlet-category')
    return render(request, template, {"data": data})






# DELETE OUTLET CATEGORY
@login_required
def outlet_category_delete_view(request, slug=None):
    data = get_object_or_404(OutletCategory, slug=slug)
    data.delete()
    messages.success(request, "Data deleted Successfully.")
    return redirect('main_app:outlet-category')





# OUTLET LOCATIONS VIEW
@login_required
def outlet_locations_view(request):
    outlets  = Outlet.objects.all()
    template = "outlet-locations.html"
    context  = { "outlets": outlets }
    return render(request, template, context)



# PRODUCT VIEW
@login_required
def product_view(request):
    products = Product.objects.all()
    template = "product.html"
    context  = { "products": products }
    return render(request, template, context)






# ADD PRODUCT VIEW
@login_required
def product_add_view(request):
    template = "product-add.html"
    productCategories = ProductCategory.objects.all()
    models = Model.objects.all()
    if request.method == "POST":
        name          = request.POST.get('name', '')
        model_slug    = request.POST.get('model_slug', '')
        measure       = request.POST.get('measure', '')
        category_slug = request.POST.get('category_slug', '')
        manufacturer  = request.POST.get('manufacturer', '')
        content       = request.POST.get('content', '')
        
        if clean_data(name) == '' or clean_data(model_slug) == '' or clean_data(measure) == '' or clean_data(category_slug) == '' or clean_data(manufacturer) == '' :
            messages.error(request, "All fields are required.")
        else:
            check_name = Product.objects.filter(name=name).count()
            if check_name == 1:
                messages.error(request, "The product with this name already exists.")
            else:
                check_model_slug = Model.objects.filter(slug=model_slug).count()
                if check_model_slug == 0:
                    messages.error(request, "This Model does not exist")
                else:
                    model_instance = Model.objects.get(slug=model_slug)
                    check_category_slug = ProductCategory.objects.filter(slug=category_slug).count()
                    if check_category_slug == 0:
                        messages.error(request, "This Category does not exist")
                    else:
                        category_instance = ProductCategory.objects.get(slug=category_slug)
                        Product.objects.create(name=name, category=category_instance, model=model_instance, manufacturer=manufacturer, measure=measure, content=content).save()
                        messages.success(request, "Product created Successfully.")
                        return redirect('main_app:product')

    return render(request, template, { "productCategories": productCategories, "models": models})







# PRODUCT EDIT VIEW
@login_required
def product_edit_view(request, slug=None):
    template   = "product-edit.html"
    data       = get_object_or_404(Product, slug=slug)
    categories = ProductCategory.objects.all()
    models     = Model.objects.all()

    if request.method == "POST":
        name          = request.POST.get('name', '')
        model_slug    = request.POST.get('model_slug', '')
        measure       = request.POST.get('measure', '')
        category_slug = request.POST.get('category_slug', '')
        manufacturer  = request.POST.get('manufacturer', '')
        content       = request.POST.get('content', '')
        if clean_data(name) == '' or clean_data(model_slug) == '' or clean_data(measure) == '' or clean_data(category_slug) == '' or clean_data(manufacturer) == '':
            messages.error(request, "All fields are required except content.")
        else:
            check_name = Product.objects.filter(name=name).exclude(slug=data.slug).count()
            if check_name == 1:
                messages.error(request, "The product with this name already exists.")
            else:
                check_category = ProductCategory.objects.filter(slug=category_slug).count()
                if check_category == 0:
                    messages.error(request, "This Category does not exist.")
                else:
                    category_instance = ProductCategory.objects.get(slug=category_slug)
                    check_model = Model.objects.filter(slug=model_slug).count()
                    if check_model == 0:
                        messages.error(request, "This Model does not exist.")
                    else:
                        model_instance = Model.objects.get(slug=model_slug)
                        data.name = name
                        data.category = category_instance
                        data.model = model_instance
                        data.manufacturer = manufacturer
                        data.measure = measure
                        data.content = content
                        data.save()
                        messages.success(request, "Data updated Successfully.")
                        return redirect('main_app:product')
    context = {
        "data": data, 
        "models": models, 
        "categories": categories
    }
    return render(request, template, context)






# DELETE PRODUCT
@login_required
def product_delete_view(request, slug=None):
    data = get_object_or_404(Product, slug=slug)
    data.delete()
    messages.success(request, "Data deleted Successfully.")
    return redirect('main_app:product')






# PRODUCT DETAILS VIEW
@login_required
def product_details_view(request, slug=None):
    detail   = get_object_or_404(Product, slug=slug)
    template = "product-details.html"
    context  = { "detail": detail }
    return render(request, template, context)



# PRODUCT CATEGORY VIEW
@login_required
def product_category_view(request):
    categories = ProductCategory.objects.all()
    template   = "product-category.html"
    context    = { "categories": categories }
    return render(request, template, context)




@login_required
def product_category_add_view(request):
    template = "product-category-add.html"
    if request.method == "POST":
        name = request.POST.get('name', '')
        
        if clean_data(name) == '':
            messages.error(request, "All fields are required.")
        else:
            check_name = ProductCategory.objects.filter(name=name).count()
            if check_name == 1:
                messages.error(request, "The category with this name already exists.")
            else:
                ProductCategory.objects.create(name=name).save()
                messages.success(request, "Product category created Successfully.")
                return redirect('main_app:product-category')

    return render(request, template, {})








# EDIT PRODUCT CATEGORY
@login_required
def product_category_edit_view(request, slug=None):
    template = "product-category-edit.html"
    data     = get_object_or_404(ProductCategory, slug=slug)

    if request.method == "POST":
        name = request.POST.get('name', '')
        if clean_data(name) == '':
            messages.error(request, "All fields are required.")
        else:
            check_name = ProductCategory.objects.filter(name=name).exclude(slug=data.slug).count()
            if check_name == 1:
                messages.error(request, "The category with this name already exists.")
            else:
                data.name = name
                data.save()
                messages.success(request, "Category updated Successfully.")
                return redirect('main_app:product-category')
    return render(request, template, {"data": data})






# DELETE PRODUCT CATEGORY
@login_required
def product_category_delete_view(request, slug=None):
    data = get_object_or_404(ProductCategory, slug=slug)
    data.delete()
    messages.success(request, "Data deleted Successfully.")
    return redirect('main_app:product-category')




# USERS LIST VIEW
@login_required
def users_list_view(request):
    users    = UserProfile.objects.all()
    template = "users-list.html"
    context  = { "users": users }
    return render(request, template, context)




# DELETE PRODUCT CATEGORY
@login_required
def user_actif_inactif_view(request, slug=None):
    data       = get_object_or_404(UserProfile, slug=slug)
    check_user = User.objects.filter(email=data).count()
    if check_user == 0:
        messages.error(request, "This user does not exist.") 
    else:
        user = User.objects.get(email=data)
        if user.is_active == False:
            user.is_active = True
            user.save()
            messages.success(request, "%s %s" %(user.first_name, user.last_name)+" switched to active.")
        else:
            user.is_active = False
            user.save()
            messages.warning(request, "%s %s" %(user.first_name, user.last_name)+" switched to inactive.")

    return redirect(request.META['HTTP_REFERER'])






# USERS LIST VIEW
@login_required
def add_user_view(request):
    counties = County.objects.all()
    template_name = "user-add.html"
    if request.method == "POST":
        first_name  = request.POST.get('first_name', '')
        last_name   = request.POST.get('last_name', '')
        email       = request.POST.get('email', '')
        password1   = request.POST.get('password1', '')
        password2   = request.POST.get('password2', '')
        county_slug = request.POST.get('county_slug', '')
        admin       = request.POST.get('admin', '')
        active      = request.POST.get('active', '')
        
        if clean_data(first_name) == '' or clean_data(last_name) == '' or clean_data(email) == '' or clean_data(password1) == '' or clean_data(password2) == '' or clean_data(county_slug) == '' or clean_data(admin) == '' or clean_data(active) == '':
            messages.error(request, "All fields are required.")
        else:
            if password1 != password2:
                messages.error(request, "Passwords do not match.")
            else:
                check_email = User.objects.filter(email=email).count()
                if check_email == 1:
                    messages.error(request, "This Email is already taken.")
                else:
                    check_county = County.objects.filter(slug=county_slug).count()
                    if check_county == 0:
                        messages.error(request, "This County does not exist.")
                    else:
                        county_instance = County.objects.get(slug=county_slug)
                        user = User.objects.create_user(email=email, first_name=first_name, last_name=last_name, is_active=active, is_superuser=admin, is_staff=admin, password=password1)
                        user.save()
                        check_user_profile = UserProfile.objects.filter(user__email=email).count()
                        if check_user_profile == 0:
                            UserProfile.objects.create(user__email=email, county=county_instance).save()
                        else:
                            user_profile = UserProfile.objects.get(user__email=email)
                            user_profile.county = county_instance
                            user_profile.save()
                        messages.success(request, "User created Successfully.")
                        return redirect('main_app:users-list')
    return render(request, template_name, {"counties": counties})






# EDIT USER PROFILE
@login_required
def user_edit_view(request, slug=None):
    template = "user-edit.html"
    data     = get_object_or_404(UserProfile, slug=slug)
    counties = County.objects.all()
    models   = Model.objects.all()

    if request.method == "POST":
        first_name  = request.POST.get('first_name', '')
        last_name   = request.POST.get('last_name', '')
        county_slug = request.POST.get('county_slug', '')
        active      = request.POST.get('active', '')
        admin       = request.POST.get('admin', '')

        if clean_data(first_name) == '' or clean_data(last_name) == '' or clean_data(county_slug) == '' or clean_data(active) == '' or clean_data(admin) == '':
            messages.error(request, "All fields are required.")
        else:
            check_email = User.objects.filter(email=data.user.email).count()
            if check_email == 0:
                messages.error(request, "This Email does not exist")
            else:
                user_instance = User.objects.get(email=data.user)
                check_county = County.objects.filter(slug=county_slug).count()
                if check_county == 0:
                    messages.error(request, "This County does not exist")
                else:
                    county_instance = County.objects.get(slug=county_slug)
                    user_instance.first_name = first_name
                    user_instance.last_name = last_name
                    user_instance.is_active = active
                    user_instance.is_superuser = admin
                    user_instance.save()
                    data.county = county_instance
                    data.save()
                    messages.success(request, "Profile updated Successfully.")
                    return redirect('main_app:users-list')
    context = {
        "data": data, 
        "models": models, 
        "counties": counties
    }
    return render(request, template, context)






# DELETE USER
@login_required
def user_delete_view(request, slug=None):
    data        = get_object_or_404(UserProfile, slug=slug)
    delete_user = User.objects.get(email=data.user)
    delete_user.delete()
    messages.success(request, "User deleted Successfully.")
    return redirect('main_app:users-list')





# USER LOGIN
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(email=username, password=password)
        if user:
            if user.is_active and user.is_staff:
                login(request, user)
                messages.success(request, "Successfully Logged In. Welcome back!")
                return HttpResponseRedirect(reverse('main_app:home'))
            else:
                messages.error(request, "Your account was inactive or You don't have permission to log in.")
                return redirect(request.META['HTTP_REFERER'])
        else:
            messages.error(request, "Invalid login details given.")
            return redirect(request.META['HTTP_REFERER'])
    else:
        
        return render(request, 'auth-login.html', {})



# USER LOGOUT
@login_required
def logout_view(request):
    logout(request)
    # messages.info(request, "Logged out successfully!")
    return HttpResponseRedirect(reverse('main_app:login'))





# RESET USER PASSWORD
def reset_password(request):
    template = "auth-recoverpw.html"
    context  = { }
    return render(request, template, context)




# CHANGE USER PASSWORD
@login_required
def change_password(request, slug=None):
    template = "change-password.html"
    data     = get_object_or_404(UserProfile, slug=slug)

    if request.method == 'POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if clean_data(password1) == '' or clean_data(password2) == '':
            messages.error(request, "All fields are required.")
        else:
            if password1 != password2 :
                messages.error(request, "Passwords do not match.")
            else:
                check_user = User.objects.filter(email=data).count()
                if check_user == 0:
                    messages.error(request, "This user does not exist.")
                else:
                    user_instance = User.objects.get(email=data)
                    user_instance.set_password(password1)
                    user_instance.save()
                    messages.success(request, "Password changed successfully.")
                    return HttpResponseRedirect(reverse('main_app:users-list'))
    context = {"data": data }
    return render(request, template, context)





# USER PROFILE VIEW
@login_required
def profile_view(request):
    template = "profile.html"
    user     = request.user
    if UserProfile.objects.filter(user=user):
        userProfile = UserProfile.objects.get(user=user)
    else:
        return Http404
    user_outlet        = Outlet.objects.filter(user=userProfile).count()
    user_audit         = Audit.objects.filter(user=userProfile).count()
    total_outlet       = Outlet.objects.all().count()
    total_product      = Product.objects.all().count()
    total_audit        = Audit.objects.all().count()
    total_user         = User.objects.all().count()
    list_of_my_outlets = Outlet.objects.filter(user=userProfile)[:10]
    list_of_my_audits  = Audit.objects.filter(user=userProfile)[:10]
    context = { 
        "userProfile": userProfile,
        "total_outlet": total_outlet,
        "total_product": total_product,
        "total_audit": total_audit,
        "total_user": total_user,
        "user_outlet": user_outlet,
        "user_audit": user_audit,
        "list_of_my_outlets": list_of_my_outlets,
        "list_of_my_audits": list_of_my_audits
    }
    return render(request, template, context)


