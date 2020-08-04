from django.db.models import Q
from django.shortcuts import render, redirect
#from passlib.hash import pbkdf2_sha256
from .forms import UserForm, SearchForm
from .models import Photos, UserDetails, UserImages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.postgres.search import SearchVector
from django.contrib.auth.models import User,auth
from django.contrib import messages

# home page function call
def index(request):
    try:
        images = Photos.objects.all()
        lifestyle_ratio,floral_ratio,fashion_ratio,nature_ratio = skills()
    except Exception as e:
        print('Exception occures ',e)

    return render(request, 'index.html', {'images': images, 'name': 'Sudhansu Sekhar',
                                              'lifestyle_ratio': lifestyle_ratio,
                                              'floral_ratio': floral_ratio,
                                              'fashion_ratio': fashion_ratio,
                                              'nature_ratio': nature_ratio})

# All image categories skill areas function call
def skills():
    try:
        images = Photos.objects.all()
        nature_count = list(Photos.objects.filter(img_category='Nature'))
        floral_count = list(Photos.objects.filter(img_category='Floral'))
        lifestyle_count = list(Photos.objects.filter(img_category='Lifestyle'))
        fashion_count = list(Photos.objects.filter(img_category='Fashion'))

        nature = float((len(nature_count) / len(images)) * 100)*2
        nature_ratio = "{:.2f}".format(nature)
        fashion = float((len(fashion_count) / len(images)) * 100)*2
        fashion_ratio = "{:.2f}".format(fashion)
        floral = float((len(floral_count) / len(images)) * 100)*2
        floral_ratio = "{:.2f}".format(floral)
        lifestyle = float((len(lifestyle_count) / len(images)) * 100)*2
        lifestyle_ratio = "{:.2f}".format(lifestyle)
    except Exception as e:
        print('Exception occures ', e)

    return lifestyle_ratio,floral_ratio,fashion_ratio,nature_ratio

# About the photographer page function call
def about_artist(request):
    try:
        lifestyle,floral,fashion,nature = skills()
    except Exception as e:
        print('Exception occures ', e)

    return render(request,'about.html',{'name':'Sudhansu Sekhar',
                                        'lifestyle_ratio':lifestyle,
                                        'floral_ratio':floral,
                                        'fashion_ratio':fashion,
                                        'nature_ratio':nature})
 # Paginations function call in all portfollios
def portfolio_func(request):
    try:
        images = Photos.objects.all()
        paginator = Paginator(images,18)
        page_number = request.GET.get('page')
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return page_obj

# portfolio1 page function call
def portfolio1(request):
    try:
        portfolio_func(request)
    except Exception as e:
        print('Exception occures ', e)
    return render(request,'portfolio1.html',{'page_obj':portfolio_func(request)})

# portfolio2 page function call
def portfolio2(request):
    try:
        portfolio_func(request)
    except Exception as e:
        print('Exception occures ', e)

    return render(request,'portfolio2.html',{'page_obj':portfolio_func(request)})

# portfolio3 page function call
def portfolio3(request):
    try:
        portfolio_func(request)
    except Exception as e:
        print('Exception occures ', e)
    return render(request,'portfolio3.html',{'page_obj':portfolio_func(request)})

#function call for contact link
def contact(request):

    return render(request, 'contact.html')

# Function for search
def search(request):
    try:
        search_data = request.GET["search_input"]

        photos_search = Photos.objects.annotate(search=SearchVector('img_category', 'img_desc')).filter(search=search_data)
        search_count = len(photos_search)
    except Exception as e:
        print('Exception occures ', e)
    return render(request,'search.html',{'search_value':photos_search,'search_count':search_count,'search_data':search_data})

# Function call for user registration
def register(request):
    try:
        images = Photos.objects.all()
        if request.method == "POST":
           username = request.POST['username']
           first_name = request.POST['first_name']
           last_name = request.POST['last_name']
           email = request.POST['email']
           password1 = request.POST['password1']
           password2 = request.POST['password2']

           if password1 == password2:
               if User.objects.filter(username=username).exists():
                   messages.info(request,'username already exists')
                   return redirect('contact')
               elif User.objects.filter(email=email).exists():
                   messages.info(request,'email ID already exists')
                   return redirect('contact')
               else:
                   user = User.objects.create_user(username=username,
                                                   first_name=first_name,
                                                   last_name=last_name,
                                                   email=email,
                                                   password=password1)
                   user.save()
                   #messages.info(request,'user created')
                   return render(request, 'login_form.html', {'images':images,'user':user})
           else:
               messages.info(request,'password not matching')
               return redirect('contact')
        else:
            return redirect('contact')
    except Exception as e:
        print('Exception occures ', e)

def googleLogin(request):
    try:
       images = Photos.objects.all()
       if request.method == 'POST':
           gUserName = request.POST['gUser']
           gUserEmail = request.POST['gEmail']
           print('google user-----',gUserName)
           print('google email -----',gUserEmail)
    except Exception as e:
        print('Exception occures ', e)
    return render(request, 'login_home.html', {'images': images})

# Function call for user login page
def login(request):
    try:
        images = Photos.objects.all()

        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username,password=password)
            if user is not None:
                auth.login(request,user)
                return render(request,'login_home.html',{'images':images,'user':user})
            else:
                messages.info(request,'Invalid credentials')
                return redirect('login')
        else:
            return render(request, 'login_form.html')
    except Exception as e:
        print('Exception occures ', e)

# Function call for user logout
def logout(request):
    try:
        auth.logout(request)
    except Exception as e:
        print('Exception occures ', e)
    return redirect('/')

# Function call for logged in user after authentication
def login_user(request):
    try:
        images = Photos.objects.all()
        if request.method == "POST":
            user_pic = request.POST['userfile']
            username = request.POST['username']
            first_name = request.POST['firstname']
            last_name = request.POST['lastname']
            email = request.POST['email']
            password = request.POST['password']
            user = UserImages(username=username, password=password, first_name=first_name, last_name=last_name,email=email, user_img=user_pic)

            if user_pic is not None:
                user.save()
                print('user saved')
                messages.info(request,'Thank you for uploading.')
                messages.info(request,'Your request for editing photos will be sent to you in your registered email after 2 to 3 working days.')
                return render(request,'login_home.html',{'images':images})
            else:
                messages.info(request,'Please try to upload a photo and see the changes in it.')
                return redirect('login_home')
        else:
            return redirect('/')
    except Exception as e:
        print('Exception occures ', e)


def message(request):
    try:
        if request.method == "POST":
            images = Photos.objects.all()
            form = UserForm(request.POST)

            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                email = form.cleaned_data['email']
                subject = form.cleaned_data['subject']
                user_message = form.cleaned_data['user_message']

                #enc_password = pbkdf2_sha256.encrypt(password,rounds=120,salt_size=32)
                user = UserDetails(username=username,password=password,first_name=first_name,last_name=last_name,email=email,subject=subject,user_message=user_message)
                user.save()
                print('user created')
            else:
                print('error')
                #raise Http404
        else:
            form = UserForm()
    except Exception as e:
        print('Exception occures ', e)

    return render(request, 'login_form.html',{'images': images,'user':user})
