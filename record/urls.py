from django.urls import path

from record import views as record_views

app_name = 'record'

urlpatterns = [
    path('', record_views.index, name='index'),
    path('dashboard/', record_views.dashboard, name='dashboard'),
    path('add-society/', record_views.addSocietyView, name='add-society'),
    path('<id>/add-member/', record_views.addMemberView, name='add-member'),
    path('<id>/', record_views.society_dash, name='society-dash'),
    path('<id>/record/', record_views.monthly_record, name='monthly-record'),
    path('<id>/<month>/change/', record_views.createMonthlyRecordView, name='change-prev-data'),



]
