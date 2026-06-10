# views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse

from .models import Crop, CartItem

import joblib
import numpy as np

# Mapping numeric labels back to crop names
CROP_LABELS = {
    0: 'rice',
    1: 'maize',
    2: 'chickpea',
    3: 'kidneybeans',
    4: 'pigeonpeas',
    5: 'mothbeans',
    6: 'mungbean',
    7: 'blackgram',
    8: 'lentil',
    9: 'pomegranate',
    10: 'banana',
    11: 'mango',
    12: 'grapes',
    13: 'watermelon',
    14: 'muskmelon',
    15: 'apple',
    16: 'orange',
    17: 'papaya',
    18: 'coconut',
    19: 'cotton',
    20: 'jute',
    21: 'coffee',
}

# ----------------------------
# Dashboard and Sub-app pages
# ----------------------------

def dashboard(request):
    return render(request, 'dashboard.html')


def recommendation(request):
    return render(request, 'subapps/recommendation.html')


def maps(request):
    return render(request, 'subapps/maps.html')


def learning(request):
    return render(request, 'subapps/learning.html')


def profit_loss(request):
    return render(request, 'subapps/profit_loss.html')


# ----------------------------
# Marketplace (E-commerce)
# ----------------------------

def market_list(request):
    crops = Crop.objects.order_by('-created_at')[:20]
    return render(request, 'market/list.html', {'crops': crops})


@require_POST
@login_required(login_url='login')  # change 'login' if your URL name is different
def add_to_cart(request, crop_id):
    crop = get_object_or_404(Crop, id=crop_id)
    qty = int(request.POST.get('quantity', 1))

    # each user has their own cart items
    item, _created = CartItem.objects.get_or_create(user=request.user, crop=crop)
    item.quantity = item.quantity + qty
    item.save()

    return redirect('cart')


@login_required(login_url='login')
def cart_view(request):
    items = (
        CartItem.objects
        .filter(user=request.user)
        .select_related('crop')
    )
    subtotal = sum(i.quantity * i.crop.price for i in items)

    return render(request, 'market/cart.html', {
        'items': items,
        'subtotal': subtotal,
    })


@login_required(login_url='login')
def checkout(request):
    items = (
        CartItem.objects
        .filter(user=request.user)
        .select_related('crop')
    )
    subtotal = sum(i.quantity * i.crop.price for i in items)
    payment_methods = ['Credit/Debit Card', 'UPI/Pay', 'Cash on Delivery (Mock)']

    return render(request, 'market/checkout.html', {
        'items': items,
        'subtotal': subtotal,
        'payment_methods': payment_methods,
    })


# ----------------------------
# API endpoint for Crop Recommendation
# ----------------------------

def load_crop_model():
    if not hasattr(load_crop_model, "model"):
        load_crop_model.model = joblib.load("ml_model/xgboost.pkl")
    return load_crop_model.model


def recommend_crop_api(request):
    try:
        N = float(request.GET.get("N"))
        P = float(request.GET.get("P"))
        K = float(request.GET.get("K"))
        temperature = float(request.GET.get("temperature"))
        humidity = float(request.GET.get("humidity"))
        ph = float(request.GET.get("ph"))
        rainfall = float(request.GET.get("rainfall"))

        features = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
        model = load_crop_model()
        pred = model.predict(features)
        pred_label = int(pred[0])  # numeric label
        crop_name = CROP_LABELS.get(pred_label, f"Unknown ({pred_label})")

        return JsonResponse({"recommended_crop": crop_name})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
