# Generated by Django 4.1.1 on 2022-09-25 16:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100, unique=True)),
                ('discount_percentage', models.FloatField(default=0)),
                ('department', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='accounts.department')),
            ],
            options={
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100)),
                ('price', models.IntegerField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='products/')),
                ('stock', models.IntegerField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.category')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
    ]
