# Generated by Django 4.1.1 on 2022-09-24 17:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_account_customer_category'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customercategory',
            options={'ordering': ['minimum_order'], 'verbose_name_plural': 'customer categories'},
        ),
        migrations.RemoveField(
            model_name='customercategory',
            name='maximum_order',
        ),
    ]
