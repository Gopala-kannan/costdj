from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from cost.models import Profile, SpendAmount
from cost.serializers import ProfileSerializer, SpendAmountSerializer, UserRegisterSerializer
# from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import get_object_or_404

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterSerializer(data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile_create')  
        else:
            return render(request, 'register.html', {'form': form})
    else:
        form = UserRegisterSerializer()
    return render(request, 'register.html', {'form': form})

def login_view(request):
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile_create')
            else:
                return render(request, 'login.html')
        return render(request, 'login.html')

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('login')

@csrf_exempt
def profile_api(request, id=0):
    if request.method == 'GET':
        profiles = Profile.objects.all()
        profiles_serializer = ProfileSerializer(profiles, many=True)
        return JsonResponse(profiles_serializer.data)
    
    elif request.method == 'POST':
        profile_data = JSONParser().parse(request)
        profile_serializer = ProfileSerializer(data=profile_data)
        if profile_serializer.is_valid():
            profile_serializer.save()
            return JsonResponse("Added Successfully")
    
    elif request.method == 'PUT':
        profile_data = JSONParser().parse(request)
        profile = Profile.objects.get(id=id)
        profile_serializer = ProfileSerializer(profile, data=profile_data)
        if profile_serializer.is_valid():
            profile_serializer.save()
            return JsonResponse("Updated Successfully")
        return JsonResponse("Failed to Update")
    
    elif request.method == 'DELETE':
        profile = Profile.objects.get(id=id)
        profile.delete()
        return JsonResponse("Deleted Successfully")
    
@csrf_exempt
def spendamount_api(request, id=0):
    if request.method == 'GET':
        spendamounts = SpendAmount.objects.all()
        spendamounts_serializer = SpendAmountSerializer(spendamounts, many=True)
        return JsonResponse(spendamounts_serializer.data)
    
    elif request.method == 'POST':
        spendamount_data = JSONParser().parse(request)
        spendamount_serializer = SpendAmountSerializer(data=spendamount_data)
        if spendamount_serializer.is_valid():
            spendamount_serializer.save()
            return JsonResponse("Added Successfully")
    
    elif request.method == 'PUT':
        spendamount_data = JSONParser().parse(request)
        spendamount = SpendAmount.objects.get(id=id)
        spendamount_serializer = SpendAmountSerializer(spendamount, data=spendamount_data)
        if spendamount_serializer.is_valid():
            spendamount_serializer.save()
            return JsonResponse("Updated Successfully")
        return JsonResponse("Failed to Update")
    
    elif request.method == 'DELETE':
        spendamount = SpendAmount.objects.get(id=id)
        spendamount.delete()
        return JsonResponse("Deleted Successfully")
    
def details(request):
    profiles = Profile.objects.all()
    for p in profiles:
        p.update_financials()
    return render(request, 'details.html', {'profiles': profiles})

def profile_spendamounts(request):
    spendamounts = SpendAmount.objects.all()
    return render(request, 'details.html', {'spendamounts': spendamounts})

def profile_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        credit = request.POST.get('credit')
        if name and credit:
            profile = Profile.objects.create(
                name=name,
                credit=credit,
                debit=0,
                balance=credit
            )
            return redirect('spendamount_create')
    return render(request, 'create.html')

def spendamount_create(request):
    profiles = Profile.objects.all()
    if request.method == 'POST':
        profile_id = request.POST.get('profile')
        profile = get_object_or_404(Profile, id=profile_id)
        SpendAmount.objects.create(
            profile=profile,
            home_rent=request.POST.get('home_rent'),
            eb_bill=request.POST.get('eb_bill'),
            gas_bill=request.POST.get('gas_bill'),
            groceries=request.POST.get('groceries')
        )
        profile.update_financials()

        return redirect('details')  
    return render(request, 'amount.html', {'profiles': profiles})