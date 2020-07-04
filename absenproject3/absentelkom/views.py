from django.shortcuts import render, redirect
from .models import *
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db.models import Q, F
from django.db.models.functions import Greatest
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta

# Create your views here.
def to_login_views(request):
    try:
        del request.session['idcook']
        del request.session['namacook']
        del request.session['gucook']
        del request.session['idacaracook']
        del request.session['aksescook']
    except:
        pass
    return render(request, 'Login/SiswaLogin.html', {})

def to_login_guru_views(request):
    try:
        del request.session['idcook']
        del request.session['namacook']
        del request.session['gucook']
        del request.session['idacaracook']
        del request.session['aksescook']
    except:
        pass
    return render(request, 'Login/GuruLogin.html', {})

def login_views(request):
    if request.method == "POST":
        if request.POST['nis'] != "":
            try:
                tbl_siswa = Tbl_siswa.objects.get(id_siswa=request.POST['nis'])
            except Tbl_siswa.DoesNotExist:
                tbl_siswa = None
            if tbl_siswa is not None:
                if tbl_siswa.password_siswa == request.POST['password']:
                    request.session['idcook'] = tbl_siswa.id_siswa
                    request.session['namacook'] = tbl_siswa.nama_siswa
                    return redirect(to_home_views)
                else:
                    messages.warning(request, 'Password tidak sesuai dengan di database kami! Cobalah lagi!', extra_tags='alert')
                    return redirect(to_login_views)
            else:
                messages.warning(request, 'NIS yang dimasukan tidak sesuai dengan di database kami! Cobalah lagi!', extra_tags='alert')
                return redirect(to_login_views)
        else:
            messages.warning(request, 'NIS masih belum terisi!', extra_tags='alert')
            return redirect(to_login_views)
    else:
        return redirect(to_login_views)

def login_guru_views(request):
    if request.method == "POST":
        tbl_kategori = Tbl_kategori.objects.all()
        if request.POST['nik'] != "":
            try:
                tbl_guru = Tbl_guru.objects.get(id_guru=request.POST['nik'])
            except Tbl_guru.DoesNotExist:
                tbl_guru = None
            if tbl_guru is not None:
                if tbl_guru.password_guru == request.POST['password']:
                    tbl_kelas = Tbl_kelas.objects.all()
                    if tbl_guru.id_akses_id == 1: # admin
                        request.session['idcook'] = tbl_guru.id_guru
                        request.session['namacook'] = tbl_guru.nama_guru
                        request.session['gucook'] = 't'
                        return redirect(to_admin_views)
                    elif tbl_guru.id_akses_id == 2: # walas
                        request.session['idcook'] = tbl_guru.id_guru
                        request.session['aksescook'] = tbl_guru.id_akses_id
                        request.session['namacook'] = tbl_guru.nama_guru
                        request.session['gucook'] = 't'
                        return redirect(to_walashome_views)
                    elif tbl_guru.id_akses_id == 3: # nonwalas-guru
                        request.session['idcook'] = tbl_guru.id_guru
                        request.session['aksescook'] = tbl_guru.id_akses_id
                        request.session['namacook'] = tbl_guru.nama_guru
                        request.session['gucook'] = 't'
                        return redirect(to_nonwalas_di_views)
                    elif tbl_guru.id_akses_id == 4: # nonwalas-manajemen
                        request.session['idcook'] = tbl_guru.id_guru
                        request.session['namacook'] = tbl_guru.nama_guru
                        request.session['gucook'] = 't'
                        return redirect(to_nonwalas_report_views)
                    else:
                        return HttpResponse("<center> ANDA SEHARUSNYA TIDAK MENAMBAHKAN ID KE-"+ tbl_guru.id_akses_id +"!!!  :| </center>")
                else:
                    messages.warning(request, 'Password tidak sesuai dengan di database kami! Cobalah lagi!', extra_tags='alert')
                    return redirect(to_login_guru_views)
            else:
                messages.warning(request, 'NIK yang dimasukan tidak sesuai dengan di database kami! Cobalah lagi!', extra_tags='alert')
                return redirect(to_login_guru_views)
        else:
            messages.warning(request, 'NIK masih belum terisi!', extra_tags='alert')
            return redirect(to_login_guru_views)
    else:
        return redirect(to_login_guru_views)   

def logout_views(request):
    try:
        del request.session['idcook']
        del request.session['namacook']
        del request.session['aksescook']
        del request.session['idacaracook']
    except:
        pass
    try:
        request.session['gucook']
    except:
        return redirect(to_login_views)
    del request.session['gucook']
    return redirect(to_login_guru_views)

