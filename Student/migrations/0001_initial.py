# Generated by Django 3.2.4 on 2021-08-07 08:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('Id', models.AutoField(primary_key=True, serialize=False)),
                ('Name', models.CharField(max_length=30)),
                ('Category', models.CharField(max_length=5)),
                ('Quantity', models.IntegerField()),
                ('AuthorName', models.CharField(max_length=30)),
                ('YearOfPublished', models.DecimalField(decimal_places=0, max_digits=4)),
            ],
        ),
        migrations.CreateModel(
            name='ReserveItem',
            fields=[
                ('Id', models.AutoField(primary_key=True, serialize=False)),
                ('Copies', models.IntegerField()),
                ('DateOfIssue', models.DateField()),
                ('DateOfReturn', models.DateField()),
                ('ItemId', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Student.item')),
                ('UserId', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
