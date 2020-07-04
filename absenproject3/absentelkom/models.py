from django.db import models
from django.utils import timezone

# Create your models here.
class Tbl_kelas(models.Model):
    id_kelas = models.CharField(primary_key=True, max_length=5)
    nama_kelas = models.CharField(max_length=9)
    jumlah_siswa = models.IntegerField()

    class Meta:
        db_table = "tbl_kelas"

class Tbl_siswa(models.Model):
    id_siswa = models.CharField(primary_key=True, max_length=9)
    id_kelas = models.ForeignKey(Tbl_kelas, on_delete=models.CASCADE, null=True)
    nama_siswa = models.CharField(max_length=50)
    email_siswa = models.CharField(max_length=50)
    password_siswa = models.CharField(max_length=100)
    jumlahpoin_siswa = models.IntegerField()

    class Meta:
        db_table = "tbl_siswa"

class Tbl_akses(models.Model):
    id_akses = models.AutoField(primary_key=True)
    nama_akses = models.CharField(max_length=20)

    class Meta:
        db_table = "tbl_akses"

class Tbl_guru(models.Model):
    id_guru = models.CharField(primary_key=True, max_length=9)
    id_akses = models.ForeignKey(Tbl_akses, on_delete=models.CASCADE, null=True)
    nama_guru = models.CharField(max_length=50)
    email_guru = models.CharField(max_length=50)
    password_guru = models.CharField(max_length=100)   

    class Meta:
        db_table = "tbl_guru"

class Tbl_kategori(models.Model):
    id_kategori = models.CharField(primary_key=True, max_length=3)
    nama_kategori = models.CharField(max_length=18)

    class Meta:
        db_table = "tbl_kategori"

class Tbl_acara(models.Model):
    id_acara = models.AutoField(primary_key=True)
    id_kategori = models.ForeignKey(Tbl_kategori, on_delete=models.CASCADE, null=True)
    nama_acara = models.CharField(max_length=30)
    waktu_acara = models.DateTimeField()
    keterangan_acara = models.CharField(max_length=400, default=None)

    class Meta:
        db_table = "tbl_acara"

class Tbl_jampel_start(models.Model):
    id_jampel_start = models.AutoField(primary_key=True)
    nama_jampel_start = models.CharField(max_length=25)
    waktu_jampel_start = models.TimeField()

    class Meta:
        db_table = "tbl_jampel_start"

class Tbl_jampel_end(models.Model):
    id_jampel_end = models.AutoField(primary_key=True)
    nama_jampel_end = models.CharField(max_length=25)
    waktu_jampel_end = models.TimeField()

    class Meta:
        db_table = "tbl_jampel_end"

class Tbl_absen_ami(models.Model):
    id_absen_ami = models.AutoField(primary_key=True)
    id_jampel_start = models.ForeignKey(Tbl_jampel_start, on_delete=models.CASCADE, null=True)
    id_jampel_end = models.ForeignKey(Tbl_jampel_end, on_delete=models.CASCADE, null=True)
    id_acara = models.ForeignKey(Tbl_acara, on_delete=models.CASCADE, null=True)
    id_siswa = models.ForeignKey(Tbl_siswa, on_delete=models.CASCADE, null=True)
    id_guru = models.ForeignKey(Tbl_guru, on_delete=models.CASCADE, null=True)
    kehadiran = models.BooleanField()
    kerapihan = models.BooleanField()
    kebersihan = models.BooleanField()
    penambahan_poin = models.IntegerField()

    class Meta:
        db_table = "tbl_absen_ami"

class Tbl_absen(models.Model):
    id_absen = models.AutoField(primary_key=True)
    id_acara = models.ForeignKey(Tbl_acara, on_delete=models.CASCADE, null=True)
    id_siswa = models.ForeignKey(Tbl_siswa, on_delete=models.CASCADE, null=True)
    waktu_absensi = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.id_absen:
            self.waktu_absensi = timezone.now()
        return super(Tbl_absen, self).save(*args, **kwargs)

    class Meta:
        db_table = "tbl_absen"

class Tbl_validasi(models.Model):
    id_validasi = models.AutoField(primary_key=True)
    id_absen = models.OneToOneField(Tbl_absen, on_delete=models.CASCADE, null=True)
    id_guru = models.ForeignKey(Tbl_guru, on_delete=models.CASCADE)
    waktu_validasi = models.DateTimeField()
    penambahan_poin = models.IntegerField()

    def save(self, *args, **kwargs):
        if not self.id_validasi:
            self.waktu_validasi = timezone.now()
        return super(Tbl_validasi, self).save(*args, **kwargs)

    class Meta:
        db_table = "tbl_validasi"