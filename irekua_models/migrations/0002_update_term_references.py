from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('irekua_models', '0001_initial'),
        ('irekua_terms', '0001_initial'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AlterField(
                    model_name='model',
                    name='terms',
                    field=models.ManyToManyField(blank=True, help_text='Terms that the model uses for its predictions.', to='irekua_terms.Term'),
                ),
                migrations.AlterField(
                    model_name='modelprediction',
                    name='labels',
                    field=models.ManyToManyField(help_text='Terms used as labels to describe the predicted event.', to='irekua_terms.Term', verbose_name='labels'),
                ),
            ],
            database_operations=[],
        ),
    ]
