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
    print(request.user,'natukodi')
    if request.method == 'POST':
        print(request.POST)
        request.POST._mutable = True  
        request.POST['user'] = request.user
        request.POST._mutable = False
        postForm = PlantForm(request.POST)
        print(postForm)
        formset = ImageFormSet(request.POST, request.FILES,queryset=Images.objects.none())
        print(postForm.is_valid(),formset.is_valid())
        if postForm.is_valid() and formset.is_valid():
            post_form = postForm.save(commit=False)
            print(request.user)
            a = Nursery_Manager.objects.get(user=request.user)
            post_form.user = a
            post_form.save()
            for form in formset.cleaned_data:
                image = form['image']
                photo = Images(plant=post_form, image=image)
                photo.save()
            messages.success(request,"Posted!")
            return HttpResponseRedirect("/")
        else:
            print (postForm.errors, formset.errors,'hi')
    else:
        postForm = PlantForm()
        formset = ImageFormSet(queryset=Images.objects.none())
    return render(request, 'Manager_home.html',{'postForm': postForm, 'formset': formset})



'''
<QueryDict: {'csrfmiddlewaretoken': ['Nwd9ScVY4xlp9jtse78hJNFL8nKTkGVbI6i5yzAp0htsIo1R49TmJoDz164NB6EN'], 'user': ['user', 'user'],
 'price': ['15'],'form-TOTAL_FORMS': ['1'], 'form-INITIAL_FORMS': ['0'], 'form-MIN_NUM_FORMS': ['0'],
 'form-MAX_NUM_FORMS': ['1000'], 'form-0-id': [''], 'submit': ['Submit']}>
<tr><th><label for="id_price">Price:</label></th><td><input type="text" name="price" value="15" maxlength="4" required id="id_price">
<input type="hidden" name="user" value="Manager1" id="id_user"></td></tr>

True True
Manager1'''