from django.urls import path
from . import views
from .views import ContactListAPI, ContactDetailAPI

# ViewSet imports
from rest_framework.routers import DefaultRouter
from .views import ContactViewSet


router = DefaultRouter()
router.register(r'api/v3/contacts', ContactViewSet, basename='contacts')


urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact),
    path('messages/', views.contact_list, name='messages'),
    path('edit/<int:id>/', views.edit_contact, name='edit_contact'),
    path('delete/<int:id>/', views.delete_contact, name='delete_contact'),

    # Function based API
    path('api/contacts', views.contact_api, name='contact_api'),
    path('api/contacts/<int:id>/', views.contact_detail_api),

    # Class based API
    path('api/v2/contacts/', ContactListAPI.as_view(), name='contacts_api_v2'),
    path('api/v2/contacts/<int:id>/', ContactDetailAPI.as_view()),
]

# ViewSet URLs
urlpatterns += router.urls