from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

import groups.api_views

urlpatterns = [

    path('', groups.api_views.GroupList.as_view()),
    path('new', groups.api_views.GroupCreate.as_view()),
    path('<int:id>/', groups.api_views.GroupRetrieveUpdateDestroy.as_view()),

    path('tags/', groups.api_views.TagList.as_view()),
    path('tags/new', groups.api_views.TagCreate.as_view()),
    path('tags/<int:id>/', groups.api_views.TagRetrieveUpdateDestroy.as_view()),

    path('categories/', groups.api_views.CategoryList.as_view()),
    path('categories/new', groups.api_views.CategoryCreate.as_view()),
    path('categories/<int:id>/', groups.api_views.CategoryRetrieveUpdateDestroy.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)