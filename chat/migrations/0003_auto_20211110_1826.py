# Generated by Django 3.2.4 on 2021-11-11 02:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_alter_chatroom_users'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ('timestamp',)},
        ),
        migrations.AlterField(
            model_name='message',
            name='room',
            field=models.CharField(max_length=255),
        ),
        migrations.DeleteModel(
            name='chatRoom',
        ),
    ]
