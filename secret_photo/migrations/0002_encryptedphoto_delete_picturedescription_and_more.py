# Generated by Django 4.1.6 on 2023-07-30 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('secret_photo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EncryptedPhoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('encrypted_image', models.BinaryField()),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='PictureDescription',
        ),
        migrations.AlterField(
            model_name='customuser',
            name='user_key',
            field=models.CharField(default='7571c8c5909d4f4698731b33c01a997f', max_length=33),
        ),
    ]