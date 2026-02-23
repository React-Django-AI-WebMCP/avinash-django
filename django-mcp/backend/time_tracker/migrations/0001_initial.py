import uuid

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
            name="Project",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("deleted_at", models.DateTimeField(db_index=True, null=True, blank=True)),
                ("name", models.CharField(max_length=255)),
                ("color", models.CharField(default="#6b7280", max_length=7)),
            ],
            options={
                "db_table": "time_tracker_project",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="TimeEntry",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("deleted_at", models.DateTimeField(db_index=True, null=True, blank=True)),
                ("date", models.DateField(db_index=True)),
                ("start_time", models.TimeField()),
                ("end_time", models.TimeField()),
                ("title", models.CharField(max_length=255)),
                (
                    "entry_type",
                    models.CharField(
                        choices=[
                            ("logged", "Logged"),
                            ("mentioned", "Mentioned"),
                            ("integrated", "Integrated"),
                        ],
                        db_index=True,
                        default="logged",
                        max_length=20,
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="time_entries",
                        to="time_tracker.project",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="time_entries",
                        to=settings.AUTH_USER_MODEL,
                        db_index=True,
                    ),
                ),
            ],
            options={
                "db_table": "time_tracker_time_entry",
                "ordering": ["date", "start_time"],
            },
        ),
        migrations.AddIndex(
            model_name="timeentry",
            index=models.Index(fields=["user", "date"], name="tt_te_user_date_idx"),
        ),
    ]
