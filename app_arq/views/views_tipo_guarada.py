from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from app_arq.forms import Tipo_guardaForm
from ..models import TipoGuarda
from ..forms import Tipo_guardaForm
from .views_log import registrar_acao_usuario, registrar_acao_usuario_deletar

@login_required
def tipo_guarda_novo(request):
    user_id = request.user.id
    user = request.user

    if request.method == 'POST':
        form = Tipo_guardaForm(request.POST)
        if form.is_valid():
            # form.save()
            instance = form.save()
            registrar_acao_usuario(request, instance, f'cadastrou')  # Passa a instância do objeto Ano e a ação
      
            return redirect('tipo_guarda_lista')  # Redirecione para a lista após criar
    else:
        # form = Tipo_guardaForm()
        form = Tipo_guardaForm(initial={'fk_user': user_id})

    
    return render(request, 'tipo_guarda/criar.html', {'form': form})

@login_required
def tipo_guarda_lista(request):
    dataset = TipoGuarda.objects.all()
    context = {"dataset": dataset}
    # print(dataset)
    return render(request, 'tipo_guarda/lista.html', context)


# @login_required
# def tipo_guarda_detalhes(request, pk):
#     tipo_guarda_ob = get_object_or_404(AnoForm, pk=pk)
#     return render(request, 'tipo_guarda/detalhes.html', {'tipo_guarda_ob': tipo_guarda_ob})

@login_required
def tipo_guarda_editar(request, id):
    user_id = request.user.id
    user = request.user

    context ={}
    tipo_guarda_ob = get_object_or_404(TipoGuarda, id=id)
    if request.method == 'POST':
        form = Tipo_guardaForm(request.POST, instance=tipo_guarda_ob)
        if form.is_valid():
            # form.save()
            instance = form.save()
            registrar_acao_usuario(request, instance, f'editou')  # Passa a instância do objeto Ano e a ação
     
            return redirect('tipo_guarda_lista')
    else:
        # form = Tipo_guardaForm(instance=tipo_guarda_ob)
        form = Tipo_guardaForm(instance=tipo_guarda_ob, initial={'fk_user': user_id})

    context = {
        'form': form,
        'tipo_guarda_ob': tipo_guarda_ob
    }
    return render(request, 'tipo_guarda/editar.html', context)

@login_required
def tipo_guarda_delete(request, id):
    user_id = request.user.id
    user = request.user
    context ={}
    tipo_guarda_ob = get_object_or_404(TipoGuarda, id=id)
    if request.method == 'POST':
        # tipo_guarda_ob.delete()
        instance = tipo_guarda_ob  # Salva a instância antes de excluir
        tipo_guarda_id = instance.id  # Obtém o ID do objeto Ano antes de excluir

        tipo_guarda_ob.delete()
        # registrar_acao_usuario(request, instance, 'deletou')  # Passa a instância do objeto Ano
        registrar_acao_usuario_deletar(request, f'TipoGuarda', tipo_guarda_id) 
        # messages.success(request, 'Registro excluído com sucesso.')
        return redirect('tipo_guarda_lista')
    
    context = {
        'tipo_guarda_ob': tipo_guarda_ob
    }
    
    return render(request, 'tipo_guarda/excluir.html', context)

