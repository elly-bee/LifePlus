# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from django.shortcuts import redirect, render,get_object_or_404
from .models import *
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse, reverse_lazy
import random
import random_word
from .forms import *
from django.views.generic import ListView, CreateView,DetailView
from decimal import Decimal
from django.http import JsonResponse
from django.contrib import messages

def whistleblower_user():
    random_word_str = random_word.RandomWords().get_random_word()
    random_number = random.randint(1000, 9999)
    return f"{random_word_str}{random_number}"


#@login_required(login_url="/login/")

def test(request):
    context = {}
    html_template = loader.get_template('home/transactionList.html')
    return HttpResponse(html_template.render(context,request))


def index(request):
    products = Products.objects.all().values(),
    context = {
        'products': products
    }
    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context,request))

def dashboard(request):
    context = {}
    html_template = loader.get_template('home/dashboard.html')
    return HttpResponse(html_template.render(context,request))

@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
    

class UserNode:
    def __init__(self, user, relationship=None):
        self.user = user
        self.relationship = relationship  # Indicates the relationship ('parent', 'child', 'grandchild', ...)
        self.children = []

    def add_child(self, child, relationship=None):
        child_node = UserNode(child, relationship)
        self.children.append(child_node)

    def show_hierarchy(self, depth=0, max_depth=10):
        hierarchy = {
            'user': self.user.username,
            'relationship': self.relationship if self.relationship else 'parent',
            'children': []
        }

        if depth < max_depth:
            for child in self.children:
                hierarchy['children'].append(child.show_hierarchy(depth + 1, max_depth))

        return hierarchy

def fetch_and_add_children(node, max_depth):
    if max_depth > 0:
        children = MyUser.objects.filter(parent=node.user)
        for child in children:
            node.add_child(child, relationship='child')
            fetch_and_add_children(node.children[-1], max_depth - 1)

