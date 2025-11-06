

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('order', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name_plural': 'categories',
                'ordering': ['order', 'name'],
            },
        ),
        migrations.AlterField(
            model_name='menu',
            name='image_url',
            field=models.URLField(blank=True, max_length=500),
        ),
        migrations.AlterField(
            model_name='menu',
            name='price',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='menu',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='menus', to='main.category'),
        ),
    ]
