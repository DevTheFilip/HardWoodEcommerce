from django.urls import path
from . import views


from django.contrib.auth import views as auth_views




urlpatterns = [
    path('register', views.register, name='register'),


    #email vericication URL's

    path('email-verification/<str:uidb64>/<str:token>/',views.email_verification,name='email-verification'),

    path('email-verification-sent',views.email_verification_sent,name='email-verification-sent'),

    path('email-verification-success',views.email_verification_success,name='email-verification-success'),

    path('email-verification-failed',views.email_verification_failed,name='email-verification-failed'),

    #Login/log-out
    path('my-login',views.my_login,name='my-login'),

    path('user-logout',views.user_logout,name='user-logout'),


    #Dashboard

    path('dashboard',views.dashboard,name='dashboard'),


    path('profile-management',views.profile_management,name='profile-management'),
    path('delete-account',views.delete_account,name='delete-account'),



    #Password management urls views


    #1) Subbmit our email form
    path('reset_password', auth_views.PasswordResetView.as_view(template_name="account/password/password-reset.html"),name='reset_password'),

    #2) Succes message stating that password email was sent
    path('reset_password_sent',auth_views.PasswordResetDoneView.as_view(template_name="account/password/password-reset-sent.html"),name='password_reset_done'),

    #3)Password reset link
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="account/password/password-reset-form.html"),name='password_reset_confirm'),

    #4) Password reset complete
    path('reset_password_complete',auth_views.PasswordResetCompleteView.as_view(template_name="account/password/password-reset-competed.html"),name='password_reset_complete'),

    #shipping

    path('shipping-address',views.manage_shipping,name='shipping-address'),

    #Track-orders

    path('track-orders',views.track_orders,name='track-orders'),

    path('manage-orders/', views.manage_orders, name='manage-orders'),

    path('admin/delete-order/<int:order_id>/', views.delete_order, name='delete-order'),



]