# Generated by Django 3.2 on 2022-12-26 15:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fio', models.CharField(default='', max_length=255)),
                ('email', models.EmailField(default='', max_length=254)),
                ('passport_number', models.CharField(max_length=9)),
                ('passport_data', models.TextField()),
                ('created_at', models.DateTimeField()),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='account', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Bank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank', models.CharField(max_length=150)),
                ('bik', models.CharField(max_length=9)),
                ('account', models.CharField(max_length=20)),
                ('inn', models.CharField(max_length=10)),
                ('kpp', models.CharField(max_length=9)),
                ('money_transfer_comission', models.IntegerField()),
                ('info', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(default='', max_length=254)),
                ('account', models.CharField(max_length=20)),
                ('inn', models.CharField(max_length=10)),
                ('kpp', models.CharField(max_length=9)),
                ('bank_bik', models.CharField(max_length=9)),
                ('transfer_purpose', models.TextField()),
                ('money', models.CharField(max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('bank', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='company_bank', to='core.bank')),
            ],
        ),
        migrations.CreateModel(
            name='MoneyTransferToClient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_user', models.CharField(max_length=255)),
                ('from_account', models.CharField(max_length=30)),
                ('to_user', models.CharField(max_length=255)),
                ('to_account', models.CharField(max_length=30)),
                ('bank', models.CharField(max_length=255)),
                ('transfer_purpose', models.TextField()),
                ('money', models.CharField(max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='MoneyTransferToCompany',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fio', models.CharField(max_length=255)),
                ('user_account', models.CharField(max_length=30)),
                ('user_bank', models.CharField(max_length=255)),
                ('company', models.CharField(max_length=255)),
                ('company_account', models.CharField(max_length=30)),
                ('company_bank', models.CharField(max_length=255)),
                ('transfer_purpose', models.TextField()),
                ('money', models.CharField(max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='TransferToCompanyData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('money', models.CharField(max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('to_company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='from_client_to_company_transfers', to='core.company')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='to_company_transfers', to='core.account')),
            ],
        ),
        migrations.CreateModel(
            name='TransferToClientData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('money', models.CharField(max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('to_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='from_client_transfers', to='core.account')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='to_client_transfers', to='core.account')),
            ],
        ),
        migrations.CreateModel(
            name='MoneyAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account', models.CharField(max_length=20)),
                ('type', models.CharField(choices=[('??????????????????', '??????????????????')], max_length=255)),
                ('status', models.CharField(choices=[('????????????', '????????????'), ('????????????', '????????????')], max_length=255)),
                ('currency', models.CharField(choices=[('RUR', 'RUR'), ('USD', 'USD'), ('EUR', 'EUR')], max_length=255)),
                ('balance', models.CharField(max_length=20)),
                ('user_account', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='money_account', to='core.account')),
            ],
        ),
    ]
