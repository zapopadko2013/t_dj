#from django.shortcuts import render

from django.http import HttpResponse
from .models import User
import time
import random
from .forms import UserForm
from django.http import JsonResponse
import string
from django.views.decorators.csrf import csrf_exempt
import json
from tj.genpassw import generate_random_password

  

from django.shortcuts import render

user = User.objects.all()
 
def index(request):

    if request.method == "POST":
        
        phone1 = request.POST.get("phone", "-1")

        # получаем все объекты
        user = User.objects.all()
        print(user.query)  
        fl = user.filter(phone = phone1).exists()
        print(fl)
        data={"phone": phone1}

        if fl :
            return HttpResponse(f"<h2>Телефон: {phone1}  найден</h2>") 
            return HttpResponse("Произошла ошибка", status=400, reason="В номере телефона должны быть только цифры ")
        else:
            time.sleep(2)
            random_number = random.randint(1000, 9999)
            data={"phone": phone1,"fl":1,"random": random_number}
            return render(request, "index.html", context=data)
    else:    
        return render(request, "index.html")

@csrf_exempt
def postupdatepassword(request): 

    if len(request.body) == 0 :
        phone1 = request.POST.get("phone")
        password1 = request.POST.get("password")
        newpassword1 = request.POST.get("newpassword").strip()
    else :
      
      body = request.body
      data1 = json.loads(body)
      
      phone1 = data1['phone'].strip()
      password1 = data1['password']
      newpassword1 = data1['newpassword']

    if len(newpassword1)<6 :
       data = {'error': 'Пароль не может быть меньше 6 символов!'}
       return JsonResponse(data, status=400)
    fl1 = user.filter(phone = phone1).exists()
    if fl1==False :
        data = {'error': 'Нет такого телефона!'}
        return JsonResponse(data, status=400)
    fl1 = user.filter(phone = phone1,password=password1).exists()
    if fl1==False :
        data = {'error': 'Нет такого пароля старого!'}
        return JsonResponse(data, status=400)
    u1 = user.filter(phone = phone1,password=password1)

    is_digit_present = any(character.isdigit() for character in newpassword1)
    if is_digit_present==False :
        data = {'error': 'В пароле должно быть число!'}
        return JsonResponse(data, status=400)
    
    is_alpha_present = any(character.isalpha() for character in newpassword1)
    if is_alpha_present==False :
        data = {'error': 'В пароле должна быть буква!'}
        return JsonResponse(data, status=400)
    
    is_spec=any(char in ".,:;!_*-+()/#¤%&@$^" for char in newpassword1)
    if is_spec==False :
        data = {'error': 'В пароле должен быть спецсимвол!'}
        return JsonResponse(data, status=400)

    u2 = User.objects.get(phone=phone1)
    u2.password = newpassword1
    u2.save(update_fields=["password"])
    if u2.id>0 :
        data={"phone": phone1,"statusp":4,"text":"Пароль у телефона заменён успешно!"}
        return JsonResponse(data, status=200)
    else:
        data = {'error': 'Нельзя сохранить пароль в базу данных!'}
        return JsonResponse(data, status=400)
      

def getuserpassw(request): 
    password1 = request.GET.get("password")
    fl1 = user.filter(password=password1).exists()
    if fl1==False :
        data = {'error': 'Нет такого пароля!'}

    u1 = user.filter(password=password1)
    ua = []
   
    for obj in u1:
        ua += [{
            'id': obj.id,
            'phone': obj.phone ,
            'password': obj.password,
            'name': obj.name
        }]
    data = {"user": ua}
    return JsonResponse(data)    


def profileuserpassw(request):    
    phone1 = request.GET.get("phone")
    password1 = request.GET.get("password")
    fl1 = user.filter(phone = phone1).exists()
    if fl1==False :
        data = {'error': 'Нет такого телефона!'}
        return JsonResponse(data, status=400)
    fl1 = user.filter(phone = phone1,password=password1).exists()
    if fl1==False :
        data = {'error': 'Нет такого пароля!'}
        return JsonResponse(data, status=400)
    u1 = user.filter(phone = phone1,password=password1)
    
    data = {"user": {
            'id': u1[0].id,
            'phone': u1[0].phone ,
            'password': u1[0].password,
            'name': u1[0].name
        }}
    print(data)
    return JsonResponse(data, status=200)

def profileuser(request):    
    phone1 = request.GET.get("phone")
    fl1 = user.filter(phone = phone1).exists()
    if fl1==False :
        data = {'error': 'Нет такого телефона!'}
        return JsonResponse(data, status=400)
    u1 = user.filter(phone = phone1)
    data = {"user": {
            'id': u1[0].id,
            'phone': u1[0].phone ,
            'password': u1[0].password,
            'name': u1[0].name
        }}
    
    return JsonResponse(data)