# Siswa
def to_home_views(request): # notice me beta!
    try:
        request.session['idcook']
    except:
        messages.warning(request, 'Sepertinya ada yang salah! Cobalah lagi!', extra_tags='alert')
        return redirect(to_login_views)
    if request.session['idcook'] != "":
        context = {
            "siswa": Tbl_siswa.objects.get(id_siswa=request.session['idcook']),
            "tbl_kategori": Tbl_kategori.objects.all(),
            "absen_amis": Tbl_absen_ami.objects.filter(Q(id_acara__waktu_acara__range=(timezone.now() - timedelta(days=7), timezone.now())), Q(id_siswa_id__exact=request.session['idcook'])),
            "validasis": Tbl_validasi.objects.filter(Q(id_absen__id_acara__waktu_acara__range=(timezone.now() - timedelta(days=7), timezone.now())), Q(id_absen__id_siswa_id__exact=request.session['idcook'])),
        }
        return render(request, 'Siswa/SiswaHome.html', context)
    else:
        return redirect(to_login_views)

def absen_views(request):
    if request.method == "POST":
        if request.session.has_key('idcook'):
            tbl_absen_save = Tbl_absen(
                id_acara_id = request.POST['idacara'],
                id_siswa_id = request.session['idcook'],
            )
            tbl_absen_save.save()
            return redirect(to_home_views)
        else:
            messages.warning(request, 'Sepertinya ada yang salah! Cobalah lagi!', extra_tags='alert')
            return redirect(to_login_views)
    else:
        return redirect(to_login_views)

# Guru
def to_walashome_views(request):
    try:
        request.session['idcook']
    except:
        messages.warning(request, 'Sepertinya ada yang salah! Cobalah lagi!', extra_tags='alert')
        return redirect(to_login_guru_views)
    if request.session['idcook'] != "":
        tbl_kategori = Tbl_kategori.objects.all()
        guru = Tbl_guru.objects.get(id_guru=request.session['idcook'])
        context = {
            "guru": guru,
            "tbl_kategori": tbl_kategori,
        }
        return render(request, "Guru/Walas/WalasHome.html", context)
    else:
        return redirect(to_login_guru_views)

def to_pilihkelas_views(request):
    if request.method == "POST":
        request.session['idacaracook'] = request.POST['idacara']
        context = {
            "tbl_kelas": Tbl_kelas.objects.all(),
        }
        return render(request, "Guru/Walas/PilihKelas.html", context)
    else:
        return redirect(to_login_guru_views)

def to_validasi_views(request):
    if request.method == "POST":
        try:
            request.session['idacaracook']
        except:
            messages.warning(request, 'Sepertinya ada yang salah! Cobalah lagi!', extra_tags='alert')
            return redirect(to_login_guru_views)
        kelas = Tbl_kelas.objects.get(id_kelas=request.POST['idkelas'])
        acara = Tbl_acara.objects.get(id_acara=request.session['idacaracook'])
        if acara.nama_acara.upper() == "AMI":
            try:
                request.session['idacaracook']
            except:
                messages.warning(request, 'Sepertinya ada yang salah! Cobalah lagi!', extra_tags='alert')
                return redirect(to_login_guru_views)
            kelas = Tbl_kelas.objects.get(id_kelas=request.POST['idkelas'])
            acara = Tbl_acara.objects.get(id_acara=request.session['idacaracook'])
            context = {
                "namakelas": kelas.nama_kelas,
                "namauser": request.session['namacook'],
                "tbl_jampel_start": Tbl_jampel_start.objects.all(),
                "tbl_jampel_end": Tbl_jampel_end.objects.all(),
                "siswas": Tbl_siswa.objects.filter(id_kelas__exact=request.POST['idkelas']),
            }
            return render(request, "Guru/Walas/ValidasiAMI.html", context)
        else:
            try:
                request.session['namacook']
            except:
                messages.warning(request, 'Sepertinya ada yang salah! Cobalah lagi!', extra_tags='alert')
                return redirect(to_login_guru_views)
            absens = Tbl_absen.objects.filter(Q(id_siswa__id_kelas__exact=request.POST['idkelas']), Q(id_acara__exact=request.session['idacaracook']))
            tbl_validasi = Tbl_validasi.objects.all()
            context = {
                "namaacara": acara.nama_acara,
                "namakelas": kelas.nama_kelas,
                "namauser": request.session['namacook'],
                "absens": absens,
                "tbl_validasi": tbl_validasi,
            }
            return render(request, "Guru/Walas/Validasi.html", context)
    else:
        return redirect(login_guru_views)

