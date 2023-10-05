# Generated by Django 4.2.2 on 2023-06-18 11:26

# PURPOSE OF THIS MIGRATION
#
# This squashed migration was created for compatibility with Wagtail 4.0's migration from PageRevision 
# to a generic Revision model. The `0001_initial` migration in this project must continue to reference the old 
# PageRevision model and wagtailcore.0052_pagelogentry dependency to maintain a consistent migration history 
# for existing databases. On the flip side, new projects that run wagtail_ab_testing's migrations for the first time
# will encounter a PageRevision model that no longer exists which causes errors.
#
# The solution for new projects is to use this squashed migration file instead.
# This file contains no references to PageRevision and will migrate without errors.

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.migrations.operations.special
import django.db.models.deletion


# Migrated from wagtail_ab_testing.migrations.0007_grant_moderators_add_abtest_permission
def grant_moderators_add_abtest_permission(apps, schema_editor):
    ContentType = apps.get_model("contenttypes.ContentType")
    Permission = apps.get_model("auth.Permission")
    Group = apps.get_model("auth.Group")

    abtest_content_type, created = ContentType.objects.get_or_create(
        app_label="wagtail_ab_testing", model="abtest"
    )
    add_abtest_permission, created = Permission.objects.get_or_create(
        content_type=abtest_content_type, codename="add_abtest"
    )

    moderators_group = Group.objects.filter(name="Moderators").first()
    if moderators_group:
        moderators_group.permissions.add(add_abtest_permission)


class Migration(migrations.Migration):
    replaces = [
        ("wagtail_ab_testing", "0001_initial"),
        ("wagtail_ab_testing", "0002_abtesthourlylog"),
        ("wagtail_ab_testing", "0003_abtest_winning_variant"),
        ("wagtail_ab_testing", "0004_started_at_and_duration"),
        ("wagtail_ab_testing", "0005_hypothesis_and_created_by"),
        ("wagtail_ab_testing", "0006_sample_size_min_value"),
        ("wagtail_ab_testing", "0007_grant_moderators_add_abtest_permission"),
        ("wagtail_ab_testing", "0008_finished_status"),
        ("wagtail_ab_testing", "0009_rename_variant_to_version"),
        ("wagtail_ab_testing", "0010_rename_treatment_to_variant"),
        ("wagtail_ab_testing", "0011_rename_treatment_to_variant_data"),
        ("wagtail_ab_testing", "0012_abtest_variant_revision"),
    ]

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("wagtailcore", "0078_referenceindex"),
    ]

    operations = [
        migrations.CreateModel(
            name="AbTest",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("goal_event", models.CharField(max_length=255)),
                (
                    "sample_size",
                    models.PositiveIntegerField(
                        validators=[django.core.validators.MinValueValidator(1)]
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("draft", "Draft"),
                            ("running", "Running"),
                            ("paused", "Paused"),
                            ("cancelled", "Cancelled"),
                            ("finished", "Finished"),
                            ("completed", "Completed"),
                        ],
                        default="draft",
                        max_length=20,
                    ),
                ),
                (
                    "goal_page",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="wagtailcore.page",
                    ),
                ),
                (
                    "page",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="ab_tests",
                        to="wagtailcore.page",
                    ),
                ),
                (
                    "variant_revision",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="wagtailcore.revision",
                    ),
                ),
                (
                    "winning_version",
                    models.CharField(
                        choices=[("control", "Control"), ("variant", "Variant")],
                        max_length=9,
                        null=True,
                    ),
                ),
                ("current_run_started_at", models.DateTimeField(null=True)),
                ("first_started_at", models.DateTimeField(null=True)),
                (
                    "previous_run_duration",
                    models.DurationField(default=datetime.timedelta(0)),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("hypothesis", models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name="AbTestHourlyLog",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "version",
                    models.CharField(
                        choices=[("control", "Control"), ("variant", "Variant")],
                        max_length=9,
                    ),
                ),
                ("date", models.DateField()),
                ("hour", models.PositiveSmallIntegerField()),
                ("participants", models.PositiveIntegerField(default=0)),
                ("conversions", models.PositiveIntegerField(default=0)),
                (
                    "ab_test",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="hourly_logs",
                        to="wagtail_ab_testing.abtest",
                    ),
                ),
            ],
            options={"ordering": ["ab_test", "version", "date", "hour"]},
        ),
        migrations.AlterUniqueTogether(
            name="abtesthourlylog",
            unique_together={("ab_test", "version", "date", "hour")},
        ),
        migrations.RunPython(
            code=grant_moderators_add_abtest_permission,
            reverse_code=django.db.migrations.operations.special.RunPython.noop,
        ),
    ]
