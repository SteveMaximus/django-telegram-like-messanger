from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_add_video_field'),
    ]

    operations = [
        migrations.CreateModel(
            name='VideoRoom',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('initiator', models.CharField(blank=True, max_length=150)),
                ('callee', models.CharField(blank=True, max_length=150)),
                ('offer', models.TextField(blank=True, null=True)),
                ('answer', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='IceCandidate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender', models.CharField(max_length=20)),
                ('candidate', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('room', models.ForeignKey(on_delete=models.deletion.CASCADE, related_name='candidates', to='users.videoroom')),
            ],
        ),
    ]
