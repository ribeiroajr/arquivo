from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .views_log import registrar_acao_usuario, registrar_acao_usuario_deletar
from django.contrib.auth import authenticate, login as login_django
from django.contrib.auth import login as login_django
from django.contrib.auth import logout
from django.contrib.auth import views as auth_views
from ..forms import OmForm
from ..models import Om

# Create your views here.


@login_required
def om_lista(request):
    dataset = Om.objects.all()
    context = {"dataset": dataset}
    # print(dataset)
    return render(request, 'om/lista.html', context)

@login_required
def om_novo(request):
    user_id = request.user.id
    user = request.user

    if request.method == 'POST':
        form = OmForm(request.POST)
        if form.is_valid():
            # form.save()
            instance = form.save()
            registrar_acao_usuario(request, instance, f'cadastrou')  # Passa a instância do objeto Ano e a ação
    
            return redirect('om_lista')  # Redirecione para a lista após criar
    else:
        form = OmForm()
        form = OmForm(initial={'fk_user': user_id})

    
    return render(request, 'om/criar.html', {'form': form})


# @login_required
# def om_detalhes(request, pk):
#     om_ob = get_object_or_404(AnoForm, pk=pk)
#     return render(request, 'om/detalhes.html', {'om_ob': om_ob})

@login_required
def om_editar(request, id):
    user_id = request.user.id
    user = request.user
    context ={}
    om_ob = get_object_or_404(Om, id=id)
    if request.method == 'POST':
        form = OmForm(request.POST, instance=om_ob)
        if form.is_valid():
            # form.save()
            instance = form.save()
            registrar_acao_usuario(request, instance, f'editou')  # Passa a instância do objeto Ano e a ação
     
            return redirect('om_lista')
    else:
        # form = OmForm(instance=om_ob)
        form = OmForm(instance=om_ob, initial={'fk_user': user_id})

    context = {
        'form': form,
        'om_ob': om_ob
    }
    return render(request, 'om/editar.html', context)

@login_required
def om_delete(request, id):
    context ={}
    om_ob = get_object_or_404(Om, id=id)
    if request.method == 'POST':
        # om_ob.delete()
        instance = om_ob  # Salva a instância antes de excluir
        om_id = instance.id  # Obtém o ID do objeto Ano antes de excluir

        om_ob.delete()
        # registrar_acao_usuario(request, instance, 'deletou')  # Passa a instância do objeto Ano
        registrar_acao_usuario_deletar(request, f'Om', om_id) 

        # messages.success(request, 'Registro excluído com sucesso.')
        return redirect('om_lista')
    
    context = {
        'om_ob': om_ob
    }
    
    return render(request, 'om/excluir.html', context)

