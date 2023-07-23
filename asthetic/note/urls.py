from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name="home"),
    path('download_section/<str:pk>/',views.download_section,name="download_section"),
    path('login',views.loginPage,name="login"),
    path('register',views.registerPage,name="register"),
    path('logout',views.logoutUser,name="logout"),
    path('createNote',views.createNote,name="create-note"),
    path('logout',views.logoutUser,name="logout"),
    path('profile/<str:pk>/',views.profilePage,name="profile"),
    path('catagories',views.Catagories,name="catagories"),
    path('semester/<str:pk>/',views.semester,name="semester"),
    path('cart',views.Cart,name="cart"),
    path('checkout',views.checkout,name="checkout"),
    path('update_item/', views.updateItem, name="update_item"), 
    path('process_order/',views.processOrder,name="process_order")  

]