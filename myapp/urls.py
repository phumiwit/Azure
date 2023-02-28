from django.urls import path
from myapp import views
urlpatterns = [
    path("mainpage",views.mainpage,name='mainpage'),
    path('choosefile/', views.choosefile, name='choosefile'),
    path("predictfile",views.predictfile),
    path("showchoosefile",views.showchoosefile),
    path('collection', views.collection, name='collection'),
    path('stackbar/<int:audio_id>/', views.stackbar, name='stackbar'),
    path('collections', views.collections, name='collections'),
    path('topsong', views.topsongspotify, name='topsongspotify'),
    path('topsong1', views.topsonglastfm, name='topsonglastfm'),
    path('collectiondetail/<str:collectionname>/', views.collection_detail, name='collection_detail'),
    path('download_json/str:filename/str:genre/', views.download_json, name='download_json'),
    path('collections/<str:audio_id>/delete/', views.collection_delete, name='collection_delete'),
    path('collections/delete/', views.delete_collection, name='delete_collection'),
    path('collection/<str:audio_id>/delete/confirm/', views.confirm_delete, name='confirm_delete'),
    path('confirm_delete_collection/', views.confirm_delete_collection, name='confirm_delete_collection'),
    path('error/', views.error, name='error'),
    
]