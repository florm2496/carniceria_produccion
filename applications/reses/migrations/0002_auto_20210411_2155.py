# Generated by Django 2.1.15 on 2021-04-12 00:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_userforeignkey.models.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PagoCliente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.BooleanField(default=True)),
                ('fc', models.DateTimeField(auto_now_add=True)),
                ('fm', models.DateTimeField(auto_now=True)),
                ('monto', models.FloatField(default=0.0)),
                ('medio', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='reses.MedioPago')),
                ('uc', django_userforeignkey.models.fields.UserForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('um', django_userforeignkey.models.fields.UserForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'pago_cliente',
                'verbose_name_plural': 'pagos_clientes',
            },
        ),
        migrations.AlterField(
            model_name='encventareses',
            name='saldada',
            field=models.BooleanField(default=True),
        ),
    ]
