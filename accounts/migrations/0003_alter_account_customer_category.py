# Generated by Django 4.1.1 on 2022-09-24 04:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_account_department'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='customer_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.customercategory'),
        ),
    ]