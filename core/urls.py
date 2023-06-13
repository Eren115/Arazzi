from django.urls import path
from .views import frontpage, gallery, productPage, checkoutPage, success, addToCart, cc, removeFromCart, rem, csn

urlpatterns = [
    path('', frontpage, name="frontpage"),
    path('gallery/', gallery, name="gallery"),
    path('checkout/', checkoutPage, name="checkout"),
    path('addToCart/<slug:slug>/', addToCart, name="addToCart"),
    path('success/', success, name="success"),
    path('rem/', rem, name="rem"),
    path('cc/<slug:slug>/', cc, name="cc"),
    path('csn/', csn, name="csn"),
    path('removeFromCart/<slug:slug>/', removeFromCart, name="removeFromCart"),
    path('<slug:slug>/', productPage, name="productPage"),
]