def validasi_views(request):
    if request.method == "POST":
        for i in range(int(request.POST['lengthloop'])):
            amount = i + 1
            if request.session.has_key('idcook'):
                if 'validasi'+str(amount) in request.POST:
                    tbl_validasi_save = Tbl_validasi(
                        id_absen_id = request.POST['validasi' + str(amount)],
                        id_guru_id = request.session['idcook'],
                        penambahan_poin = 1,
                    )
                    tbl_validasi_save.save()
            else:
                messages.warning(request, 'Sepertinya ada yang salah! Cobalah lagi!', extra_tags='alert')
                return redirect(to_login_guru_views)
        return redirect(to_walashome_views)
    else:
        return redirect(to_login_guru_views)

def to_nonwalas_pilihkelas_views(request):
    if request.method == "POST":
        request.session['idacaracook'] = request.POST['idacara']
        context = {
            "tbl_kelas": Tbl_kelas.objects.all(),
        }
        return render(request, "Guru/NonWalas_Guru/PilihKelas.html", context)
    else:
        return redirect(to_login_guru_views)

def to_nonwalas_validasi_views(request):
    if request.method == "POST":
        try:
            request.session['idacaracook']
        except:
            messages.warning(request, 'Sepertinya ada yang salah! Cobalah lagi!', extra_tags='alert')
            return redirect(to_login_guru_views)
        kelas = Tbl_kelas.objects.get(id_kelas=request.POST['idkelas'])
        acara = Tbl_acara.objects.get(id_acara=request.session['idacaracook'])
        context = {
            "namakelas": kelas.nama_kelas,
            "namauser": request.session['namacook'],
            "tbl_jampel_start": Tbl_jampel_start.objects.all(),
            "tbl_jampel_end": Tbl_jampel_end.objects.all(),
            "siswas": Tbl_siswa.objects.filter(id_kelas__exact=request.POST['idkelas']),
        }
        return render(request, "Guru/NonWalas_Guru/ValidasiAMI.html", context)
    else:
        return redirect(login_guru_views)

def ami_validasi_views(request):
    if request.method == "POST":
        try:
            request.session['idacaracook']
        except:
            messages.warning(request, 'Sepertinya ada yang salah! Cobalah lagi!', extra_tags='alert')
            return redirect(to_login_guru_views)
        tbl_absen_ami = Tbl_absen_ami.objects.all()
        for i in range(int(request.POST['lengthloop'])):
            amount = i + 1
            edit = False
            for absen_ami in tbl_absen_ami:
                if int(absen_ami.id_acara_id) == int(request.session['idacaracook']) and int(absen_ami.id_siswa_id) == int(request.POST['validasi' + str(amount)]) and int(absen_ami.id_jampel_start_id) == int(request.POST['idstart']) and int(absen_ami.id_jampel_end_id) == int(request.POST['idend']):
                    edit = True
                    if request.session.has_key('idcook'):
                        hadirvar = False
                        rapihvar = False
                        bersihvar = False
                        poinvar = 0
                        if 'hadir'+str(amount) in request.POST:
                            hadirvar = True
                            poinvar += 1
                        if 'rapih'+str(amount) in request.POST:
                            rapihvar = True
                            poinvar += 1
                        if 'bersih'+str(amount) in request.POST:
                            bersihvar = True
                            poinvar += 1
                        if 'validasi'+str(amount) in request.POST:
                            absen_ami_update = Tbl_absen_ami.objects.get(id_absen_ami=absen_ami.id_absen_ami)
                            absen_ami_update.id_jampel_start_id = request.POST['idstart']
                            absen_ami_update.id_jampel_end_id = request.POST['idend']
                            absen_ami_update.id_guru_id = request.session['idcook']
                            absen_ami_update.kehadiran = hadirvar
                            absen_ami_update.kerapihan = rapihvar
                            absen_ami_update.kebersihan = bersihvar
                            absen_ami_update.penambahan_poin = poinvar
                            absen_ami_update.save()
                            
                        else:
                            messages.warning(request, 'Sepertinya ada yang salah! Cobalah lagi!', extra_tags='alert')
                            return redirect(to_login_guru_views)
                    else:
                        messages.warning(request, 'Sepertinya ada yang salah! Cobalah lagi!', extra_tags='alert')
                        return redirect(to_login_guru_views)
            if edit == False:    
                if request.session.has_key('idcook'):
                    hadirvar = False
                    rapihvar = False
                    bersihvar = False
                    poinvar = 0
                    if 'hadir'+str(amount) in request.POST:
                        hadirvar = True
                        poinvar += 1
                    if 'rapih'+str(amount) in request.POST:
                        rapihvar = True
                        poinvar += 1
                    if 'bersih'+str(amount) in request.POST:
                        bersihvar = True
                        poinvar += 1
                    if 'validasi'+str(amount) in request.POST:
                        tbl_absenami_save = Tbl_absen_ami(
                            id_jampel_start_id = request.POST['idstart'],
                            id_jampel_end_id = request.POST['idend'],
                            id_acara_id = request.session['idacaracook'],
                            id_siswa_id = request.POST['validasi' + str(amount)],
                            id_guru_id = request.session['idcook'],
                            kehadiran = hadirvar,
                            kerapihan = rapihvar,
                            kebersihan = bersihvar,
                            penambahan_poin = poinvar,
                        )
                        tbl_absenami_save.save()
                    else:
                        messages.warning(request, 'Sepertinya ada yang salah! Cobalah lagi!', extra_tags='alert')
                        return redirect(to_login_guru_views)
                else:
                    messages.warning(request, 'Sepertinya ada yang salah! Cobalah lagi!', extra_tags='alert')
                    return redirect(to_login_guru_views)
        try:
            request.session['aksescook']
        except:
            messages.warning(request, 'Sepertinya ada yang salah! Cobalah lagi!', extra_tags='alert')
            return redirect(to_login_guru_views)
        if request.session['aksescook'] == 3:
            return redirect(to_nonwalas_di_views)
        elif request.session['aksescook'] == 2:
            request.session['permission'] = request.POST
            return redirect(to_walashome_views)
        else:
            messages.warning(request, 'Sepertinya ada yang salah! Cobalah lagi!', extra_tags='alert')
            return redirect(to_login_guru_views)   
    else:
        return redirect(to_login_guru_views)

