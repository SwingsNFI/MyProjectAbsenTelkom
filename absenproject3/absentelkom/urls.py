from django.urls import path
from . import views

urlpatterns = [
    path('', views.to_login_views),
    path('login', views.to_login_views),
    path('guru', views.to_login_guru_views),
    path('loginprocess', views.login_views),
    path('guruprocess', views.login_guru_views),
    path('validasiprocess', views.validasi_views),
    path('validasiamiprocess', views.ami_validasi_views),
    path('absen', views.absen_views),
    path('home', views.to_home_views),
    path('walashome', views.to_walashome_views),
    path('cta', views.to_cta_views),
    path('re', views.to_re_views),
    path('di', views.to_di_views),
    path('validasi', views.to_validasi_views),
    path('kelas', views.to_pilihkelas_views),
    path('dinonwalas', views.to_nonwalas_di_views),
    path('kelasnonwalas', views.to_nonwalas_pilihkelas_views),
    path('validasinonwalas', views.to_nonwalas_validasi_views),
    path('report', views.to_nonwalas_report_views),
    path('admin', views.to_admin_views),
    path('adminguru', views.to_admin_guru_views),
    path('tambahguru', views.to_admin_tambahguru_views),
    path('editguru', views.to_admin_editguru_views),
    path('tambahguruprocess', views.admin_tambahguru_views),
    path('editguruprocess', views.admin_editguru_views),
    path('hapusguru', views.admin_hapusguru_views),
    path('adminsiswa', views.to_admin_siswa_views),
    path('tambahsiswa', views.to_admin_tambahsiswa_views),
    path('editsiswa', views.to_admin_editsiswa_views),
    path('tambahsiswaprocess', views.admin_tambahsiswa_views),
    path('editsiswaprocess', views.admin_editsiswa_views),
    path('hapussiswa', views.admin_hapussiswa_views),
    path('adminkelas', views.to_admin_kelas_views),
    path('tambahkelas', views.to_admin_tambahkelas_views),
    path('editkelas', views.to_admin_editkelas_views),
    path('tambahkelasprocess', views.admin_tambahkelas_views),
    path('editkelasprocess', views.admin_editkelas_views),
    path('hapuskelas', views.admin_hapuskelas_views),
    path('adminacara', views.to_admin_acara_views),
    path('tambahacara', views.to_admin_tambahacara_views),
    path('editacara', views.to_admin_editacara_views),
    path('tambahacaraprocess', views.admin_tambahacara_views),
    path('editacaraprocess', views.admin_editacara_views),
    path('hapusacara', views.admin_hapusacara_views),
    path('adminpelajaran', views.to_admin_pelajaran_views),
    path('tambahpelajaran', views.to_admin_tambahpelajaran_views),
    path('editpelajaran', views.to_admin_editpelajaran_views),
    path('tambahpelajaranprocess', views.admin_tambahpelajaran_views),
    path('editpelajaranprocess', views.admin_editpelajaran_views),
    path('hapuspelajaran', views.admin_hapuspelajaran_views),
    path('sortingreport', views.sorting_report_views),
    path('logout', views.logout_views),
    path('ajaxcheckpelajaran', views.checkpelajaran_views, name="ajaxcheckpelajaran"),
]