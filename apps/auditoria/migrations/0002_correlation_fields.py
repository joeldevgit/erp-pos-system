# Generated manually for senior observability/audit trail
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auditoria", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="auditlog",
            name="correlation_id",
            field=models.CharField(blank=True, db_index=True, max_length=64),
        ),
        migrations.AddField(
            model_name="auditlog",
            name="request_id",
            field=models.CharField(blank=True, db_index=True, max_length=64),
        ),
        migrations.AddField(
            model_name="auditlog",
            name="ip_address",
            field=models.GenericIPAddressField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="auditlog",
            name="user_agent",
            field=models.TextField(blank=True),
        ),
    ]