def to_nonwalas_report_views(request):
    context = {
        "tbl_siswa": Tbl_siswa.objects.all(),
        "tbl_kelas": Tbl_kelas.objects.all(),
        "tbl_validasi": Tbl_validasi.objects.all(),
        "tbl_absen_ami": Tbl_absen_ami.objects.all(),
    }
    return render(request, "Guru/Nonwalas_Manajemen/Report.html", context)

def sorting_report_views(request):
    if request.method == "POST":
        context = {
            "tbl_siswa": Tbl_siswa.objects.filter(id_kelas_id__exact=request.POST['idkelas']),
            "tbl_kelas": Tbl_kelas.objects.all(),
            "tbl_validasi": Tbl_validasi.objects.filter(Q(id_absen__id_acara__waktu_acara__range=(request.POST['start'], request.POST['end'])), Q(id_absen__id_siswa__id_kelas_id__exact=request.POST['idkelas'])),
            "tbl_absen_ami": Tbl_absen_ami.objects.filter(Q(id_acara__waktu_acara__range=(request.POST['start'], request.POST['end'])), Q(id_siswa__id_kelas_id__exact=request.POST['idkelas'])),
        }
        return render(request, "Guru/Nonwalas_Manajemen/Report.html", context)
    else:
        messages.warning(request, 'Sepertinya ada yang salah! Cobalah lagi!', extra_tags='alert')
        return redirect(to_login_guru_views)  

# Admin
def to_admin_views(request):
    if request.session.has_key('namacook'):
        context = {
            "jumlahsiswa": len(Tbl_siswa.objects.all()),
            "jumlahguru": len(Tbl_guru.objects.all()), 
            "jumlahacara": len(Tbl_acara.objects.all()),
            "jumlahkelas": len(Tbl_kelas.objects.all()),
            "namauser": request.session['namacook'],
        }
        return render(request, "Guru/Admin/AdminDashboard.html", context)
    else:
        messages.warning(request, 'Sepertinya ada yang salah! Cobalah lagi!', extra_tags='alert')
        return redirect(to_login_guru_views)

def to_admin_guru_views(request):
    if request.session.has_key('namacook'):
        context = {
            "tbl_guru": Tbl_guru.objects.all(),
            "namauser": request.session['namacook'],
        }
        return render(request, "Guru/Admin/Guru/AdminGuru.html", context)
    else:
        messages.warning(request, 'Sepertinya ada yang salah! Cobalah lagi!', extra_tags='alert')
        return redirect(to_login_guru_views)

def to_admin_tambahguru_views(request):
    if request.session.has_key('namacook'):
        context = {
            "tbl_akses": Tbl_akses.objects.all(),
            "namauser": request.session['namacook'],
        }
        return render(request, "Guru/Admin/Guru/AdminTambahGuru.html", context)
    else:
        messages.warning(request, 'Sepertinya ada yang salah! Cobalah lagi!', extra_tags='alert')
        return redirect(to_login_guru_views)

def to_admin_editguru_views(request):
    if request.method == "POST":
        if request.session.has_key('namacook'):
            context = {
                "guru": Tbl_guru.objects.get(id_guru=request.POST['idguru']),
                "tbl_akses": Tbl_akses.objects.all(),
                "namauser": request.session['namacook'],
            }
            return render(request, "Guru/Admin/Guru/AdminEditGuru.html", context)
        else:
            messages.warning(request, 'Sepertinya ada yang salah! Cobalah lagi!', extra_tags='alert')
            return redirect(to_login_guru_views)
    else:
        return redirect(to_login_guru_views)

