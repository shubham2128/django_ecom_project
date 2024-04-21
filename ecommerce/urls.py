from django.contrib import admin
from django.urls import path , include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('chat/', include('livechat.urls')),
    path('feedback/' , include('feedback.urls')),
    path('recommendation/', include('recommendation.urls')),
    path('promotions/',include('promotions.urls'))
]
