# Generated by Django 3.1 on 2020-09-10 08:57

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uu', models.CharField(default=uuid.uuid4, max_length=255)),
                ('total_number', models.IntegerField(default=0)),
                ('url', models.CharField(max_length=255, null=True)),
                ('email', models.CharField(max_length=255, null=True)),
                ('total_cost', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('is_new', models.BooleanField(default=True)),
                ('is_payed', models.BooleanField(default=False)),
                ('created_at', models.DateField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SocialNetwork',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discount', models.IntegerField(default=0)),
                ('name', models.CharField(max_length=255, null=True)),
                ('icon', models.ImageField(null=True, upload_to='services/')),
                ('slogan', models.CharField(max_length=255, null=True)),
                ('created_at', models.DateField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True)),
                ('css_class', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tarif',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('price_w_discount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('min', models.IntegerField(default=0)),
                ('max', models.IntegerField(default=0)),
                ('description', models.TextField(blank=True, null=True)),
                ('service', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tarifs', to='cp.service')),
            ],
            options={
                'ordering': ['price'],
            },
        ),
        migrations.AddField(
            model_name='service',
            name='social_network',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='services', to='cp.socialnetwork'),
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_id', models.CharField(blank=True, max_length=255, null=True)),
                ('payment_url', models.TextField(blank=True, null=True)),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Сумма')),
                ('status', models.BooleanField(default=False, verbose_name='Статус платежа')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата создания')),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cp.order')),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
        migrations.AddField(
            model_name='order',
            name='service',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cp.service'),
        ),
        migrations.AddField(
            model_name='order',
            name='social_network',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cp.socialnetwork'),
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to='cp.status'),
        ),
        migrations.AddField(
            model_name='order',
            name='tarif',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cp.tarif'),
        ),
    ]
