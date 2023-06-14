from django.urls import path

from .views import *
urlpatterns = [
    path('', index, name='home'),

    path('esasy-shypa/', homepage, name="home_page"),
    path('kamera-1/', livefe, name="live_camera"),
    path('kamera-2/', livefe_2, name="live_camera_2"),

    path('ulgama-giris/', admin_login, name='login'),
    path('ulgamdan_cykys/', admin_logout, name='logout'),

    path('ulgama-gosmak/', register, name='register'),
    path('surat-gosmak/', face_add, name='face_add'),
    path('isgarlerin-gory/', StaffMembers.as_view(), name='staff_members'),
    path('isgar/<slug:slug>/', PersonView.as_view(), name='person'),

    path('isgar/<slug:slug>/ayyrmak/', PersonDeleteView.as_view(), name='delete'),
    path('isgar/<slug:slug>/uytgetmek/', PersonUpdateView.as_view(), name='update'),

    path('giris-gatnasyk/', export_get_in_excel_file, name='excel_in'),
    path('cykys-gatnasyk/', export_get_out_excel_file, name='excel_out'),
    path('giris-statistikasy/', InputStatistics.as_view(), name='input_statistics'),
    path('cykys-statistikasy/', OutputStatistics.as_view(), name='output_statistics'),

]


handler404 = 'core.views.error_404'
handler500 = 'core.views.error_500'
handler403 = 'core.views.error_403'
handler400 = 'core.views.error_400'
