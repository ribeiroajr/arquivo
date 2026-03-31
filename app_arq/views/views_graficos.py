# views_graficos.py
import plotly.express as px
import pandas as pd
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..models import Docs


@login_required
def gerar_graficos(request):
    # Busca apenas os campos necessários — sem carregar objetos completos
    qs = Docs.objects.values(
        'doc_corrente_ano',
        'doc_eliminacao_ano',
        'doc_intermediario_ano',
        'doc_destinacao_final_ano',
    )

    df = pd.DataFrame.from_records(qs)

    fig_corrente       = px.histogram(df, x='doc_corrente_ano',       title='Distribuição de Anos Correntes')
    fig_eliminacao     = px.histogram(df, x='doc_eliminacao_ano',      title='Distribuição de Anos de Eliminação')
    fig_intermediario  = px.histogram(df, x='doc_intermediario_ano',   title='Distribuição de Anos Intermediários')
    fig_destinacao     = px.histogram(df, x='doc_destinacao_final_ano', title='Distribuição de Anos de Destinação Final')

    context = {
        'graph_corrente':       fig_corrente.to_html(full_html=False),
        'graph_eliminacao':     fig_eliminacao.to_html(full_html=False),
        'graph_intermediario':  fig_intermediario.to_html(full_html=False),
        'graph_destinacao_final': fig_destinacao.to_html(full_html=False),
    }

    return render(request, 'graficos.html', context)