def admin_tambahguru_views(request):
    if request.method == "POST":
        tbl_guru_save = Tbl_guru(
            id_guru = request.POST['nik'],
            nama_guru = request.POST['namag'],
            email_guru = request.POST['emailg'],
            password_guru = request.POST['passwordg'],
            id_akses_id = request.POST['idaksesg'],
        )
        tbl_guru_save.save()
        return redirect(to_admin_guru_views)
    else:
        messages.warning(request, 'Sepertinya ada yang salah! Cobalah lagi!', extra_tags='alert')
        return redirect(login_guru_views)

def admin_editguru_views(request):
    if request.method == "POST":
        tbl_guru = Tbl_guru.objects.get(id_guru=request.POST['nik'])
        tbl_guru.id_guru = request.POST['nik']
        tbl_guru.nama_guru = request.POST['namag']
        tbl_guru.email_guru = request.POST['emailg']
        tbl_guru.password_guru = request.POST['passwordg']
        tbl_guru.id_akses_id = request.POST['idaksesg']
        tbl_guru.save()
        return redirect(to_admin_guru_views)
    else:
        messages.warning(request, 'Sepertinya ada yang salah! Cobalah lagi!', extra_tags='alert')
        return redirect(login_guru_views)

def admin_hapusguru_views(request):
    if request.method == "POST":
        tbl_guru = Tbl_guru.objects.get(id_guru=request.POST['idguru'])
        tbl_guru.delete()
        return redirect(to_admin_guru_views)
    else:
        messages.warning(request, 'Sepertinya ada yang salah! Cobalah lagi!', extra_tags='alert')
        return redirect(login_guru_views)

def to_admin_siswa_views(request):
    if request.session.has_key('namacook'):
        context = {
            "tbl_siswa": Tbl_siswa.objects.all(),
            "namauser": request.session['namacook'],
        }
        return render(request, "Guru/Admin/Siswa/AdminSiswa.html", context)
    else:
        messages.warning(request, 'Sepertinya ada yang salah! Cobalah lagi!', extra_tags='alert')
        return redirect(to_login_guru_views)

def to_admin_tambahsiswa_views(request):
    if request.session.has_key('namacook'):
        context = {
            "tbl_kelas": Tbl_kelas.objects.all(),
            "namauser": request.session['namacook'],
        }
        return render(request, "Guru/Admin/Siswa/AdminTambahSiswa.html", context)
    else:
        messages.warning(request, 'Sepertinya ada yang salah! Cobalah lagi!', extra_tags='alert')
        return redirect(to_login_guru_views)

def to_admin_editsiswa_views(request):
    if request.method == "POST":
        if request.session.has_key('namacook'):
            context = {
                "siswa": Tbl_siswa.objects.get(id_siswa=request.POST['idsiswa']),
                "tbl_kelas": Tbl_kelas.objects.all(),
                "namauser": request.session['namacook'],
            }
            return render(request, "Guru/Admin/Siswa/AdminEditSiswa.html", context)
        else:
            messages.warning(request, 'Sepertinya ada yang salah! Cobalah lagi!', extra_tags='alert')
            return redirect(to_login_guru_views)
    else:
        return redirect(to_login_guru_views)

def admin_tambahsiswa_views(request):
    if request.method == "POST":
        tbl_siswa_save = Tbl_siswa(
            id_siswa = request.POST['nis'],
            nama_siswa = request.POST['namas'],
            email_siswa = request.POST['emails'],
            id_kelas_id = request.POST['idkelass'],
            password_siswa = request.POST['passwords'],
            jumlahpoin_siswa = request.POST['poins'],
        )
        tbl_siswa_save.save()
        return redirect(to_admin_siswa_views)
    else:
        messages.warning(request, 'Sepertinya ada yang salah! Cobalah lagi!', extra_tags='alert')
        return redirect(login_guru_views)

def admin_editsiswa_views(request):
    if request.method == "POST":
        tbl_siswa = Tbl_siswa.objects.get(id_siswa=request.POST['nis'])    
        tbl_siswa.id_siswa = request.POST['nis']
        tbl_siswa.nama_siswa = request.POST['namas']
        tbl_siswa.email_siswa = request.POST['emails']
        tbl_siswa.id_kelas_id = request.POST['idkelass']
        tbl_siswa.password_siswa = request.POST['passwords']
        tbl_siswa.jumlahpoin_siswa = request.POST['poins']
        tbl_siswa.save()
        return redirect(to_admin_siswa_views)
    else:
        messages.warning(request, 'Sepertinya ada yang salah! Cobalah lagi!', extra_tags='alert')
        return redirect(login_guru_views)

