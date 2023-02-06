from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    operations = [
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(max_length=2048)),
                ('alias', models.CharField(max_length=6, unique=True, validators=[django.core.validators.RegexValidator(code='invalid_alias', message='Alias can only contain lowercase alphabets, numerals, underscores and hyphens', regex='^[a-z0-9-_]+$')])),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Click',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clicked_date', models.DateField(auto_now_add=True)),
                ('clicks_count', models.PositiveIntegerField(default=0)),
                ('link', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_urls.link')),
            ],
        ),
    ]
