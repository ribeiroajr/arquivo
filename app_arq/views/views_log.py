from ..models import LogAcaoUsuario
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from django.db.models import Count, Q
from django.db.models.functions import TruncDate
from collections import defaultdict


@login_required
def listar_logs(request):
    # Uma única query: todos os logs agrupados por usuário + dia
    rows = (
        LogAcaoUsuario.objects
        .select_related('fk_user')
        .annotate(data=TruncDate('create_at'))
        .values('fk_user__id', 'fk_user__username', 'data')
        .annotate(
            cadastrou=Count('acao', filter=Q(acao='cadastrou')),
            editou=Count('acao', filter=Q(acao='editou')),
            deletou=Count('acao', filter=Q(acao='deletou')),
        )
        .order_by('fk_user__username', 'data')
    )

    # Reagrupa em {username: [linha_por_dia, ...]} para manter compatibilidade com o template
    logs_por_usuario_por_dia = defaultdict(list)
    for row in rows:
        logs_por_usuario_por_dia[row['fk_user__username']].append(row)

    context = {
        'logs_por_usuario_por_dia': dict(logs_por_usuario_por_dia),
    }

    return render(request, 'relatorio.html', context)


def registrar_acao_usuario(request, obj_instance, acao):
    user = request.user
    if request.user.is_authenticated:
        log = LogAcaoUsuario(
            fk_user=user,
            acao=acao,
            objeto=obj_instance.__class__.__name__,
            objeto_id=obj_instance.id
        )
        log.save()


def registrar_acao_usuario_deletar(request, objeto, id):
    user = request.user
    if request.user.is_authenticated:
        log = LogAcaoUsuario(fk_user=user, acao='deletou', objeto=objeto, objeto_id=id)
        log.save()
