# Generated by Django 3.2.4 on 2021-11-13 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0005_auto_20211112_1841'),
        ('accounts', '0002_account_chatrooms'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='chatRooms',
            field=models.ManyToManyField(blank=True, to='chat.ChatRoom'),
        ),
    ]