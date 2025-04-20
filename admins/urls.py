
from django.urls import path
from admins.views import Registration_View
from admins.views import Login_View
from admins.views import Logout_View
from admins.views import Admin_View
from admins.views import All_Doctor_Admin_View
from admins.views import Toggle_Doctor_Approval_View
from admins.views import All_Users_View
from admins.views import Groq_View
from admins.views import All_Booking_Admin_View
from admins.views import website_reviews
from admins.views import PasswordResetView, OTPVerificationView, SetNewPasswordView

urlpatterns = [
    
    path('registration/', Registration_View.as_view(), name='registration'),
    path('login/', Login_View.as_view(), name='login'),
    path('logout/', Logout_View.as_view(), name='logout'),
    path('admin/', Admin_View.as_view(), name='admin'),
    path('all_doctor_admin/', All_Doctor_Admin_View.as_view(), name='all_doctor_admin'),
    path('toggle-approval/<int:doctor_id>/', Toggle_Doctor_Approval_View.as_view(), name='toggle_doctor_approval'),
    path('all_users/', All_Users_View.as_view(), name='all_users'),
    path("chatbot/", Groq_View.as_view(), name="chatbot"),
    path("all_booking_admin/", All_Booking_Admin_View.as_view(), name="all_booking_admin"),
    path('reviews/', website_reviews, name='website_reviews'),
    
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('otp-verification/', OTPVerificationView.as_view(), name='otp_verification'),
    path('set-new-password/', SetNewPasswordView.as_view(), name='set_new_password'),
    
]
