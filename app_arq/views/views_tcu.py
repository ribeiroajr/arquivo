from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required

from .views_log import registrar_acao_usuario, registrar_acao_usuario_deletar
from ..forms import TcuForm
from ..models import Tcu

@login_required
def tcu_lista(request):
    dataset = Tcu.objects.all()
    context = {"dataset": dataset}
    # print(dataset)
    return render(request, 'tcu/lista.html', context)

@login_required
def tcu_novo(request):
    user_id = request.user.id
    user = request.user

    if request.method == 'POST':
        form = TcuForm(request.POST)
        if form.is_valid():
            # form.save()
            instance = form.save()
            registrar_acao_usuario(request, instance, f'cadastrou')  # Passa a instância do objeto Ano e a ação
     
            return redirect('tcu_lista')  # Redirecione para a lista após criar
    else:
        # form = TcuForm()
        form = TcuForm(initial={'fk_user': user_id})

    
    return render(request, 'tcu/criar.html', {'form': form})


# @login_required
# def tcu_detalhes(request, pk):
#     tcu_ob = get_object_or_404(AnoForm, pk=pk)
#     return render(request, 'tcu/detalhes.html', {'tcu_ob': tcu_ob})

@login_required
def tcu_editar(request, id):
    user_id = request.user.id
    user = request.user

    context ={}
    tcu_ob = get_object_or_404(Tcu, id=id)
    if request.method == 'POST':
        form = TcuForm(request.POST, instance=tcu_ob)
        if form.is_valid():
            # form.save()
            instance = form.save()
            registrar_acao_usuario(request, instance, f'editou')  # Passa a instância do objeto Ano e a ação
      
            return redirect('tcu_lista')
    else:
        # form = TcuForm(instance=tcu_ob)
        form = TcuForm(instance=tcu_ob, initial={'fk_user': user_id})

    context = {
        'form': form,
        'tcu_ob': tcu_ob
    }
    return render(request, 'tcu/editar.html', context)

@login_required
def tcu_delete(request, id):
    user_id = request.user.id
    user = request.user
    context ={}
    tcu_ob = get_object_or_404(Tcu, id=id)
    if request.method == 'POST':
        # tcu_ob.delete()
        instance = tcu_ob  # Salva a instância antes de excluir
        tcu_id = instance.id  # Obtém o ID do objeto Ano antes de excluir

        tcu_ob.delete()
        # registrar_acao_usuario(request, instance, 'deletou')  # Passa a instância do objeto Ano
        registrar_acao_usuario_deletar(request, f'Tcu', tcu_id) 
        # messages.success(request, 'Registro excluído com sucesso.')
        return redirect('tcu_lista')
    
    context = {
        'tcu_ob': tcu_ob
    }
    
    return render(request, 'tcu/excluir.html', context)

