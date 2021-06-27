# -*- coding: utf-8 -*-
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from main_app.models import *


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer





class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['name'] = user.name
        # Add more custom fields from your custom user model, If you have a
        # custom user model.
        # ...

        return token

        
# USER SERIALIZER
class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
        	"first_name",
        	"last_name",
        	"email"
        ]



# COUNTY SERIALIZER
class CountySerializer(ModelSerializer):
	class Meta:
		model 	= County
		fields 	= [
			'name', 
            'created_at', 
			'slug', 
		]







# USER PROFILE SERIALIZER
class UserProfileSerializer(ModelSerializer):
	first_name 	= serializers.CharField(source='user.first_name', read_only=True)
	last_name 	= serializers.CharField(source='user.last_name', read_only=True)
	email 		= serializers.CharField(source='user.email', read_only=True)
	county 	= serializers.CharField(source='county.name', read_only=True)
	class Meta:
		lookup_field = 'email'
		model  = User
		fields = [
			"first_name",
			"last_name",
			"email",
			"county",
			"created_at",
			"slug"
		]
		read_only_fields = [
			'email',
			'created_at',
            'slug'
		]



# OUTLET CATEGORY SERIALIZER
class OutletCategorySerializer(ModelSerializer):
    class Meta:
        model 	= OutletCategory
        fields 	= [
            'name',
            'created_at',
            'slug', 
        ]




# MODEL SERIALIZER
class OutletSerializer(ModelSerializer):
    user 	 = serializers.CharField(source='user.user', read_only=True)
    county 	 = serializers.CharField(source='user.county', read_only=True)
    category = serializers.CharField(source='category.name', read_only=True)
    class Meta:
        model 	= Outlet
        fields 	= [
            'user',
            'name',
            'county',
            'category',
            'outlet_id',
            'gps',
            'created_at',
            'slug', 
        ]




# BRAND SERIALIZER
class BrandSerializer(ModelSerializer):
    class Meta:
        model 	= Brand
        fields 	= [
            'name', 
            'created_at',	 
            'slug', 
        ]


# MODEL SERIALIZER
class ModelSerializer(ModelSerializer):
    brand_name 	= serializers.CharField(source='brand.name', read_only=True)
    class Meta:
        model 	= Model
        fields 	= [
            'brand_name',
            'name',
            'created_at',
            'slug', 
        ]




# PRODUCT GROUP SERIALIZER
class ProductCategorySerializer(ModelSerializer):
	class Meta:
		model 	= ProductCategory
		fields 	= [
			'name',
            'created_at', 	 
			'slug', 
		]


# MODEL SERIALIZER
class ProductSerializer(ModelSerializer):
    category = serializers.CharField(source='category.name', read_only=True)
    model 	 = serializers.CharField(source='model.name', read_only=True)
    brand 	 = serializers.CharField(source='model.brand.name', read_only=True)
    class Meta:
        model 	= Product
        fields 	= [
            'name',
            'category',
            'brand',
            'model',
            'manufacturer',
            'measure',
            'content',
            'created_at',
            'slug', 
        ]