from django.urls import path
from tj import views




 
urlpatterns = [
   
    path("", views.index, name='index'),
    path("postphone/", views.postphone, name='postphone'),
    path("postcode/", views.postcode, name='postcode'),
    path("postpassword/", views.postpassword, name='postpassword'),
    path("profileuser/", views.profileuser, name='profileuser'),
    path("profileuserpassw/", views.profileuserpassw, name='profileuserpassw'),
    path("getuserpassw/", views.getuserpassw, name='getuserpassw'),
    path("postupdatepassword/", views.postupdatepassword, name='postupdatepassword'),
    path("postafterpassword/", views.postafterpassword, name='postafterpassword')

    



    
]
