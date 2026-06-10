from django.urls import path
from . import views

urlpatterns = [
    
    path('dashboard/', views.dashboard, name='dashboard'),
    path('market/', views.market_list, name='market'),   
    # path('market/', include('market.urls')),
    path('cart/', views.cart_view, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('add/<int:crop_id>/', views.add_to_cart, name='add_to_cart'),

    path('recommendation/', views.recommendation, name='recommendation'),
    path('maps/', views.maps, name='maps'),
    path('learning/', views.learning, name='learning'),
    path('profit-loss/', views.profit_loss, name='profit_loss'),
    path('api/recommend-crop/', views.recommend_crop_api, name='recommend_crop_api'),
]
