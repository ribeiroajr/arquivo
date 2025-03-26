# views_graficos.py
import plotly.express as px
import pandas as pd
from django.shortcuts import render # type: ignore
from ..models import Docs

def gerar_graficos(request):
    # Queryset para buscar todos os documentos
    docs = Docs.objects.all()

    # Convertendo queryset para dataframe
    data = {
        'doc_data': [doc.doc_data for doc in docs],
        'doc_corrente_ano': [doc.doc_corrente_ano for doc in docs],
        'doc_eliminacao_ano': [doc.doc_eliminacao_ano for doc in docs],
        'doc_numero': [doc.doc_numero for doc in docs],
        'new_file_sigad': [doc.new_file_sigad for doc in docs],
        'doc_intermediario_ano': [doc.doc_intermediario_ano for doc in docs],
        'doc_destinacao_final_ano': [doc.doc_destinacao_final_ano for doc in docs],
        'doc_obs_ano': [doc.doc_obs_ano for doc in docs],
    }
    df = pd.DataFrame(data)

    # Gerar gráficos usando Plotly
    fig_corrente = px.histogram(df, x='doc_corrente_ano', title='Distribuição de Anos Correntes')
    fig_eliminacao = px.histogram(df, x='doc_eliminacao_ano', title='Distribuição de Anos de Eliminação')
    fig_intermediario = px.histogram(df, x='doc_intermediario_ano', title='Distribuição de Anos Intermediários')
    fig_destinacao_final = px.histogram(df, x='doc_destinacao_final_ano', title='Distribuição de Anos de Destinação Final')

    # Convertendo os gráficos para HTML
    graph_corrente = fig_corrente.to_html(full_html=False)
    graph_eliminacao = fig_eliminacao.to_html(full_html=False)
    graph_intermediario = fig_intermediario.to_html(full_html=False)
    graph_destinacao_final = fig_destinacao_final.to_html(full_html=False)

    context = {
        'graph_corrente': graph_corrente,
        'graph_eliminacao': graph_eliminacao,
        'graph_intermediario': graph_intermediario,
        'graph_destinacao_final': graph_destinacao_final,
    }

    return render(request, 'graficos.html', context)
