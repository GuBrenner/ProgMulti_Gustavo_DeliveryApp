from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from django.contrib.auth.views import logout_then_login
from .forms import LoginForm, MyPasswordChangeForm, MyPasswordResetForm, MySetPasswordForm
urlpatterns = [
    path("",views.home),
    path('about/',views.about, name="about"),
    path('contact/',views.contact, name="contact"),
    path("category/<slug:val>", views.CategoryView.as_view(), name= "category"),
    path("product-detail/<int:pk>", views.ProductDetail.as_view(), name= "product-detail"),
    path("category-title/<val>", views.CategoryTitle.as_view(), name = "category-title"),
    path('profile/', views.ProfileView.as_view(), name= 'profile'),
    path('address/', views.address, name= 'address'),
    path('updateAddress/<int:pk>', views.updateAdress.as_view(), name= 'updateAddress'),
    path('add-to-cart/', views.add_to_cart, name = 'add-to-cart'),
    path('cart/', views.show_cart, name ='showcart'),
    path('checkout/', views.checkout.as_view(), name ='checkout'),
    path('orders/', views.show_orders, name ='orders'),
    path('place-order/', views.place_order, name ='place_order'),


    path('pluscart/', views.plus_cart),
    path('minuscart/', views.minus_cart),
    path('removecart/', views.remove_cart),

    #login e registro no sitema
    path('registration/', views.CustomerRegistrationView.as_view(), name = "customerregistration"),
    path('accounts/login', auth_view.LoginView.as_view(template_name = "app/login.html", authentication_form= LoginForm), name = "login"),
    path('password-reset/', auth_view.PasswordResetView.as_view(template_name = "app/password_reset.html",form_class = MyPasswordResetForm), name = "password_reset"),
    path('passwordchange/', auth_view.PasswordChangeView.as_view(template_name = "app/passwordchange.html", form_class = MyPasswordChangeForm, success_url = '/passwordchangedone'), name = 'passwordchange'),
    path('passwordchangedone/', auth_view.PasswordChangeDoneView.as_view(template_name = 'app/passwordchangedone.html'), name = 'passwordchangedone'),
    path('logout/', views.UserLogoutView.as_view(http_method_names = ['get', 'post', 'options']), name='logout'),

    path('password-reset/done/', auth_view.PasswordResetDoneView.as_view(template_name = "app/password_reset_done.html"), name = "password_reset_done"),
    path('password-reset-confirm/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(template_name = "app/password_reset_confirm.html", form_class = MySetPasswordForm), name = "password_reset_confirm"),
    path('password-reset-complete/', auth_view.PasswordResetCompleteView.as_view(template_name = "app/password_reset_complete.html"), name = "password_reset_complete"),


]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)