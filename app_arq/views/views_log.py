from ..models import LogAcaoUsuario
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from django.db.models import Count, Q
from django.db.models.functions import TruncDate
from collections import defaultdict
from datetime import date, timedelta


@login_required
def listar_logs(request):
    hoje = date.today()
    data_inicio_str = request.GET.get('data_inicio', '')
    data_fim_str    = request.GET.get('data_fim', '')
    usuario_id      = request.GET.get('usuario', '')

    try:
        data_inicio = date.fromisoformat(data_inicio_str) if data_inicio_str else hoje - timedelta(days=30)
    except ValueError:
        data_inicio = hoje - timedelta(days=30)

    try:
        data_fim = date.fromisoformat(data_fim_str) if data_fim_str else hoje
    except ValueError:
        data_fim = hoje

    qs = (
        LogAcaoUsuario.objects
        .filter(create_at__date__gte=data_inicio, create_at__date__lte=data_fim)
        .select_related('fk_user')
    )

    # Filtro opcional por usuário
    usuario_selecionado = None
    if usuario_id:
        try:
            usuario_selecionado = int(usuario_id)
            qs = qs.filter(fk_user__id=usuario_selecionado)
        except (ValueError, TypeError):
            usuario_selecionado = None

    rows = (
        qs
        .annotate(data=TruncDate('create_at'))
        .values('fk_user__id', 'fk_user__username', 'data')
        .annotate(
            cadastrou=Count('acao', filter=Q(acao='cadastrou')),
            editou=Count('acao', filter=Q(acao='editou')),
            deletou=Count('acao', filter=Q(acao='deletou')),
        )
        .order_by('fk_user__username', 'data')
    )

    dados_usuarios = defaultdict(lambda: {'dias': [], 'total_cadastrou': 0, 'total_editou': 0, 'total_deletou': 0})
    for row in rows:
        u = row['fk_user__username']
        dados_usuarios[u]['dias'].append(row)
        dados_usuarios[u]['total_cadastrou'] += row['cadastrou']
        dados_usuarios[u]['total_editou']    += row['editou']
        dados_usuarios[u]['total_deletou']   += row['deletou']

    total_geral = {
        'cadastrou': sum(v['total_cadastrou'] for v in dados_usuarios.values()),
        'editou':    sum(v['total_editou']    for v in dados_usuarios.values()),
        'deletou':   sum(v['total_deletou']   for v in dados_usuarios.values()),
    }

    # Lista de usuários que têm logs (para o select)
    usuarios = (
        User.objects
        .filter(logacaousuario__isnull=False)
        .distinct()
        .order_by('username')
    )

    context = {
        'dados_usuarios':      dict(dados_usuarios),
        'total_geral':         total_geral,
        'data_inicio':         data_inicio.isoformat(),
        'data_fim':            data_fim.isoformat(),
        'usuarios':            usuarios,
        'usuario_selecionado': usuario_selecionado,
    }

    return render(request, 'relatorio.html', context)


def registrar_acao_usuario(request, obj_instance, acao):
    user = request.user
    if request.user.is_authenticated:
        LogAcaoUsuario(
            fk_user=user,
            acao=acao,
            objeto=obj_instance.__class__.__name__,
            objeto_id=obj_instance.id
        ).save()


def registrar_acao_usuario_deletar(request, objeto, id):
    user = request.user
    if request.user.is_authenticated:
        LogAcaoUsuario(fk_user=user, acao='deletou', objeto=objeto, objeto_id=id).save()
