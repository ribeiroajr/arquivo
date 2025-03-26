from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .views_log import registrar_acao_usuario, registrar_acao_usuario_deletar
from ..forms import StatusForm
from ..models import Status




@login_required
def status_lista(request):
    dataset = Status.objects.all()
    context = {"dataset": dataset}
    # print(dataset)
    return render(request, 'status/lista.html', context)

@login_required
def status_novo(request):
    user_id = request.user.id
    user = request.user

    if request.method == 'POST':
        form = StatusForm(request.POST)
        if form.is_valid():
            # form.save()
            instance = form.save()
            registrar_acao_usuario(request, instance, f'cadastrou')  # Passa a instância do objeto Ano e a ação
     
            return redirect('status_lista')  # Redirecione para a lista após criar
    else:
        # form = StatusForm()
        form = StatusForm(initial={'fk_user': user_id})

    
    return render(request, 'status/criar.html', {'form': form})


# @login_required
# def status_detalhes(request, pk):
#     status_ob = get_object_or_404(AnoForm, pk=pk)
#     return render(request, 'status/detalhes.html', {'status_ob': status_ob})

@login_required
def status_editar(request, id):
    user_id = request.user.id
    user = request.user
    
    context ={}
    status_ob = get_object_or_404(Status, id=id)
    if request.method == 'POST':
        form = StatusForm(request.POST, instance=status_ob)
        if form.is_valid():
            # form.save()
            instance = form.save()
            registrar_acao_usuario(request, instance, f'editou')  # Passa a instância do objeto Ano e a ação
            

            return redirect('status_lista')
    else:
        # form = StatusForm(instance=status_ob)
        form = StatusForm(instance=status_ob, initial={'fk_user': user_id})

    context = {
        'form': form,
        'status_ob': status_ob
    }
    return render(request, 'status/editar.html', context)

@login_required
def status_delete(request, id):
    context ={}
    status_ob = get_object_or_404(Status, id=id)
    if request.method == 'POST':
        # status_ob.delete()
        instance = status_ob  # Salva a instância antes de excluir
        status_id = instance.id  # Obtém o ID do objeto Ano antes de excluir

        status_ob.delete()
        # registrar_acao_usuario(request, instance, 'deletou')  # Passa a instância do objeto Ano
        registrar_acao_usuario_deletar(request, f'Status', status_id) 

        # messages.success(request, 'Registro excluído com sucesso.')
        return redirect('status_lista')
    
    context = {
        'status_ob': status_ob
    }
    
    return render(request, 'status/excluir.html', context)

