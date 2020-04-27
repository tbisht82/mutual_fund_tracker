from django.urls import path
from . import views

urlpatterns = [
    path('new/', views.add_new_isin, name='new_isin'),
    path('detail/<str:isin>', views.detail_isin, name='details_isin'),
    path('search', views.search, name='search_isin'),
    path('chart/<str:isin>', views.chart_data, name='chart_data'),
]