@csrf_exempt    
def postafterpassword(request):    

    if len(request.body) == 0 :
        phone1 = request.POST.get("phone")
        password1 = request.POST.get("password")
    else :
      
      body = request.body
      data1 = json.loads(body)
      
      phone1 = data1['phone'].strip()
      password1 = data1['password']

    fl1 = user.filter(phone = phone1).exists()
    if fl1==False :
        data = {'error': 'Нет такого телефона!'}
        return JsonResponse(data, status=400)
    
    # Мгновенная проверка
    is_digit_present = any(character.isdigit() for character in password1)
    if is_digit_present==False :
        data = {'error': 'В пароле должно быть число!'}
        return JsonResponse(data, status=400)
    
    is_alpha_present = any(character.isalpha() for character in password1)
    if is_alpha_present==False :
        data = {'error': 'В пароле должна быть буква!'}
        return JsonResponse(data, status=400)
    
    is_spec=any(char in ".,:;!_*-+()/#¤%&@$^" for char in password1)
    if is_spec==False :
        data = {'error': 'В пароле должен быть спецсимвол!'}
        return JsonResponse(data, status=400)

    u2 = User.objects.get(phone=phone1)
    u2.password = password1
    u2.save(update_fields=["password"])
    if u2.id>0 :
        data={"phone": phone1,"statusp":4,"text":"Пароль у телефона введён успешно!"}
        return JsonResponse(data, status=200)
    else:
        data = {'error': 'Нельзя сохранить пароль в базу данных!'}
        return JsonResponse(data, status=400)

@csrf_exempt    
def postpassword(request):    

    if len(request.body) == 0 :
        phone1 = request.POST.get("phone")
        password1 = request.POST.get("password")
    else :
      
      body = request.body
      data1 = json.loads(body)
      
      phone1 = data1['phone'].strip()
      password1 = data1['password']

    fl1 = user.filter(phone = phone1).exists()
    if fl1==False :
        data = {'error': 'Нет такого телефона!'}
        return JsonResponse(data, status=400)
    fl = user.filter(phone = phone1,password=password1,status=2).exists()
    if fl :
        data={"phone": phone1,"statusp":3,"text":"Телефон есть в базе данных. Регистрация прошла успешно!"}
        return JsonResponse(data, status=200)
    else:
        data = {'error': 'Нет такого пароля для заданного телефона!'}
        return JsonResponse(data, status=400)

def generate_password(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password        

@csrf_exempt
def postcode(request):

    if len(request.body) == 0 :
        phone1 = request.POST.get("phone")
        code = request.POST.get("code")
    else :
      
      body = request.body
      data1 = json.loads(body)
      
      phone1 = data1['phone'].strip()
      code = data1['code']    

    fl1 = user.filter(phone = phone1).exists()
    if fl1==False :
        data = {'error': 'Нет такого телефона!'}
        return JsonResponse(data, status=400)
    fl = user.filter(phone = phone1,password=code,status=1).exists()
    if fl :
        # random_number = generate_password(6)
        random_number =generate_random_password(6,3,2,1)
        data={"phone": phone1,"statusp":2,"random": random_number,"text":"Телефон есть в базе данных. Введите пароль:"}
        u2 = User.objects.get(phone=phone1)
        u2.password = random_number
        u2.status=2
        u2.save(update_fields=["password","status"])
        if u2.id>0 :
            return JsonResponse(data, status=200)
        else:
            data = {'error': 'Нельзя сохранить пароль в базу данных!'}
            return JsonResponse(data, status=400)
    else:
        data = {'error': 'Нет такого кода для заданного телефона!'}
        return JsonResponse(data, status=400)    
    
@csrf_exempt 
def postphone(request):
    # получаем из данных запроса POST отправленные через форму данные

    
    
    if len(request.body) == 0 :
      
      
      phone1 = request.POST.get("phone").strip()
      name1 = request.POST.get("name")
    else :
      

      body = request.body
      data1 = json.loads(body)
      
      phone1 = data1['phone'].strip()
      name1 = data1['name']    

    if len(phone1)!=10 :
       data = {'error': 'В номере телефона должно быть 10 цифр!'}
       return JsonResponse(data, status=400)

    if request.method == "POST":
        if len(request.body) == 0 :
           
           userform = UserForm(request.POST)
        else :
           
           body = request.body
           data1 = json.loads(body)
           userform = UserForm(data1)     
        if userform.is_valid():
            
            # получаем все объекты
            # user = User.objects.all()
            print(user.query)  
            fl = user.filter(phone = phone1).exists()
            print(fl)
            data={"phone": phone1}

            if fl :

                fl1 = user.filter(phone = phone1,status=1).exists()
                u1 = user.filter(phone = phone1)
                if fl1 :
                                        
                    #Здесь посылается смс на телефон, random передаю, для теста, чтобы знать какой код вводить, а так не надо его здесь возвращать
                    data={"phone": phone1,"statusp":1,"random": u1[0].password,"text":"Телефон есть в базе данных. Регистрация до конца не прошла. Введите код:"}
                    
                else :
                    
                    #Здесь пользователь должен после этого ввести пароль, random передаю, для теста, чтобы знать какой пароль вводить, а так не надо его здесь возвращать
                   data={"phone": phone1,"statusp":2,"random": u1[0].password,"text":"Телефон есть в базе данных. Введите пароль:"}
                
                return JsonResponse(data, status=200) 
        
            else:
                time.sleep(2)
                random_number = random.randint(1000, 9999)
                data={"phone": phone1,"statusp":1,"random": random_number,"text":"Телефон отсутствует в базе данных. Введите код:"}
                u1=User.objects.create(phone=phone1,name=name1, password=random_number, status=1)
                if u1.id>0 :
                    return JsonResponse(data, status=200)
                else:
                    data = {'error': 'Нельзя сохранить код в базу данных!'}
                    return JsonResponse(data, status=400)

        else:
            
            data = {'error': 'В поле номер должны быть только цифры!'}
            return JsonResponse(data, status=400)

    