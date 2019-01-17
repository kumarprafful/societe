from django.urls import path

from record import views as record_views

app_name = 'record'

urlpatterns = [
    # path('', record_views.index, name='index'),
    path('', record_views.dashboard, name='dashboard'),
    path('add-society/', record_views.addSocietyView, name='add-society'),
    path('<slug>/add-member/', record_views.addMemberView, name='add-member'),
    path('<slug>/', record_views.society_dash, name='society-dash'),
    path('<slug>/settings/', record_views.society_settings, name='society-settings'),
    path('<slug>/record/', record_views.monthly_record, name='monthly-record'),
    path('<slug>/record/<month>', record_views.monthly_record, name='monthly-record'),
    path('<slug>/record/<month>/json', record_views.monthly_record_ajax, name='monthly-record-ajax'),
    path('<slug>/<id>/<month>/change/', record_views.createMonthlyRecordView, name='change-prev-data'),
    path('<soc_id>/delete-member/<id>/', record_views.delete_member_view, name='delete-member'),
    path('<slug>/all-record/', record_views.all_record, name='all-records'),
    path('<slug>/<member_id>/<month>/edit-record/', record_views.editMonthlyRecordView, name='edit-record'),
    path('<slug>/analytics/', record_views.getMonthlyRecordSum, name='analytics'),
    path('<slug>/analytics/<year>', record_views.getMonthlyRecordSum, name='analytics'),







]
