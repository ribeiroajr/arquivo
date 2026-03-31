from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_arq', '0002_docs_status_doc'),
    ]

    operations = [
        # BaseModel.create_at — usado em TruncDate nos logs
        migrations.AlterField(
            model_name='logacaousuario',
            name='create_at',
            field=models.DateTimeField(auto_now_add=True, null=True, db_index=True),
        ),
        # Docs.doc_data — filtro de busca e ordenação
        migrations.AlterField(
            model_name='docs',
            name='doc_data',
            field=models.DateField(blank=True, null=True, verbose_name='Data do documento', db_index=True),
        ),
        # Docs.doc_eliminacao_ano — usado em relatórios e gráficos
        migrations.AlterField(
            model_name='docs',
            name='doc_eliminacao_ano',
            field=models.IntegerField(blank=True, null=True, verbose_name='Ano de eliminação', db_index=True),
        ),
        # Docs.status_doc — filtro de conferência
        migrations.AlterField(
            model_name='docs',
            name='status_doc',
            field=models.BooleanField(default=False, verbose_name='Conferido', db_index=True),
        ),
    ]