def admin_hapussiswa_views(request):
    if request.method == "POST":
        tbl_siswa = Tbl_siswa.objects.get(id_siswa=request.POST['idsiswa'])
        tbl_siswa.delete()
        return redirect(to_admin_siswa_views)
    else:
        messages.warning(request, 'Sepertinya ada yang salah! Cobalah lagi!', extra_tags='alert')
        return redirect(login_guru_views)

def to_admin_kelas_views(request):
    if request.session.has_key('namacook'):
        context = {
            "tbl_kelas": Tbl_kelas.objects.all(),
            "tbl_siswa": Tbl_siswa.objects.all(),
            "namauser": request.session['namacook'],
        }
        return render(request, "Guru/Admin/Kelas/AdminKelas.html", context)
    else:
        messages.warning(request, 'Sepertinya ada yang salah! Cobalah lagi!', extra_tags='alert')
        return redirect(to_login_guru_views)

def to_admin_tambahkelas_views(request):
    if request.session.has_key('namacook'):
        context = {
            "nextkelas": len(Tbl_kelas.objects.all()) + 1,
            "namauser": request.session['namacook'],
        }
        return render(request, "Guru/Admin/Kelas/AdminTambahKelas.html", context)
    else:
        messages.warning(request, 'Sepertinya ada yang salah! Cobalah lagi!', extra_tags='alert')
        return redirect(to_login_guru_views)

def to_admin_editkelas_views(request):
    if request.method == "POST":
        if request.session.has_key('namacook'):
            context = {
                "kelas": Tbl_kelas.objects.get(id_kelas=request.POST['idkelas']),
                "namauser": request.session['namacook'],
            }
            return render(request, "Guru/Admin/Kelas/AdminEditKelas.html", context)
        else:
            messages.warning(request, 'Sepertinya ada yang salah! Cobalah lagi!', extra_tags='alert')
            return redirect(to_login_guru_views)
    else:
        return redirect(to_login_guru_views)

def admin_tambahkelas_views(request):
    if request.method == "POST":
        tbl_kelas_save = Tbl_kelas(
            id_kelas = request.POST['idkelas'],
            nama_kelas = request.POST['namak'],
            jumlah_siswa = request.POST['jumlahk'],
        )
        tbl_kelas_save.save()
        return redirect(to_admin_kelas_views)
    else:
        messages.warning(request, 'Sepertinya ada yang salah! Cobalah lagi!', extra_tags='alert')
        return redirect(login_guru_views)

def admin_editkelas_views(request):
    if request.method == "POST":
        tbl_kelas = Tbl_kelas.objects.get(id_kelas=request.POST['idkelas'])
        tbl_kelas.id_kelas = request.POST['idkelas']
        tbl_kelas.nama_kelas = request.POST['namak']
        tbl_kelas.jumlah_siswa = request.POST['jumlahk']
        tbl_kelas.save()
        return redirect(to_admin_kelas_views)
    else:
        messages.warning(request, 'Sepertinya ada yang salah! Cobalah lagi!', extra_tags='alert')
        return redirect(login_guru_views)

def admin_hapuskelas_views(request):
    if request.method == "POST":
        tbl_kelas = Tbl_kelas.objects.get(id_kelas=request.POST['idkelas'])
        tbl_kelas.delete()
        return redirect(to_admin_kelas_views)
    else:
        messages.warning(request, 'Sepertinya ada yang salah! Cobalah lagi!', extra_tags='alert')
        return redirect(login_guru_views)

def to_admin_acara_views(request):
    if request.session.has_key('namacook'):
        context = {
            "tbl_acara": Tbl_acara.objects.all(),
            "namauser": request.session['namacook'],
        }
        return render(request, "Guru/Admin/Acara/AdminAcara.html", context)
    else:
        messages.warning(request, 'Sepertinya ada yang salah! Cobalah lagi!', extra_tags='alert')
        return redirect(to_login_guru_views)

def to_admin_tambahacara_views(request):
    if request.session.has_key('namacook'):
        context = {
            "namauser": request.session['namacook'],
        }
        return render(request, "Guru/Admin/Acara/AdminTambahAcara.html", context)
    else:
        messages.warning(request, 'Sepertinya ada yang salah! Cobalah lagi!', extra_tags='alert')
        return redirect(to_login_guru_views)

def to_admin_editacara_views(request):
    if request.method == "POST":
        if request.session.has_key('namacook'):
            context = {
                "tbl_kategori": Tbl_kategori.objects.all(),
                "tbl_acara": Tbl_acara.objects.all(),
                "acara": Tbl_acara.objects.get(id_acara=request.POST['idacara']),
                "namauser": request.session['namacook'],
            }
            return render(request, "Guru/Admin/Acara/AdminEditAcara.html", context)
        else:
            messages.warning(request, 'Sepertinya ada yang salah! Cobalah lagi!', extra_tags='alert')
            return redirect(to_login_guru_views)
    else:
        return redirect(to_login_guru_views)

