from django.urls import path
from django.views.generic import TemplateView

from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

from .views import *

app_name="web"


urlpatterns = [

    path('', home, name="home"),

    path('audit/', audit_view, name="audit"),
    path('audit/edit/<slug:slug>/', audit_edit_view, name='audit-edit'),
    path('audit/delete/<slug:slug>/', audit_delete_view, name='audit-delete'),

    path('brand/', brand_view, name="brand"),
    path('brand/add/', brand_add_view, name="brand-add"),
    path('brand/edit/<slug:slug>/', brand_edit_view, name='brand-edit'),
    path('brand/delete/<slug:slug>/', brand_delete_view, name='brand-delete'),

    path('county/', county_view, name="county"),
    path('county/add/', county_add_view, name="county-add"),
    path('county/edit/<slug:slug>/', county_edit_view, name='county-edit'),
    path('county/delete/<slug:slug>/', county_delete_view, name='county-delete'),

    path('model/', model_view, name="model"),
    path('model/add/', model_add_view, name="model-add"),
    path('model/edit/<slug:slug>/', model_edit_view, name='model-edit'),
    path('model/delete/<slug:slug>/', model_delete_view, name='model-delete'),

    path('outlet/', outlet_view, name="outlet"),
    path('outlet/add/', outlet_add_view, name="outlet-add"),
    path('outlet/edit/<slug:slug>/', outlet_edit_view, name='outlet-edit'),
    path('outlet/delete/<slug:slug>/', outlet_delete_view, name='outlet-delete'),

    path('outlet/category/', outlet_category_view, name="outlet-category"),
    path('outlet/category/add/', outlet_category_add_view, name="outlet-category-add"),
    path('outlet/category/edit/<slug:slug>/', outlet_category_edit_view, name='outlet-category-edit'),
    path('outlet/category/delete/<slug:slug>/', outlet_category_delete_view, name='outlet-category-delete'),
    path('outlet/locations/', outlet_locations_view, name="outlet-locations"),


    path('product/', product_view, name="product"),
    path('product/add/', product_add_view, name="add-product"),
    path('product/edit/<slug:slug>/', product_edit_view, name='product-edit'),
    path('product/delete/<slug:slug>/', product_delete_view, name='product-delete'),
    path('product/view/<slug:slug>/', product_details_view, name='product-details'),

    path('product/category/', product_category_view, name="product-category"),
    path('product/category/add/', product_category_add_view, name="product-category-add"),
    path('product/category/edit/<slug:slug>/', product_category_edit_view, name='product-category-edit'),
    path('product/category/delete/<slug:slug>/', product_category_delete_view, name='product-category-delete'),

    path('users-list/', users_list_view, name="users-list"),
    path('users/add/', add_user_view, name="add-user"),
    path('users/edit/<slug:slug>/', user_edit_view, name='user-edit'),
    path('users/delete/<slug:slug>/', user_delete_view, name='user-delete'),
    path('user/delete/<slug:slug>/', user_actif_inactif_view, name='user-actif-inactif'),



    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
    path('reset-password/', reset_password, name="reset-password"),
    path('change-password/<slug:slug>/', change_password, name="change-password"),
    path('account/', profile_view, name="profile"),



]
