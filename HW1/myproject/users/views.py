from django.shortcuts import render,redirect
from . import models
from .forms import UserForm, RegisterForm, DriverForm, RideRequestForm, SharerForm
from django.db.models import Q

def index(request):
    #if not request.session.get('is_login', None):
        #return redirect('/login/')
    return render(request,'users/index.html')

def login(request):
    if request.session.get('is_login',None):#不允许重复登录
        return redirect('/index')

    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = models.User.objects.get(name=username)
                if user.password == password:
                    request.session['is_login'] = True      #往session字典内写入用户状态和字典
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    request.session['is_driver'] = user.is_driver
                    return redirect('/index/')
                else:
                    message = "密码不正确！"
            except:
                message = "用户不存在！"
        return render(request, 'users/login.html', locals())

    login_form = UserForm()
    return render(request, 'users/login.html', locals())


def register(request):
    if request.session.get('is_login', None):
        # 登录状态不允许注册。你可以修改这条原则！
        return redirect("/index/")
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'users/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:  # 用户名唯一
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, 'users/register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:  # 邮箱地址唯一
                    message = '该邮箱地址已被注册，请使用别的邮箱！'
                    return render(request, 'users/register.html', locals())

                # 当一切都OK的情况下，创建新用户
                request.session['is_driver'] = False
                new_user = models.User.objects.create()
                new_user.name = username
                new_user.password = password1
                new_user.email = email
                new_user.save()
                return redirect('/login/')  # 自动跳转到登录页面
    register_form = RegisterForm()
    return render(request, 'users/register.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/index/")
    request.session.flush()
    # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect("/index/")

def base(request):
    return render(request, 'users/base.html')

def driver(request):#driver resgitration
    if not request.session.get('is_login', None):
        # 没有登录不允许注册车辆。你可以修改这条原则！
        return redirect("/index/")

    if request.method == "POST":
        driver_form = DriverForm(request.POST)
        message = "请检查填写的内容！"
        if driver_form.is_valid():  # 获取数据
            vehicle_type = driver_form.cleaned_data['vehicle_type']
            license_number = driver_form.cleaned_data['license_number']
            max_number_of_passengers = driver_form.cleaned_data['max_number_of_passengers']
            special_request = driver_form.cleaned_data['special_request']
            # find the cur_user
            cur_user = models.User.objects.get(id = request.session['user_id'])
            if (cur_user.is_driver):
                message = 'already register as a driver'
                return render(request, 'users/index.html', locals())
                
                # 当一切都OK的情况下，创建新用户
            #new_car = models.Vehicle.objects.create()
            new_car = models.Vehicle()
            new_car.user = cur_user
            cur_user.is_driver = True
            request.session['is_driver'] = cur_user.is_driver
            new_car.vehicle_type = vehicle_type
            new_car.license_number = license_number
            new_car.max_number_of_passengers = max_number_of_passengers
            new_car.special_request = special_request
            new_car.save()
            cur_user.save()
            return redirect('/index/')  # 自动跳转到主页

    driver_form = DriverForm()
    return render(request, 'users/driver.html', locals())

def driverUpdate(request):#driver resgitration
    if not request.session.get('is_login', None):
        # 没有登录不允许注册车辆。你可以修改这条原则！
        return redirect("/index/")
    if request.method == "POST":
        driver_form = DriverForm(request.POST)
        message = "请检查填写的内容！"
        if driver_form.is_valid():  # 获取数据
            vehicle_type = driver_form.cleaned_data['vehicle_type']
            license_number = driver_form.cleaned_data['license_number']
            max_number_of_passengers = driver_form.cleaned_data['max_number_of_passengers']
            special_request = driver_form.cleaned_data['special_request']
            # find the cur_user
            cur_user = models.User.objects.get(id = request.session['user_id'])
                
                # 当一切都OK的情况下，创建新用户
            #new_car = models.Vehicle.objects.create()
            cur_car = cur_user.vehicle
            cur_car.vehicle_type = vehicle_type
            cur_car.license_number = license_number
            cur_car.max_number_of_passengers = max_number_of_passengers
            cur_car.special_request = special_request
            cur_car.save()
            return redirect('/index/')  # 自动跳转到主页
    driver_form = DriverForm()    
    return render(request, 'users/driverUpdate.html', locals())
    



def rideRequest(request):
    if request.method == "POST":
        ride_form = RideRequestForm(request.POST)
        if ride_form.is_valid():  # 获取数据
            destination = ride_form.cleaned_data['destination']
            arrival_time = ride_form.cleaned_data['arrival_time']
            number_of_total_passengers = ride_form.cleaned_data['number_of_total_passengers']
            vehicle_type = ride_form.cleaned_data['vehicle_type']
            is_shared = ride_form.cleaned_data['is_shared']
            # create the ride
            cur_ride = models.Ride()
            cur_ride.owner = request.session['user_name']
            cur_ride.owner_number = number_of_total_passengers
            cur_ride.destination = destination
            cur_ride.arrival_time_early = arrival_time
            cur_ride.current_passenger_num = number_of_total_passengers
            cur_ride.vehicle_type = vehicle_type
            cur_ride.is_shared = is_shared
            cur_ride.save()
            return redirect('/index/')  # 自动跳转到主页

    ride_form = RideRequestForm()    
    return render(request, 'users/rideRequest.html', locals())

def sharerSearch(request):
    if request.method == "POST":
        sharer_form = SharerForm(request.POST)
        if sharer_form.is_valid():  # 获取数据
            destination = sharer_form.cleaned_data['destination']
            arrival_early = sharer_form.cleaned_data['arrival_early']
            arrival_late = sharer_form.cleaned_data['arrival_late']
            number_of_passengers = sharer_form.cleaned_data['number_of_passengers']

            # create the ride
            cur_user_id = request.session['user_id']
            cur_user = models.User.objects.get(id = cur_user_id)
            ride_list = models.Ride.objects.filter(\
                Q(destination = destination) & Q(arrival_time_early__gte=arrival_early)\
                 & Q(arrival_time_early__lte=arrival_late) & Q(is_shared=True) \
                 & Q(is_confirmed = False) & Q(is_complete = False) & ~Q(owner = cur_user) \
                 & Q(has_shared = False)
            )

            return render(request, 'users/sharerResult.html', locals())
            #return redirect('/index/')  # 自动跳转到主页

    sharer_form = SharerForm()    
    return render(request, 'users/sharerSearch.html', locals())

def sharerConfirm(request, id, num):#
    ride = models.Ride.objects.get(id = id)
    cur_user_id = request.session['user_id']
    cur_user= models.User.objects.get(id = cur_user_id)
    ride.sharer.add(cur_user)
    ride.has_shared = True
    ride.current_passenger_num = ride.owner_number + num
    ride.save()
    return render(request, 'users/index.html')


def driverSearch(request):
    cur_user_id = request.session['user_id']
    cur_user = models.User.objects.get(id = cur_user_id)
    cur_vehicle = cur_user.vehicle
    ride_list = models.Ride.objects.filter(\
            Q(current_passenger_num__lte = cur_vehicle.max_number_of_passengers) \
            & Q(is_confirmed = False) & Q(is_complete = False) \
            & ~Q(owner = cur_user) \
            & ~Q(sharer__name = cur_user)
            & (Q(vehicle_type = '') | Q(vehicle_type = cur_vehicle.vehicle_type))
    )

    return render(request, 'users/driverResult.html', locals())


def driverConfirm(request, id):#
    ride = models.Ride.objects.get(id = id)
    cur_user_id = request.session['user_id']
    cur_user= models.User.objects.get(id = cur_user_id)
    ride.driver = cur_user.name
    ride.vehicle_type = cur_user.vehicle.vehicle_type
    #ride.current_passenger_num = ride.current_passenger_num + num
    ride.is_confirmed = True
    ride.save()
    return render(request, 'users/index.html')

def ownerView(request):
    cur_user_id = request.session['user_id']
    cur_user = models.User.objects.get(id=cur_user_id)
    ride_list = models.Ride.objects.filter(Q(owner=cur_user.name) & Q(is_complete=False))

    return render(request, 'users/ownerView.html', locals())

def rideDetail(request, id):
    ride = models.Ride.objects.get(id = id)
    user = models.User.objects.get(name = ride.owner)
    sharers = ride.sharer.all()
    return render(request, 'users/rideDetail.html', locals())





def rideOwnerEdit(request, id):
    ride = models.Ride.objects.get(id = id)
    sharers = ride.sharer.all()
    if (sharers.exists()):
        return rideOwnerEdit_hasS(request, id)
    else:
        return rideOwnerEdit_noS(request, id)


def rideOwnerEdit_noS(request, id):
    if request.method == "POST":
        print(1234)
        ride_form = RideRequestForm(request.POST)
        if ride_form.is_valid():  # 获取数据
            destination = ride_form.cleaned_data['destination']
            arrival_time = ride_form.cleaned_data['arrival_time']
            number_of_total_passengers = ride_form.cleaned_data['number_of_total_passengers']
            vehicle_type = ride_form.cleaned_data['vehicle_type']
            is_shared = ride_form.cleaned_data['is_shared']
            # create the ride
            cur_ride = models.Ride.objects.get(id=id)
            cur_ride.destination = destination
            cur_ride.arrival_time_early = arrival_time
            cur_ride.current_passenger_num = number_of_total_passengers
            cur_ride.vehicle_type = vehicle_type
            cur_ride.is_shared = is_shared
            cur_ride.save()
            return redirect('/index/')  # 自动跳转到主页

    ride_form = RideRequestForm()    
    return render(request, 'users/rideOwnerEdit_noS.html', locals())



def rideOwnerEdit_hasS(request, id):
    if request.method == "POST":
        ride_form = RideRequestForm(request.POST)
        if ride_form.is_valid():  # 获取数据
            number_of_total_passengers = ride_form.cleaned_data['number_of_total_passengers']
            vehicle_type = ride_form.cleaned_data['vehicle_type']
            # create the ride
            cur_ride = models.Ride.objects.get(id=id)
            cur_ride.current_passenger_num = number_of_total_passengers
            cur_ride.vehicle_type = vehicle_type
            cur_ride.save()
            return redirect('/index/')  # 自动跳转到主页

    ride_form = RideRequestForm()    
    return render(request, 'users/rideOwnerEdit_hasS.html', locals())


def rideOwnerCancel(request, id):
    models.Ride.objects.get(id=id).delete()
    return redirect('/index/')


def sharerView(request):
    cur_user_id = request.session['user_id']
    cur_user = models.User.objects.get(id=cur_user_id)
    #有待测试
    ride_list = models.Ride.objects.filter(Q(sharer=cur_user) & Q(is_complete=False))

    return render(request, 'users/sharerView.html', locals())

def sharerDetail(request, id):
    ride = models.Ride.objects.get(id = id)
    user = models.User.objects.get(name = ride.owner)
    sharers = ride.sharer.all()
    return render(request, 'users/sharerDetail.html', locals())

def sharerCancel(request, id):
    ride = models.Ride.objects.get(id=id)
    ride.has_shared = False
    ride.current_passenger_num = ride.owner_number
    cur_user_id = request.session['user_id']
    cur_user = models.User.objects.get(id=cur_user_id)
    ride.sharer.remove(cur_user)
    ride.save()
    return redirect('/index/')


def driverView(request):
    cur_user_id = request.session['user_id']
    cur_user = models.User.objects.get(id=cur_user_id)
    #有待测试
    ride_list = models.Ride.objects.filter(Q(driver=cur_user.name) & Q(is_complete=False))

    return render(request, 'users/driverView.html', locals())

def driverDetail(request, id):
    ride = models.Ride.objects.get(id = id)
    user = models.User.objects.get(name = ride.owner)
    sharers = ride.sharer.all()
    return render(request, 'users/driverDetail.html', locals())

def driverCancel(request, id):
    models.Ride.objects.get(id=id).delete()
    return redirect('/index/')

def driverComplete(request,id):
    ride = models.Ride.objects.get(id = id)
    ride.is_complete = True
    ride.save()
    return redirect('/index/')