def admin_tambahacara_views(request):
    if request.method == "POST":
        tbl_acara_save = Tbl_acara(
            nama_acara = request.POST['namaa'],
            waktu_acara = request.POST['waktua'],
            keterangan_acara = request.POST['keta'],
            id_kategori_id = request.POST['idkat'],
        )
        tbl_acara_save.save()
        return redirect(to_admin_acara_views)
    else:
        messages.warning(request, 'Sepertinya ada yang salah! Cobalah lagi!', extra_tags='alert')
        return redirect(login_guru_views)

def admin_editacara_views(request):
    if request.method == "POST":
        tbl_acara = Tbl_acara.objects.get(id_acara=request.POST['idacara'])
        tbl_acara.nama_acara = request.POST['namaa']
        tbl_acara.waktu_acara = request.POST['waktua']
        tbl_acara.keterangan_acara = request.POST['keta']
        tbl_acara.id_kategori_id = request.POST['idkat']
        tbl_acara.save()
        return redirect(to_admin_acara_views)
    else:
        messages.warning(request, 'Sepertinya ada yang salah! Cobalah lagi!', extra_tags='alert')
        return redirect(login_guru_views)

def admin_hapusacara_views(request):
    if request.method == "POST":
        tbl_acara = Tbl_acara.objects.get(id_acara=request.POST['idacara'])
        tbl_acara.delete()
        return redirect(to_admin_acara_views)
    else:
        messages.warning(request, 'Sepertinya ada yang salah! Cobalah lagi!', extra_tags='alert')
        return redirect(login_guru_views)

def to_admin_pelajaran_views(request):
    if request.session.has_key('namacook'):
        context = {
            "tbl_jampel_start": Tbl_jampel_start.objects.all(),
            "tbl_jampel_end": Tbl_jampel_end.objects.all(),
            "namauser": request.session['namacook'],
        }
        return render(request, "Guru/Admin/Pelajaran/AdminPelajaran.html", context)
    else:
        messages.warning(request, 'Sepertinya ada yang salah! Cobalah lagi!', extra_tags='alert')
        return redirect(to_login_guru_views)

def to_admin_tambahpelajaran_views(request):
    if request.session.has_key('namacook'):
        context = {
            "namauser": request.session['namacook'],
        }
        return render(request, "Guru/Admin/Pelajaran/AdminTambahPelajaran.html", context)
    else:
        messages.warning(request, 'Sepertinya ada yang salah! Cobalah lagi!', extra_tags='alert')
        return redirect(to_login_guru_views)

def to_admin_editpelajaran_views(request):
    if request.method == "POST":
        if request.session.has_key('namacook'):
            context = {
                "jampel_start": Tbl_jampel_start.objects.get(id_jampel_start=request.POST['idstart']),
                "namauser": request.session['namacook'],
            }
            return render(request, "Guru/Admin/Pelajaran/AdminEditPelajaran.html", context)
        else:
            messages.warning(request, 'Sepertinya ada yang salah! Cobalah lagi!', extra_tags='alert')
            return redirect(to_login_guru_views)
    else:
        return redirect(to_login_guru_views)

def admin_tambahpelajaran_views(request):
    if request.method == "POST":
        tbl_jampel_start_save = Tbl_jampel_start(
            nama_jampel_start = request.POST['namap'],
            waktu_jampel_start = request.POST['waktup'],
        )
        tbl_jampel_start_save.save()
        tbl_jampel_end_save = Tbl_jampel_end(
            nama_jampel_end = request.POST['namap'],
            waktu_jampel_end = request.POST['waktup'],
        )
        tbl_jampel_end_save.save()
        return redirect(to_admin_pelajaran_views)
    else:
        messages.warning(request, 'Sepertinya ada yang salah! Cobalah lagi!', extra_tags='alert')
        return redirect(login_guru_views)

def admin_editpelajaran_views(request):
    if request.method == "POST":
        tbl_jampel_start = Tbl_jampel_start.objects.get(id_jampel_start=request.POST['idstart'])
        tbl_jampel_start.nama_jampel_start = request.POST['namap']
        tbl_jampel_start.waktu_jampel_start = request.POST['waktup']
        tbl_jampel_start.save()
        tbl_jampel_end = Tbl_jampel_end.objects.get(id_jampel_end=request.POST['idstart'])
        tbl_jampel_end.nama_jampel_end= request.POST['namap']
        tbl_jampel_end.waktu_jampel_end = request.POST['waktup']
        tbl_jampel_end.save()
        return redirect(to_admin_pelajaran_views)
    else:
        messages.warning(request, 'Sepertinya ada yang salah! Cobalah lagi!', extra_tags='alert')
        return redirect(login_guru_views)

