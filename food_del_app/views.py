from .models import Restaurants,Menus,Cart
from django.urls import reverse_lazy , reverse
import razorpay
from django.conf import settings
from django.views.generic import ListView, UpdateView
from django.views.generic.edit import CreateView,DeleteView
from .forms import MenuForm,ContactForm
from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import FoodieSignupForm, RestaurantForm
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
class create_restaurant(CreateView):
    model =  Restaurants
    template_name = 'create_restaurant.html'
    fields = [  'name','address','phone_no','image_url']
    success_url = reverse_lazy('restaurant_list')
    

class restaurant_list(ListView):
    model = Restaurants
    template_name = 'restaurant_list.html'
    context_object_name = 'restaurants'
    
    
class Restaurant_delete(DeleteView):
    model = Restaurants
    template_name = 'restaurant_delete.html'
    success_url = reverse_lazy('restaurant_list')
    
class dish_delete(DeleteView):
    model = Menus
    template_name = 'dish_delete.html'
    success_url = reverse_lazy('restaurant_list')

def about(request):
    return render(request, 'aboutus.html')
    
def restaurant_menu(request,restaurant_id):
    restaurant = get_object_or_404(Restaurants, id=restaurant_id)
    menus = Menus.objects.filter(restaurant_id=restaurant)
    return render(request, 'restaurant_menu.html', {'restaurant': restaurant, 'menus': menus})
    
def restaurant_menu(request, restaurant_id):
    restaurant = get_object_or_404(Restaurants, id=restaurant_id)
    menus = Menus.objects.filter(restaurant_id=restaurant)
    form = MenuForm()

    if request.method == 'POST':
        form = MenuForm(request.POST, request.FILES)
        if form.is_valid():
            menu_item = form.save(commit=False)
            menu_item.restaurant_id = restaurant
            menu_item.save()
            return redirect('restaurant_menu', restaurant_id=restaurant.id)

    return render(request, 'restaurant_menu.html', {'restaurant': restaurant, 'menus': menus, 'form': form})

class RestaurantUpdateView(UpdateView):
    model = Restaurants
    form_class = RestaurantForm
    template_name = 'restaurant_update.html'  # Ensure this template exists
    success_url = '/'

class MenuUpdateView(UpdateView):
    model = Menus
    form_class = MenuForm
    template_name = 'dish_update.html'
    
    def form_valid(self, form):
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('restaurant_menu', kwargs={'restaurant_id': self.object.restaurant_id.id})

@login_required(login_url='/foodie/login/')
def cart_page(request):
     if not request.user.is_authenticated:
        messages.warning(request, "First login to access the cart.")
        return redirect(f'/foodie/login/?next=/foodie/cart/')  # Redirect to login with next parameter
    
     cart_items = Cart.objects.filter(user=request.user)
     total_amount = sum(item.total_price() for item in cart_items)
     return render(request, 'cart.html', {'cart_items': cart_items, 'total_amount': total_amount})



@login_required
def add_to_cart(request, menu_id):
    menu_item = get_object_or_404(Menus, id=menu_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, menu_item=menu_item)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, f"{menu_item.name} added to cart!")  # Success message
    return redirect('restaurant_menu', restaurant_id=menu_item.restaurant_id.id)


def signup(request):
    if request.method == 'POST':
        form = FoodieSignupForm(request.POST)
        if form.is_valid():
            foodie = form.save(commit=False)
            foodie.username = form.cleaned_data['email']  
            foodie.set_password(form.cleaned_data['password'])  
            foodie.save()
            messages.success(request, "Account created successfully!")
            return redirect('login')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = FoodieSignupForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    next_url = request.GET.get('next', 'restaurant_list')  # Default redirect

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect(next_url)  # Redirect user after login
        else:
            messages.error(request, "Invalid email or password.")

    return render(request, 'login.html', {'next': next_url})



def logout_view(request):
    logout(request)
    return redirect('login')


@login_required(login_url='/foodie/login/')
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(Cart, id=item_id, user=request.user)
    cart_item.delete()
    return redirect('cart')

@login_required(login_url='/foodie/login/')
def update_cart(request, item_id):
    cart_item = get_object_or_404(Cart, id=item_id, user=request.user)
    if request.method == 'POST':
        new_quantity = request.POST.get('quantity')
        if new_quantity and int(new_quantity) > 0:
            cart_item.quantity = int(new_quantity)
            cart_item.save()
        else:
            cart_item.delete()  # Remove item if quantity is set to 0
    return redirect('cart')




def searchView(request):
    query = request.GET.get('q', '')
    if query:
        restaurants = Restaurants.objects.filter(name__icontains=query)
    else:
        restaurants = Restaurants.objects.none()  # Ensure it returns an empty queryset

    return render(request, 'search.html', {'restaurants': restaurants, 'query': query})


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            messages.success(request, "Your message has been sent successfully!")
            return redirect("contact")  
    else:
        form = ContactForm()

    return render(request, "contact.html", {"form": form})




def create_order(request):
    if request.method == "POST":
        address = request.POST.get('address1', '').strip()
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        cart_items = Cart.objects.filter(user=request.user)
        total_amount = sum(float(item.total_price()) for item in cart_items)  

        if total_amount <= 0:
            return JsonResponse({"error": "Cart total must be greater than zero."}, status=400)

        print("Session data:", request.session.items())
        
        request.session['address1'] = address
        request.session.modified = True 
        
        
        order_data = {
            "amount": int(total_amount * 100),  
            "currency": "INR",
            "payment_capture": 1
        }

        try:
            order = client.order.create(order_data)
        except razorpay.errors.BadRequestError as e:
            return JsonResponse({"error": str(e)}, status=400)

        return render(request, "razorpay_payment.html", {
            "order": order,
            "razorpay_key_id": settings.RAZORPAY_KEY_ID,
            "razorpay_order_id": order["id"],
            "total_amount": total_amount
        })

    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt
def payment_success(request):
    total_amount = request.GET.get('total_amount', 0)

    address1 = request.session.get('address1', "Not Provided") 
    
    Cart.objects.filter(user=request.user).delete()

    return render(request, 'payment_success.html', {
        'total_amount': total_amount,
        'address1': address1,
    })