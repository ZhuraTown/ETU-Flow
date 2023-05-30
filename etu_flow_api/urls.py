from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from etu_flow_api.settings import DEBUG, MEDIA_URL, MEDIA_ROOT
from etu_flow_api.swagger import schema_view
from users.urls import urlpatterns as url_users
from university_structure.urls import urlpatterns as url_university_structure
from schedule.urls import urlpatterns as url_schedule


urlpatterns = [
   path('swagger<str:format>', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns += url_users
urlpatterns += url_university_structure
urlpatterns += url_schedule

if DEBUG:
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)


