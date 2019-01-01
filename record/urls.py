from django.urls import path

from record import views as record_views

app_name = 'record'

urlpatterns = [
    # path('', record_views.index, name='index'),
    path('', record_views.dashboard, name='dashboard'),
    path('add-society/', record_views.addSocietyView, name='add-society'),
    path('<slug>/add-member/', record_views.addMemberView, name='add-member'),
    path('<slug>/', record_views.society_dash, name='society-dash'),
    path('<slug>/record/', record_views.monthly_record, name='monthly-record'),
    path('<slug>/<id>/<month>/change/', record_views.createMonthlyRecordView, name='change-prev-data'),
    path('<soc_id>/delete-member/<id>', record_views.delete_member_view, name='delete-member'),



]
