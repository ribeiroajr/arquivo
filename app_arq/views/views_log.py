from ..models import LogAcaoUsuario
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from django.db.models import Count, Q  # Adicione esta linha
from django.db.models.functions import TruncDate


def listar_logs(request):
    # Obter todos os usuários para listar os logs separadamente por usuário
    usuarios = User.objects.all()
    
    # Criar um dicionário para armazenar os logs de cada usuário por dia
    logs_por_usuario_por_dia = {}
    
    # Iterar sobre cada usuário
    for usuario in usuarios:
        # Filtrar os logs do usuário e agrupá-los por dia
        logs_usuario_por_dia = (
            LogAcaoUsuario.objects.filter(fk_user=usuario)
            .annotate(data=TruncDate('create_at'))
            .values('data')
            .annotate(
                cadastrou=Count('acao', filter=Q(acao='Cadastrou')),
                editou=Count('acao', filter=Q(acao='Editou')),
                deletou=Count('acao', filter=Q(acao='Deletou'))
            )
            .order_by('data')
        )
        logs_por_usuario_por_dia[usuario] = logs_usuario_por_dia
    
    context = {
        'logs_por_usuario_por_dia': logs_por_usuario_por_dia
    }
    
    return render(request, 'relatorio.html', context)



# @login_required
# def registrar_acao_usuario(request, acao):
#     user_id = request.user.id
#     user = request.user
#     user = User.objects.get(id=user_id)  # Recupera o usuário com base no ID
#     print(user_id)
#     print(acao)
#     if request.user.is_authenticated:
#         log = LogAcaoUsuario(fk_user=user, acao=acao)  # Passe a instância de User para fk_user
#         log.save()

# @login_required
# def registrar_acao_usuario(request, obj_instance, acao):
#     user = request.user
#     if request.user.is_authenticated:
#         log = LogAcaoUsuario(fk_user=user, acao=f'{user} - {acao}', objeto=obj_instance.__class__.__name__, objeto_id=obj_instance.id)
#         log.save()


def registrar_acao_usuario(request, obj_instance, acao):
    user = request.user
    if request.user.is_authenticated:
        log = LogAcaoUsuario(
            fk_user=user,
            # acao=f'{user} - {acao}',
            acao = acao,
            objeto=obj_instance.__class__.__name__,
            objeto_id=obj_instance.id
        )
        log.save()


def registrar_acao_usuario_deletar(request, objeto, id):
    user = request.user
    if request.user.is_authenticated:
        log = LogAcaoUsuario(fk_user=user, acao=f'deletou', objeto=objeto, objeto_id=id)
        log.save()