def create_user(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            
            # Check if user with this username already exists
            if MyUser.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists. Please choose a different username.')
            else:
                user_instance = form.save(commit=False)
                password = form.cleaned_data['password']
                user_instance.set_password(password)

                if request.user.is_authenticated:
                    user_instance.parent = request.user

                user_instance.save()

                if request.user.is_authenticated:
                    parent_node = UserNode(request.user, relationship='parent')
                    children_under_parent = MyUser.objects.filter(parent=request.user)
                    
                    for child in children_under_parent:
                        parent_node.add_child(child, relationship='child')
                        fetch_and_add_children(parent_node.children[-1], max_depth=10)

                    hierarchy_data = parent_node.show_hierarchy(max_depth=10)

                # Redirect to user detail page after successful creation
                return redirect('user_detail',pk=request.user.pk)
        # If form is not valid, re-render the form with errors
    else:
        # Determine which form template to render based on the URL or some condition
        if request.path == '/home/user_detials.html':  # Adjust condition based on actual URL
            form = CreateUserForm()
            template = 'home/user_detials.html'
        else:
            form = CreateUserForm()
            template = 'home/UserRegistration.html'

    return render(request, template, {
        'form': form,
        'recruit': form, })



def user_detail(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user_instance = form.save(commit=False)
            password = form.cleaned_data['password']
            user_instance.set_password(password)

            if request.user.is_authenticated:
                user_instance.parent = request.user
            user_instance.save()

            # Assuming you want to show hierarchy data after successful form submission
            parent_node = UserNode(request.user, relationship='parent')
            children_under_parent = MyUser.objects.filter(parent=request.user)
                
            for child in children_under_parent:
                parent_node.add_child(child, relationship='child')
                fetch_and_add_children(parent_node.children[-1], max_depth=10)

            hierarchy_data = parent_node.show_hierarchy(max_depth=10)
            pk=user_instance.pk
            return redirect(reverse('apps_home:user_create_info', kwargs={'pk': user_instance.pk}))

            """return render(request, 'home/user_detials.html', {
                'hierarchy': hierarchy_data,
                'form': form,
            })"""
        # If form is not valid, render form with errors
    else:
        # GET request handling
        orders = Orders.objects.filter(user=request.user.id).values(
            'order_id',
            'order_date',
            'package_id__package_name',
            'package_id__package_price',
        )

        parent_node = UserNode(request.user, relationship='parent')
        children_under_parent = MyUser.objects.filter(parent=request.user)
        
        for child in children_under_parent:
            parent_node.add_child(child, relationship='child')
            fetch_and_add_children(parent_node.children[-1], max_depth=10)
        
        hierarchy_data = parent_node.show_hierarchy(max_depth=10)
        form = CreateUserForm()  # Initialize form for GET request

        return render(request, 'home/user_detials.html', {
            'hierarchy': hierarchy_data,
            'form': form,
            'orders': orders
        })

def create_user_details(request, pk):
    products = Products.objects.all().values()  # Assuming Products model exists
    user = get_object_or_404(MyUser, pk=pk)  # Retrieve user by primary key
    myAccount = Account.objects.filter(acc_holder=request.user).values('acc_type_id__name','cur_bal')
    form = keyBonusUpdate()
    print(myAccount)
    searched_user = None
    if request.method == 'POST':
        if 'search_button' in request.POST:
            form = keyBonusUpdate(request.POST)
            if form.is_valid():
                keyBonus_username = form.cleaned_data['keyBonus']
                try:
                    searched_user = MyUser.objects.get(username=keyBonus_username)
                except MyUser.DoesNotExist:
                    messages.error(request, f'User with username "{keyBonus_username}" does not exist.')
        elif 'save_button' in request.POST:
            keyBonus_username = request.POST.get('keyBonus_username')
            try:
                searched_user = MyUser.objects.get(username=keyBonus_username)
                user.keyBonus = searched_user
                user.save()
                messages.success(request, f'Key Bonus updated successfully for user "{user.username}".')
            # Redirect to home or appropriate URL
            except MyUser.DoesNotExist:
                messages.error(request, f'User with username "{keyBonus_username}" does not exist.')

    return render(request, 'home/user_details_create.html', {
        'products': products,
        'user': user,
        'form': form,
        'searched_user': searched_user,
        'myAccount': myAccount,
    })
class ProductView(CreateView):
    model = Products
    template_name = 'home/billing.html'
    success_url = reverse_lazy('apps_home:dashboard')
    form_class = CreateProducts 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Combine queryset data from multiple models
        context['product_form'] = CreateProducts()
        context['product_data'] = {
            'products': Products.objects.all().values(),
        }
        return context
    def get_template_names(self):
        if self.request.GET.get('template') == 'alternative':
            return ['home/alternative_billing.html']
        else:
            return [self.template_name]

class ProductDetials(DetailView):
    model = Products
    template_name = 'home/productDetials.html'
    success_url = reverse_lazy('apps_home:dashboard')
    form_class = CreateProducts 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        productID = self.object.pk
        productDetials = Products.objects.filter(product_id=productID).values(
            'bonus__bonus',
            'bonus__occurance__occurrence_type',
            'bonus__percentage',
            'package_name',
            'package_price'
            ),
        print(productDetials)
        # Combine queryset data from multiple models
        context['product_form'] = CreateProducts()
        context['product_data'] = {
            'productsDetail': productDetials
        }
        return context

class ClientProductDetail(DetailView):
    model = Products
    template_name = 'home/productPurchase.html'
    form_class = CreateProducts  # Assuming this is another form class for displaying products

    def post(self, request, *args, **kwargs):
        product = self.get_object()
        user = self.request.user  # Assuming you have authentication set up
        package = product  # Assuming Products model is related to package
        
        order_instance = Orders(
            user=user,
            package=package,
            # Assuming you want to auto-generate order_date
            order_date=timezone.now()  # Import timezone if not already imported
        )
        order_instance.save()
        return redirect('apps_home:user_detail')

    def form_invalid(self, order_form):
        # Handle invalid form submission
        context = self.get_context_data(order_form=order_form)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        productID = product.pk
        productDetails = Products.objects.filter(product_id=productID).values(
            'bonus__bonus',
            'bonus__occurance__occurrence_type',
            'bonus__percentage',
            'package_name',
            'package_price'
        )

        context['product_form'] = CreateProducts()
        context['order_form'] = OrderForm()
        context['product_data'] = {
            'productsDetail': productDetails
        }
        return context
    

class TransactionDetail(DetailView):
    model = Transaction
    template_name = 'home/transactionList.html'
    form_class = CreateProducts  # Assuming this is a form class for some purpose

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        userTran = Transaction.objects.filter(user=user).values()
        
        context['user_trans'] = userTran   # Add user transactions to context
        return context
    