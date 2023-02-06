from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_urls', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='link',
            options={'ordering': ('-date_created',)},
        ),
    ]
