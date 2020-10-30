from django.contrib.auth import login, logout,authenticate
from django.shortcuts import redirect, render
from django.contrib import messages
from django.views.generic import CreateView
from .forms import CustomerSignUpForm, Nursery_manager_SignUpForm
from django.contrib.auth.forms import AuthenticationForm
from .models import User,Customer,Nursery_Manager,Plants,Images
from .forms import PlantForm,ImageForm
from django.http import HttpResponse, HttpResponseRedirect
from django.forms import formset_factory,modelformset_factory
from django.template import RequestContext
from Accounts import models

def register(request):
    return render(request, 'register.html')

class customer_register(CreateView):
    model = User
    form_class = CustomerSignUpForm
    template_name = 'customer_register.html'
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return render(self.request,'Customer_home.html')

class manager_register(CreateView):
    model = User
    form_class = Nursery_manager_SignUpForm
    template_name = 'manager_register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('post')

def login_request(request):
    if request.method=='POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None :
                login(request,user)
                #print(user)
                a = User.objects.get(username=user)
                #print(a.is_customer)
                if a.is_customer:
                    x = Customer.objects.all()
                    return render(request,'Customer_home.html')
                if a.is_manager:
                    x = Nursery_Manager.objects.all()
                    return redirect('post')
            else:
                messages.error(request,"Invalid username or password")
        else:
                messages.error(request,"Invalid username or password")
    return render(request, 'login.html',
    context={'form':AuthenticationForm()})

def logout_view(request):
    logout(request)
    return redirect('/')


def homepage(request):
    print(request)
    context={'text':'You are logged in thats y u r seeing this'}
    return render(request,'Customer_home.html',context)

def landingpage(request):
    return render(request,'landingpage.html')



def post(request):
    ImageFormSet = modelformset_factory(Images,form=ImageForm, extra=1)
    if request.method == 'POST':
        request.POST._mutable = True  
        request.POST['user'] = request.user
        request.POST._mutable = False
        postForm = PlantForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES,queryset=Images.objects.none())
        if postForm.is_valid() and formset.is_valid():
            post_form = postForm.save(commit=False)
            a = Nursery_Manager.objects.get(user=request.user)
            post_form.user = a
            post_form.save()
            for form in formset.cleaned_data:
                image = form['image']
                photo = Images(plant=post_form, image=image)
                photo.save()
            messages.success(request,"Posted!")
            return redirect("post")
        else:
            print (postForm.errors, formset.errors)
    else:
        postForm = PlantForm()
        formset = ImageFormSet(queryset=Images.objects.none())
    a = Nursery_Manager.objects.get(user=request.user)
    plants = Plants.objects.filter(user=a)
    k = []
    for i in plants:
        if Images.objects.filter(pk=i.id):
            k.append(i.id)
    print(k)
    images = Images.objects.filter(pk__in=k)
    print(images)
    for i in images:
        print(i.id)
    return render(request, 'Manager_home.html',{'postForm': postForm, 'formset': formset,'plants':plants,'images':images})


def edit(request,key):
    ImageFormSet = modelformset_factory(Images,form=ImageForm, extra=1)
    post = Plants.objects.filter(pk=key).first()
    if request.method == 'POST':
        request.POST._mutable = True  
        request.POST['user'] = request.user
        request.POST._mutable = False
        postForm = PlantForm(request.POST,instance=post)
        #imageForm = ImageForm(request.POST,instance=post)
        formset = ImageFormSet(request.POST, request.FILES)
        #print(formset)
       # v = Images.objects.filter(plant=post)
        #print(v)
        if postForm.is_valid() and formset.is_valid():
            post_form = postForm.save(commit=False)
            a = Nursery_Manager.objects.get(user=request.user)
            post_form.user = a
            post_form.save()
            for form in formset.cleaned_data:
                image = form['image']
                print(image)
                print(post_form.id,key)
                photo = Images(id=post_form.id, plant=post_form,image=image)
                photo.save()
            messages.success(request,"Posted!")
            return redirect("post")
        else:
            print (postForm.errors, formset.errors)
    else:
        postForm = PlantForm()
        formset = ImageFormSet(queryset=Images.objects.none())
    return render(request, 'edit.html',{'postForm': postForm, 'formset': formset})


def delete(request,key,key1):
    Images.objects.filter(id=key).delete()
    Plants.objects.filter(pk=key1).delete()
    return render(request,'Manager_home.html')


def upload(request):
    ImageFormSet = modelformset_factory(Images,form=ImageForm, extra=1)
    if request.method == 'POST':
        request.POST._mutable = True  
        request.POST['user'] = request.user
        request.POST._mutable = False
        postForm = PlantForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES,queryset=Images.objects.none())
        if postForm.is_valid() and formset.is_valid():
            post_form = postForm.save(commit=False)
            a = Nursery_Manager.objects.get(user=request.user)
            post_form.user = a
            post_form.save()
            for form in formset.cleaned_data:
                image = form['image']
                photo = Images(plant=post_form, image=image)
                photo.save()
            messages.success(request,"Posted!")
            return redirect("post")
        else:
            print (postForm.errors, formset.errors)
    else:
        postForm = PlantForm()
        formset = ImageFormSet(queryset=Images.objects.none())
    return render(request, 'Manager_home1.html',{'postForm': postForm, 'formset': formset})
