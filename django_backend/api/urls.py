from django.urls import path
from .views import *
app_name="api"

from rest_framework_simplejwt import views as jwt_views

urlpatterns = [

    path('', HelloView.as_view(), name='hello'),
    path('outlet/', OutletList.as_view()),
    path('outlet/add/', createOutletView.as_view()),
    path('outlet/category/', OutletCategoryListView.as_view()),
    path('product/', ProductList.as_view()),
    path('login/', LoginView.as_view()),
    path('audit/', auditSaveView.as_view()),

    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', jwt_views.TokenVerifyView.as_view(), name='token_verify'),


]