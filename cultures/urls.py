from django.urls import path
from . import views
from .views import CultureListView

app_name = 'cultures'

urlpatterns = [
    path('<id>/', views.get_culture_view, name="culture-get"),
    path('delete/<id>', views.delete_culture_view, name="culture-delete"),
    path('update/<id>', views.update_culture_view, name="culture-put"),
    path('add', views.post_culture_view, name="culture-post"),
    path('list', CultureListView.as_view(), name="culture-list"),
    path('vinculate', views.vinculate_culture_view, name="culture-vinculate"),
]
