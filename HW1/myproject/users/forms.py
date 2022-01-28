from django import forms


class UserForm(forms.Form):
    username = forms.CharField(label="用户", max_length=128)
    password = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    gender = (
        ('male', "男"),
        ('female', "女"),
    )
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(attrs={'class': 'form-control'}))

class DriverForm(forms.Form):
    vehicle_type = forms.CharField(label="车辆类型", max_length=100)
    license_number = forms.CharField(label="车牌号", max_length=100)
    max_number_of_passengers = forms.IntegerField(label="最大乘客数量")
    special_request = forms.CharField(label="特殊要求", required = False, max_length=100) # optional

class RideRequestForm(forms.Form):
    destination = forms.CharField(label="目的地", max_length=100)
    arrival_time = forms.DateTimeField()
    number_of_total_passengers = forms.IntegerField(label="乘客数量")
    vehicle_type = forms.CharField(label="指定车型", required = False, max_length=100) # optional
    is_shared = forms.BooleanField(required = False)

class SharerForm(forms.Form):
    destination = forms.CharField(max_length=256)
    arrival_early = forms.DateTimeField()
    arrival_late = forms.DateTimeField()
    number_of_passengers = forms.IntegerField()

