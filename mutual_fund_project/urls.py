from django.contrib import admin
from django.urls import path, include
import debug_toolbar
from . import views
from django.conf.urls import handler404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('mutualfunds/', include('mutual_fund_track.urls')),
    path('__debug__/', include(debug_toolbar.urls)),
]

handler404 = views.handler404
