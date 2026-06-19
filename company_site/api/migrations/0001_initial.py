from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='HomepageStats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('projects_executed', models.PositiveIntegerField()),
                ('field_personnel', models.PositiveIntegerField()),
                ('clients_partners', models.PositiveIntegerField()),
                ('operational_locations', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('is_hidden', models.BooleanField(default=False)),
                ('author', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={'ordering': ['-created_at']},
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('status', models.CharField(choices=[('planned', 'Planned'), ('active', 'Active'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='planned', max_length=20)),
                ('client', models.CharField(max_length=255)),
                ('scope', models.TextField()),
                ('execution', models.JSONField(default=list, help_text='Execution steps as a JSON list')),
                ('outcome', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('text', models.TextField()),
                ('first_image', models.ImageField(blank=True, null=True, upload_to='services/')),
                ('second_image', models.ImageField(blank=True, null=True, upload_to='services/')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='projects/')),
                ('order', models.PositiveIntegerField(default=0)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='api.project')),
            ],
            options={'ordering': ['order', 'id']},
        ),
        migrations.CreateModel(
            name='NewsImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='news/')),
                ('order', models.PositiveIntegerField(default=0)),
                ('news', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='api.news')),
            ],
            options={'ordering': ['order', 'id']},
        ),
    ]
