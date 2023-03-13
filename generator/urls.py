from django.urls import path
from . import views

urlpatterns = [
    path('', views.data_schemas, name='data_schemas'),
    path('new/', views.add_schema, name='add_schema'),
    path('create/', views.new_schem, name='new_schem'),

    path('edit_scheme/<int:pk>/', views.edit_scheme, name='edit_scheme'),
    path('delete_scheme/<int:pk>/', views.delete_scheme, name='delete_scheme'),
    path('delete_column/<int:pk>/', views.delete_column, name='delete_column'),
    path('data_sets/', views.data_sets, name='data_sets'),
    path('download/<str:filename>/', views.download_file, name='download'),
]
