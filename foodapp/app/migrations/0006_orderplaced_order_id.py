# Generated by Django 5.2.3 on 2025-06-27 17:25

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_orderplaced'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderplaced',
            name='order_id',
            field=models.UUIDField(db_index=True, default=uuid.uuid4, editable=False),
        ),
    ]
