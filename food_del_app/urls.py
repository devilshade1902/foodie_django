from django.urls import path
from .views import restaurant_list,create_restaurant,Restaurant_delete,dish_delete,remove_from_cart,update_cart,create_order, payment_success,RestaurantUpdateView,MenuUpdateView,payment_failed,order_history
from .import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('',restaurant_list.as_view(),name = 'restaurant_list'),
    path('create_restaurant/',create_restaurant.as_view(),name = 'create_restaurant'),
    path('delete_restaurant/<int:pk>/',Restaurant_delete.as_view(),name = 'delete_restaurant'),
    path('delete_dish/<int:pk>/',dish_delete.as_view(),name = 'delete_dish'),
    path('restaurant/<int:restaurant_id>/menu/', views.restaurant_menu, name='restaurant_menu'),
    path('add_to_cart/<int:menu_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/',login_required(views.cart_page), name='cart'),
    path('cart/remove/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:item_id>/', update_cart, name='update_cart'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('about/', views.about, name='aboutus'),
    path('search/', views.searchView, name='search'),
    path("contact/", views.contact, name="contact"),
    path("create-order/", create_order, name="create_order"),
    path("payment-failed/", payment_failed, name="payment_failed"),
    path("payment-success/", payment_success, name="payment_success"),
    path('restaurant/<int:pk>/update/', RestaurantUpdateView.as_view(), name='restaurant_update'),
    path('menu/<int:pk>/update/', MenuUpdateView.as_view(), name='menu_update'),
    path('update-cart/<int:item_id>/', update_cart, name='update_cart'),
    path('order-history/', order_history, name='order_history'),
    ]