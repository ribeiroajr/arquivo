from pyexpat.errors import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .views_log import registrar_acao_usuario, registrar_acao_usuario_deletar
from ..forms import TipoForm
from ..models import Tipo
from django.contrib import messages


@login_required
def tipo_lista(request):
    dataset = Tipo.objects.all()
    context = {"dataset": dataset}
    # print(dataset)
    return render(request, 'tipo/lista.html', context)

@login_required
def tipo_novo(request):
    user_id = request.user.id
    user = request.user

    if request.method == 'POST':
        form = TipoForm(request.POST)
        if form.is_valid():
            # form.save()
            instance = form.save()
            registrar_acao_usuario(request, instance, f'cadastrou')  # Passa a instância do objeto Ano e a ação
     
            return redirect('tipo_lista')  # Redirecione para a lista após criar
    else:
        # form = TipoForm()
        form = TipoForm(initial={'fk_user': user_id})

    
    return render(request, 'tipo/criar.html', {'form': form})


# @login_required
# def tipo_detalhes(request, pk):
#     tipo_ob = get_object_or_404(AnoForm, pk=pk)
#     return render(request, 'tipo/detalhes.html', {'tipo_ob': tipo_ob})

@login_required
def tipo_editar(request, id):
    user_id = request.user.id
    user = request.user

    context ={}
    tipo_ob = get_object_or_404(Tipo, id=id)
    if request.method == 'POST':
        form = TipoForm(request.POST, instance=tipo_ob)
        if form.is_valid():
            # form.save()
            instance = form.save()
            registrar_acao_usuario(request, instance, f'editou')  # Passa a instância do objeto Ano e a ação
     
            return redirect('tipo_lista')
    else:
        # form = TipoForm(instance=tipo_ob)
        form = TipoForm(instance=tipo_ob, initial={'fk_user': user_id})

    context = {
        'form': form,
        'tipo_ob': tipo_ob
    }
    return render(request, 'tipo/editar.html', context)

@login_required
def tipo_delete(request, id):
    context ={}
    tipo_ob = get_object_or_404(Tipo, id=id)
    if request.method == 'POST':
        # tipo_ob.delete()
        instance = tipo_ob  # Salva a instância antes de excluir
        tipo_id = instance.id  # Obtém o ID do objeto Ano antes de excluir

        tipo_ob.delete()
        # registrar_acao_usuario(request, instance, 'deletou')  # Passa a instância do objeto Ano
        registrar_acao_usuario_deletar(request, f'Tipo', tipo_id)  # Passa o ID do objeto Ano deletado

        messages.success(request, 'Registro excluído com sucesso.')
        return redirect('tipo_lista')
    
    context = {
        'tipo_ob': tipo_ob
    }
    
    return render(request, 'tipo/excluir.html', context)

