# Generated by Django 3.0.6 on 2021-08-24 17:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Student', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reserveitem',
            name='Copies',
        ),
        migrations.AddField(
            model_name='reserveitem',
            name='Category',
            field=models.CharField(default=True, max_length=5),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='item',
            name='YearOfPublished',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='reserveitem',
            name='ItemId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Student.Item'),
        ),
        migrations.AlterField(
            model_name='reserveitem',
            name='UserId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]