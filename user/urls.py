
from django.urls import path
from . import views

from user.views import User_View
from user.views import User_Profile_Create_View,All_Doctor_View
from user.views import User_Profile_Updation_View
from user.views import Pet_Update_View
from user.views import Pet_Delete_View
from user.views import All_Appointment_View
from user.views import Appointment_Delete_View
from user.views import CreatePaymentView
from user.views import TemplateView
from .views import ToggleAdoptView
from user.views import Adoption_View,AdopterDetailsView
from .views import AdoptionRequestsView, ToggleAdoptionView
from user.views import User_Orders
from user.views import MyAdoptionRequestsView 
from .views import DeleteAdoptionRequestView


urlpatterns = [
    
    path('user', User_View.as_view(), name='user'),
    path('user_profile', User_Profile_Create_View.as_view(), name='user_profile'),
    path('user_profile_update', User_Profile_Updation_View.as_view(), name='user_profile_update'),
    path('all_doctor', All_Doctor_View.as_view(), name='all_doctor'),
    path('pet_update/<int:pk>/', Pet_Update_View.as_view(), name='update_pet'),
    path('pet_delete/<int:pk>/', Pet_Delete_View.as_view(), name='pet_delete'),
    path('book/<int:doctor_id>/', views.book_appointment, name='book_appointment'),
    path('all_appointment', All_Appointment_View.as_view(), name='all_appointment'),
    path('appointment_delete/<int:pk>/', Appointment_Delete_View.as_view(), name='appointment_delete'),
    
    
    path('pay/<int:appointment_id>/', CreatePaymentView.as_view(), name='create_payment'),
    path('success/', TemplateView.as_view(template_name='payment_success.html'), name='appointment_success'),
    path('toggle_adopt/<int:pet_id>/', ToggleAdoptView.as_view(), name='toggle_adopt'),
    path('adoption', Adoption_View.as_view(), name='adoption'),
    path('adopt/<int:pet_id>/', AdopterDetailsView.as_view(), name='adopter_details'),
    
    path('adoption-requests/', AdoptionRequestsView.as_view(), name='adoption_requests'),
    path('toggle-adoption/<int:adopter_id>/', ToggleAdoptionView.as_view(), name='toggle_adoption'),
    path('user_order', User_Orders.as_view(), name='user_order'),
    path('my_adoption_requests/', MyAdoptionRequestsView.as_view(), name='my_adoption_requests'),
    path('delete_adoption_request/<int:pk>/', DeleteAdoptionRequestView.as_view(), name='delete_adoption_request'),
]
