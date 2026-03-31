import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.db.models.functions import TruncDate
from datetime import date, timedelta
from ..models import Docs, LogAcaoUsuario


@login_required
def gerar_graficos(request):
    """Gráficos técnicos de distribuição de anos (página existente)."""
    qs = Docs.objects.values(
        'doc_corrente_ano',
        'doc_eliminacao_ano',
        'doc_intermediario_ano',
        'doc_destinacao_final_ano',
    )
    df = pd.DataFrame.from_records(qs)

    context = {
        'graph_corrente':         px.histogram(df, x='doc_corrente_ano',        title='Distribuição de Anos Correntes').to_html(full_html=False),
        'graph_eliminacao':       px.histogram(df, x='doc_eliminacao_ano',       title='Distribuição de Anos de Eliminação').to_html(full_html=False),
        'graph_intermediario':    px.histogram(df, x='doc_intermediario_ano',    title='Distribuição de Anos Intermediários').to_html(full_html=False),
        'graph_destinacao_final': px.histogram(df, x='doc_destinacao_final_ano', title='Distribuição de Anos de Destinação Final').to_html(full_html=False),
    }
    return render(request, 'graficos.html', context)


@login_required
def dashboard(request):
    """Dashboard com visão geral do acervo e produtividade."""

    # Primeiro gráfico emite o JS do Plotly inline (offline); os demais reutilizam
    opts_first = dict(full_html=False, include_plotlyjs=True)
    opts       = dict(full_html=False, include_plotlyjs=False)

    # --- 1. Documentos por tipo (pizza) ---
    tipo_qs = (
        Docs.objects
        .exclude(fk_tipo__isnull=True)
        .values('fk_tipo__tipo')
        .annotate(total=Count('id'))
        .order_by('-total')
    )
    if tipo_qs:
        df_tipo = pd.DataFrame(tipo_qs)
        fig_tipo = px.pie(
            df_tipo, names='fk_tipo__tipo', values='total',
            title='Documentos por Tipo',
            hole=0.35,
        )
        fig_tipo.update_traces(textposition='inside', textinfo='percent+label')
        fig_tipo.update_layout(showlegend=False, margin=dict(t=40, b=10, l=10, r=10))
        graph_tipo = fig_tipo.to_html(**opts_first)
    else:
        graph_tipo = '<p class="text-muted">Sem dados.</p>'

    # --- 2. Documentos por caixa (barras) — top 20 ---
    caixa_qs = (
        Docs.objects
        .exclude(fk_caixa__isnull=True)
        .values('fk_caixa__caixa')
        .annotate(total=Count('id'))
        .order_by('-total')[:20]
    )
    if caixa_qs:
        df_caixa = pd.DataFrame(caixa_qs)
        fig_caixa = px.bar(
            df_caixa, x='fk_caixa__caixa', y='total',
            title='Documentos por Caixa (top 20)',
            labels={'fk_caixa__caixa': 'Caixa', 'total': 'Qtd'},
            color='total', color_continuous_scale='Blues',
        )
        fig_caixa.update_layout(coloraxis_showscale=False, margin=dict(t=40, b=60, l=10, r=10))
        graph_caixa = fig_caixa.to_html(**opts)
    else:
        graph_caixa = '<p class="text-muted">Sem dados.</p>'

    # --- 3. Cadastros por dia — últimos 60 dias (linha) ---
    inicio = date.today() - timedelta(days=60)
    dia_qs = (
        LogAcaoUsuario.objects
        .filter(acao='cadastrou', create_at__date__gte=inicio)
        .annotate(dia=TruncDate('create_at'))
        .values('dia')
        .annotate(total=Count('id'))
        .order_by('dia')
    )
    if dia_qs:
        df_dia = pd.DataFrame(dia_qs)
        fig_dia = px.line(
            df_dia, x='dia', y='total',
            title='Cadastros por Dia (últimos 60 dias)',
            labels={'dia': 'Data', 'total': 'Cadastros'},
            markers=True,
        )
        fig_dia.update_layout(margin=dict(t=40, b=40, l=10, r=10))
        graph_dia = fig_dia.to_html(**opts)
    else:
        graph_dia = '<p class="text-muted">Sem registros nos últimos 60 dias.</p>'

    # --- 4. Produtividade por usuário no mês atual (barras horizontais) ---
    inicio_mes = date.today().replace(day=1)
    prod_qs = (
        LogAcaoUsuario.objects
        .filter(acao='cadastrou', create_at__date__gte=inicio_mes)
        .values('fk_user__username')
        .annotate(total=Count('id'))
        .order_by('total')
    )
    if prod_qs:
        df_prod = pd.DataFrame(prod_qs)
        fig_prod = px.bar(
            df_prod, x='total', y='fk_user__username',
            orientation='h',
            title='Cadastros por Usuário (mês atual)',
            labels={'fk_user__username': 'Usuário', 'total': 'Cadastros'},
            color='total', color_continuous_scale='Greens',
        )
        fig_prod.update_layout(coloraxis_showscale=False, margin=dict(t=40, b=20, l=10, r=10))
        graph_prod = fig_prod.to_html(**opts)
    else:
        graph_prod = '<p class="text-muted">Sem cadastros no mês atual.</p>'

    # --- Totais gerais ---
    totais = {
        'total_docs':      Docs.objects.count(),
        'docs_conferidos': Docs.objects.filter(status_doc=True).count(),
        'docs_mes':        LogAcaoUsuario.objects.filter(acao='cadastrou', create_at__date__gte=inicio_mes).count(),
    }

    context = {
        'graph_tipo':  graph_tipo,
        'graph_caixa': graph_caixa,
        'graph_dia':   graph_dia,
        'graph_prod':  graph_prod,
        'totais':      totais,
    }
    return render(request, 'dashboard.html', context)