def admin_hapuspelajaran_views(request):
    if request.method == "POST":
        tbl_jampel_start = Tbl_jampel_start.objects.get(id_jampel_start=request.POST['idstart'])
        tbl_jampel_start.delete()
        tbl_jampel_end = Tbl_jampel_end.objects.get(id_jampel_end=request.POST['idstart'])
        tbl_jampel_end.delete()
        return redirect(to_admin_pelajaran_views)
    else:
        messages.warning(request, 'Sepertinya ada yang salah! Cobalah lagi!', extra_tags='alert')
        return redirect(login_guru_views)

# Acara
def to_cta_views(request):
    if request.method == "POST":
        if request.POST['cta'].upper() == "CTA":
            context = {
                "acaras": Tbl_acara.objects.filter(id_kategori__exact="CTA"),
                "absens": Tbl_absen.objects.filter(id_siswa__exact=request.session['idcook']),
                "today": timezone.now(),
                "todaydate": timezone.now().date(),
            }
            try:
                request.session['gucook']
            except:
                return render(request, 'Siswa/CTAAcara.html', context)
            return render(request, 'Guru/Walas/CTAAcara.html', context)    
        else:
            messages.warning(request, 'Sepertinya ada yang salah! Cobalah lagi!', extra_tags='alert')
            return redirect(to_login_views)
    else:
        return redirect(to_login_views)

def to_re_views(request):
    if request.method == "POST":
        if request.POST['re'].upper() == "RE":
            context = {
                "acaras": Tbl_acara.objects.filter(id_kategori__exact="RE"),
                "absens": Tbl_absen.objects.filter(id_siswa__exact=request.session['idcook']),
                "today": timezone.now(),
                "todaydate": timezone.now().date(),
            }
            try:
                request.session['gucook']
            except:
                return render(request, 'Siswa/ReligiusAcara.html', context)
            return render(request, 'Guru/Walas/ReligiusAcara.html', context)
        else:
            messages.warning(request, 'Sepertinya ada yang salah! Cobalah lagi!', extra_tags='alert')
            return redirect(to_login_views)
    else:
        return redirect(to_login_views)

def to_di_views(request):
    if request.method == "POST":
        if request.POST['di'].upper() == "DI":
            context = {
                "acaras": Tbl_acara.objects.filter(id_kategori__exact="DI"),
                "absens": Tbl_absen.objects.filter(id_siswa__exact=request.session['idcook']),
                "today": timezone.now(),
                "todaydate": timezone.now().date(),
            }
            try:
                request.session['gucook']
            except:
                messages.warning(request, 'Sepertinya ada yang salah! Cobalah lagi!', extra_tags='alert')
                return redirect(to_login_guru_views)
            return render(request, 'Guru/Walas/DisiplinAcara.html', context)
        else:
            messages.warning(request, 'Sepertinya ada yang salah! Cobalah lagi!', extra_tags='alert')
            return redirect(to_login_views)
    else:
        return redirect(to_login_views)

def to_nonwalas_di_views(request):
    if request.session.has_key('idcook'):
        context = {
            "acaras": Tbl_acara.objects.filter(id_kategori__exact="DI"),
            "absens": Tbl_absen.objects.filter(id_siswa__exact=request.session['idcook']),
            "today": timezone.now(),
            "todaydate": timezone.now().date(),
        }
        try:
            request.session['gucook']
        except:
            messages.warning(request, 'Sepertinya ada yang salah! Cobalah lagi!', extra_tags='alert')
            return redirect(to_login_guru_views)
        return render(request, 'Guru/NonWalas_Guru/DisiplinAcara.html', context)
    else:
        messages.warning(request, 'Sepertinya ada yang salah! Cobalah lagi!', extra_tags='alert')
        return redirect(to_login_views)

# ajax
def checkpelajaran_views(request):
    if request.is_ajax and request.method == "GET":
        try:
            request.session['idacaracook']
        except:
            messages.warning(request, 'Sepertinya ada yang salah! Cobalah lagi!', extra_tags='alert')
            return redirect(to_login_guru_views)
        startaj = request.GET.get("startaj", None)
        endaj = request.GET.get("endaj", None)
        absen_amis = Tbl_absen_ami.objects.filter(Q(id_jampel_start_id=startaj), Q(id_jampel_end_id=endaj), Q(id_acara_id=request.session['idacaracook']))
        return JsonResponse({"valid":False}, status = 200)
    return JsonResponse({}, status = 400)