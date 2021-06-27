from django.shortcuts import render

from django.urls import reverse

from .serializer import *
from main_app.models import *

from django.contrib.auth import authenticate, get_user_model

from django.contrib.auth.decorators import login_required
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes

from main_app.functions import *
from django.http import HttpResponse

from django.db.models import Q


from django.views.decorators.csrf import csrf_exempt
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)





class HelloView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)






# OUTLET CATEGORY LIST VIEW
class OutletCategoryListView(ListAPIView):
	permission_classes = (AllowAny,)             
	serializer_class = OutletCategorySerializer

	def get_queryset(self, *args, **kwargs):
		queryset = OutletCategory.objects.order_by('-created_at')
		return queryset



# OUTLET LIST VIEW
class OutletList(ListAPIView):
    permission_classes = (AllowAny,) 
    serializer_class = OutletSerializer

    def get_queryset(self, *args, **kwargs):
        userEmail  = self.request.GET.get("userEmail", None)
        if clean_data(userEmail) == '':
            queryset = Outlet.objects.all()[:0]
        else:
            check_user = UserProfile.objects.filter(user__email=userEmail).count()
            if check_user == 0:
                queryset = Outlet.objects.all()[:0]
            else:
                user_instance = UserProfile.objects.get(user__email=userEmail)
                queryset = Outlet.objects.filter(user=user_instance)
        return queryset




# CREATE OUTLET
class createOutletView(APIView):
    permission_classes = (AllowAny,) 

    def get(self, request,  *args, **kwargs):
        userEmail = request.GET.get('userEmail', None)
        name      = request.GET.get('name', None)
        category  = request.GET.get('category', None)
        if clean_data(userEmail) == '' or clean_data(name) == '' or clean_data(category) == '':
            return Response({"result": "0", "success": "", "error": "All fields are required."})
        else:
            check_user = UserProfile.objects.filter(user__email=userEmail).count()
            if check_user == 0:
                return Response({"result": "0", "success": "", "error": "This user does not exist."})
            else:
                user_instance = UserProfile.objects.get(user__email=userEmail)
                check_category = OutletCategory.objects.filter(slug=category).count()
                if check_category == 0:
                    return Response({"result": "0", "success": "", "error": "This Category does not exist."})
                else:
                    category_instance = OutletCategory.objects.get(slug=category)
                    check_name = Outlet.objects.filter(name=name).count()
                    if check_name == 1:
                        return Response({"result": "0", "success": "", "error": "Outlet with this name already exists."})
                    else:
                        Outlet.objects.create(user=user_instance, name=name, category=category_instance).save()
                        return Response({"result": "1", "success": "Outlet created successfully", "error": ""})



# CREATE AUDIT
class auditSaveView(APIView):
    permission_classes = (AllowAny,) 

    def get(self, request,  *args, **kwargs):
        outlet  = request.GET.get('outlet', None)
        product = request.GET.get('product', None)
        price   = request.GET.get('price', None)
        measure = request.GET.get('measure', None)
        auditor = request.GET.get('auditor', None)
        if clean_data(auditor) == '' or clean_data(outlet) == '' or clean_data(product) == '' or clean_data(price) == '' or clean_data(measure) == '':
            return Response({"result": "0", "success": "", "error": "All fields are required."})
        else:
            check_auditor = UserProfile.objects.filter(user__email=auditor).count()
            if check_auditor == 0:
                return Response({"result": "0", "success": "", "error": "This user does not exist."})
            else:
                user_instance = UserProfile.objects.get(user__email=auditor)
                check_outlet  = Outlet.objects.filter(name=outlet).count()
                if check_outlet == 0:
                    return Response({"result": "0", "success": "", "error": "This outlet does not exist."})
                else:
                    outlet_instance = Outlet.objects.get(name=outlet)
                    check_product = Product.objects.filter(name=product).count()
                    if check_product == 0:
                        return Response({"result": "0", "success": "", "error": "This product does not exist."})
                    else:
                        product_instance = Product.objects.get(name=product)
                        Audit.objects.create(user=user_instance, outlet=outlet_instance, product=product_instance, price=price, measure=measure).save()
                        return Response({"result": "1", "success": "Data submitted successfully", "error": ""})




# PRODUCT LIST VIEW
class ProductList(ListAPIView):
    permission_classes = []
    serializer_class = ProductSerializer

    def get_queryset(self, *args, **kwargs):
        queryset = Product.objects.all().order_by('-created_at')
        return queryset






# USER LOG IN VIEW
class LoginView(APIView):
    permission_classes = (AllowAny,) 
    def get(self, request,  *args, **kwargs):
        username	= request.GET.get('username', None)
        password	= request.GET.get('password', None)

        if username is None or password is None:
            content = {'result': '0', 'error': 'Please provide both registration number and password.'}
            return Response(content)
        user = authenticate(email=username, password=password)
        if user:
            if user.is_active:
                content = {'result': '1', 'userEmail': user.email}
                return Response(content)
            else:
                content = {'result': '0', 'error': "Your account was inactive or You don't have permission to log in."}
                return Response(content)
        else:
            content = {'result': '0', 'error': 'Invalid Email or Password.'}
            return Response(content)





