from . import views
from django.conf import settings
from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static


urlpatterns = [
    path('', views.LoginAccount.as_view()),
    path('login/', views.LoginAccount.as_view(), name="login"),
    path("register/", views.RegisterAccount.as_view(), name="register"),
    path("logout/", views.logout_page, name="logout"),
    path("profile/", views.UpdateAccount.as_view(), name="profile"),
    path("delete_profile/", views.DeleteAccount.as_view(), name="delete_profile"),
    path("change_password/", views.ChangePasswordAccount.as_view(), name="change_password"),
    path('reset_password/', views.PasswordResetView_main.as_view(template_name='account/password_reset_form.html'),
                       name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='account/password_reset_done.html'),
                       name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='account/password_reset_confirm.html'),
                       name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(
                      template_name='account/password_reset_complete.html'), name='password_reset_complete'),

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #new