# Generated by Django 3.2.9 on 2021-11-28 08:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bondapp', '0002_auto_20211128_1734'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ylddeviation',
            name='fk_date',
            field=models.ForeignKey(db_column='fk_date', on_delete=django.db.models.deletion.CASCADE, to='bondapp.bondyld'),
        ),
    ]
