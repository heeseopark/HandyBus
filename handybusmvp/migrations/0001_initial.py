# Generated by Django 4.2 on 2024-03-05 15:46

from django.db import migrations, models
import django.db.models.deletion
import handybusmvp.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Concert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('idol', models.CharField(max_length=255)),
                ('date', models.DateField()),
                ('location', models.CharField(max_length=255)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField(blank=True, null=True)),
                ('image', models.ImageField(upload_to=handybusmvp.models.concert_image_path)),
                ('status', models.CharField(choices=[('ready_for_reservation', '예약 준비 단계'), ('pre_reservation', '선예약 모집 단계'), ('pre_reservation_complete', '선예약 모집 완료'), ('reservation', '실예약 모집 단계'), ('reservation_complete', '실예약 모집 완료'), ('paused', '모집 일시중지 단계'), ('canceled', '대절 취소'), ('finished', '콘서트 완료')], default='ready_for_reservation', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='GatheringPlace',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region', models.CharField(choices=[('daegu', '대구'), ('daejeon', '대전'), ('busan', '부산'), ('changwon', '창원'), ('sejong', '세종'), ('cheongju', '청주')], max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('location', models.CharField(max_length=255, null=True)),
                ('time', models.TimeField(null=True)),
                ('direction', models.CharField(choices=[('upward', '상행'), ('downward', '하행')], max_length=255)),
                ('reservation_fixed', models.BooleanField()),
                ('concert', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='handybusmvp.concert')),
            ],
        ),
        migrations.CreateModel(
            name='PrivacyConsent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.CharField(max_length=50)),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('phone_number', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('head_count', models.IntegerField(default=1)),
                ('has_paid_pre_reserve_price', models.BooleanField()),
                ('has_paid_reserve_price', models.BooleanField()),
                ('preferred_fallback_option', models.CharField(choices=[('refund', '본인 계좌로 환불'), ('pay_extra', '추가금 지불 후 탑승 및 타지역 경유')], default='refund', max_length=50, verbose_name='인원 미달시 희망하는 진행방향')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('is_in_charge', models.BooleanField()),
                ('refund_account', models.CharField(max_length=255)),
                ('concert', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='handybusmvp.concert')),
                ('gathering_place_down', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='reservations_down', to='handybusmvp.gatheringplace')),
                ('gathering_place_up', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='reservations_up', to='handybusmvp.gatheringplace')),
                ('privacy_consent_version', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='handybusmvp.privacyconsent')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='handybusmvp.user')),
            ],
        ),
        migrations.CreateModel(
            name='Pricing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region', models.CharField(choices=[('daegu', '대구'), ('daejeon', '대전'), ('busan', '부산'), ('changwon', '창원'), ('sejong', '세종'), ('cheongju', '청주')], max_length=255)),
                ('pre_reserve_price', models.DecimalField(decimal_places=0, max_digits=10)),
                ('round_trip_price', models.DecimalField(decimal_places=0, max_digits=10)),
                ('upbound_price', models.DecimalField(decimal_places=0, max_digits=10)),
                ('downbound_price', models.DecimalField(decimal_places=0, max_digits=10)),
                ('concert', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='handybusmvp.concert')),
            ],
        ),
        migrations.CreateModel(
            name='PreReservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_upbound', models.BooleanField()),
                ('is_downbound', models.BooleanField()),
                ('region', models.CharField(choices=[('daegu', '대구'), ('daejeon', '대전'), ('busan', '부산'), ('changwon', '창원'), ('sejong', '세종'), ('cheongju', '청주')], max_length=255)),
                ('head_count', models.IntegerField(default=1)),
                ('has_paid', models.BooleanField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('concert', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='handybusmvp.concert')),
                ('privacy_consent_version', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='handybusmvp.privacyconsent')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='handybusmvp.user')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=0, max_digits=10)),
                ('paid_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('need_to_check', '확인 필요'), ('completed', '완료'), ('failed', '실패')], default='need_to_check', max_length=255)),
                ('pre_reservation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='pre_payments', to='handybusmvp.prereservation')),
                ('reservation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='payments', to='handybusmvp.reservation')),
            ],
        ),
        migrations.CreateModel(
            name='OpenChatUrl',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region', models.CharField(choices=[('daegu', '대구'), ('daejeon', '대전'), ('busan', '부산'), ('changwon', '창원'), ('sejong', '세종'), ('cheongju', '청주')], max_length=255)),
                ('open_chat_url', models.CharField(max_length=511)),
                ('concert', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='handybusmvp.concert')),
            ],
        ),
        migrations.CreateModel(
            name='EventDiscount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sns_share_image', models.ImageField(blank=True, null=True, upload_to=handybusmvp.models.sns_image_path)),
                ('reservation', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='handybusmvp.reservation')),
            ],
        ),
        migrations.CreateModel(
            name='Companion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('phone_number', models.CharField(max_length=50)),
                ('reservation', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='reservation_companions', to='handybusmvp.reservation')),
            ],
        ),
    ]
