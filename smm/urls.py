from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView



admin.site.site_header = "SMM"
admin.site.site_title =  "SMM"
admin.site.index_title = "SMM"


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('front.urls')),
    path('cp/', include('cp.urls')),
    path('index.html', RedirectView.as_view(url='/', permanent=False), name='index1'),
    path('index.php', RedirectView.as_view(url='/', permanent=False), name='index2'),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)