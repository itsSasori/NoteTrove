# Generated by Django 4.1.4 on 2023-07-21 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('note', '0012_alter_customer_email_alter_room_department_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='quantity',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='room',
            name='price',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]
