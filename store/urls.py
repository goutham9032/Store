from django.conf.urls import url
from django.contrib import admin

from app import views as app_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^create-discount/$', app_views.create_discount, name='create_discount'),
    url(r'^all-discounts/$', app_views.all_discounts, name='all_discounts'),
    url(r'^map-discount-store/$', app_views.map_discount_store, name='map_discount_store'),
]
