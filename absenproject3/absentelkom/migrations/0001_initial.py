# Generated by Django 3.0.7 on 2020-06-07 15:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tbl_absen',
            fields=[
                ('id_absen', models.AutoField(primary_key=True, serialize=False)),
                ('waktu_absensi', models.DateTimeField()),
            ],
            options={
                'db_table': 'tbl_absen',
            },
        ),
        migrations.CreateModel(
            name='Tbl_akses',
            fields=[
                ('id_akses', models.AutoField(primary_key=True, serialize=False)),
                ('nama_akses', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'tbl_akses',
            },
        ),
        migrations.CreateModel(
            name='Tbl_guru',
            fields=[
                ('id_guru', models.CharField(max_length=9, primary_key=True, serialize=False)),
                ('nama_guru', models.CharField(max_length=50)),
                ('email_guru', models.CharField(max_length=50)),
                ('password_guru', models.CharField(max_length=100)),
                ('id_akses', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='absentelkom.Tbl_akses')),
            ],
            options={
                'db_table': 'tbl_guru',
            },
        ),
        migrations.CreateModel(
            name='Tbl_jampel_end',
            fields=[
                ('id_jampel_end', models.IntegerField(primary_key=True, serialize=False)),
                ('nama_jampel_end', models.CharField(max_length=25)),
                ('waktu_jampel_end', models.TimeField()),
            ],
            options={
                'db_table': 'tbl_jampel_end',
            },
        ),
        migrations.CreateModel(
            name='Tbl_jampel_start',
            fields=[
                ('id_jampel_start', models.IntegerField(primary_key=True, serialize=False)),
                ('nama_jampel_start', models.CharField(max_length=25)),
                ('waktu_jampel_start', models.TimeField()),
            ],
            options={
                'db_table': 'tbl_jampel_start',
            },
        ),
        migrations.CreateModel(
            name='Tbl_kategori',
            fields=[
                ('id_kategori', models.CharField(max_length=3, primary_key=True, serialize=False)),
                ('nama_kategori', models.CharField(max_length=18)),
            ],
            options={
                'db_table': 'tbl_kategori',
            },
        ),
        migrations.CreateModel(
            name='Tbl_kelas',
            fields=[
                ('id_kelas', models.CharField(max_length=5, primary_key=True, serialize=False)),
                ('nama_kelas', models.CharField(max_length=9)),
                ('jumlah_siswa', models.IntegerField()),
            ],
            options={
                'db_table': 'tbl_kelas',
            },
        ),
        migrations.CreateModel(
            name='Tbl_validasi',
            fields=[
                ('id_validasi', models.AutoField(primary_key=True, serialize=False)),
                ('waktu_validasi', models.DateTimeField()),
                ('penambahan_poin', models.IntegerField()),
                ('id_absen', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='absentelkom.Tbl_absen')),
                ('id_guru', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='absentelkom.Tbl_guru')),
            ],
            options={
                'db_table': 'tbl_validasi',
            },
        ),
        migrations.CreateModel(
            name='Tbl_siswa',
            fields=[
                ('id_siswa', models.CharField(max_length=9, primary_key=True, serialize=False)),
                ('nama_siswa', models.CharField(max_length=50)),
                ('email_siswa', models.CharField(max_length=50)),
                ('password_siswa', models.CharField(max_length=100)),
                ('jumlahpoin_siswa', models.IntegerField()),
                ('id_kelas', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='absentelkom.Tbl_kelas')),
            ],
            options={
                'db_table': 'tbl_siswa',
            },
        ),
        migrations.CreateModel(
            name='Tbl_acara',
            fields=[
                ('id_acara', models.AutoField(primary_key=True, serialize=False)),
                ('nama_acara', models.CharField(max_length=30)),
                ('waktu_acara', models.DateTimeField()),
                ('id_kategori', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='absentelkom.Tbl_kategori')),
            ],
            options={
                'db_table': 'tbl_acara',
            },
        ),
        migrations.CreateModel(
            name='Tbl_absen_ami',
            fields=[
                ('id_absen_ami', models.AutoField(primary_key=True, serialize=False)),
                ('kehadiran', models.BooleanField()),
                ('kerapihan', models.BooleanField()),
                ('kebersihan', models.BooleanField()),
                ('penambahan_poin', models.IntegerField()),
                ('id_acara', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='absentelkom.Tbl_acara')),
                ('id_jampel_end', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='absentelkom.Tbl_jampel_end')),
                ('id_jampel_start', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='absentelkom.Tbl_jampel_start')),
                ('id_siswa', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='absentelkom.Tbl_siswa')),
            ],
            options={
                'db_table': 'tbl_absen_ami',
            },
        ),
        migrations.AddField(
            model_name='tbl_absen',
            name='id_acara',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='absentelkom.Tbl_acara'),
        ),
        migrations.AddField(
            model_name='tbl_absen',
            name='id_siswa',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='absentelkom.Tbl_siswa'),
        ),
    ]
