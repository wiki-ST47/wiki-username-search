from django.contrib.auth import views as auth_views
from django.urls import include, path
from django.contrib import admin
import username_search.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('', username_search.views.index, name='home'),
    path('docs/', username_search.views.docs, name='docs'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('search/', username_search.views.search, name='search'),
    path('tools/', username_search.views.tools, name='tools'),
]
