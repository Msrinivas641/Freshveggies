from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings



 # include should be imported

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('swachathapp.urls')),# Include the app's urls
    path('auth/', include("authcart.urls")),  
    

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
