
from django.contrib import admin
from django.urls import path, include

from newsportal.views import NewsListView, NewsDetailView, NewsSearchView, NewsCreateView, NewsDeleteView, \
    NewsUpdateView, upgrade_me

urlpatterns = [

    path('news/', NewsListView.as_view(), name= 'news_all'),

    path('news/search/', NewsSearchView.as_view(), name = 'news_search' ),
    path('news/add/', NewsCreateView.as_view(), name = 'news_create'),
    path('news/<int:pk>', NewsDetailView.as_view(), name='news_single'),
    path('news/<int:pk>/edit/', NewsUpdateView.as_view(), name = 'news_update'),
    path('news/<int:pk>/delete/', NewsDeleteView.as_view(), name = 'news_delete'),
    path('upgrade_to_author/', upgrade_me, name ='upgrade')



]
