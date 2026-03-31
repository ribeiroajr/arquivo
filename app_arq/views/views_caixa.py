from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .views_log import registrar_acao_usuario, registrar_acao_usuario_deletar
from ..forms import CaixaForm
from ..models import Caixa

#dataset = Caixa.objects.filter(fk_status=1)
@login_required
def caixa_lista(request):
    from django.db.models import Count, Case, When, IntegerField
    dataset = Caixa.objects.select_related('fk_ano', 'fk_status').all()
    totais = Caixa.objects.aggregate(
        qtd_cx_aberta=Count(Case(When(fk_status=1, then=1), output_field=IntegerField())),
        qtd_cx_fechada=Count(Case(When(fk_status=2, then=1), output_field=IntegerField())),
        qtd_cx_conferida=Count(Case(When(fk_status=3, then=1), output_field=IntegerField())),
    )
    context = {"dataset": dataset, **totais}
    return render(request, 'caixa/lista.html', context)

@login_required
def caixa_novo(request):
    user_id = request.user.id
    user = request.user
    if request.method == 'POST':
        form = CaixaForm(request.POST)
        if form.is_valid():
            # form.save()
            instance = form.save()
            registrar_acao_usuario(request, instance, f'cadastrou')  # Passa a instância do objeto Ano e a ação
      
            return redirect('caixa_lista')  # Redirecione para a lista após criar
    else:
        # form = CaixaForm()
        form = CaixaForm(initial={'fk_user': user_id})
        
    
    return render(request, 'caixa/criar.html', {'form': form})


# @login_required
# def caixa_detalhes(request, pk):
#     caixa_ob = get_object_or_404(AnoForm, pk=pk)
#     return render(request, 'ano/detalhes.html', {'caixa_ob': caixa_ob})

@login_required
def caixa_editar(request, id):
    user_id = request.user.id
    user = request.user
    context ={}
    caixa_ob = get_object_or_404(Caixa, id=id)
    if request.method == 'POST':
        form = CaixaForm(request.POST, instance=caixa_ob)
        if form.is_valid():
            # form.save()
            instance = form.save()
            registrar_acao_usuario(request, instance, f'editou')  # Passa a instância do objeto Ano e a ação
     
            return redirect('caixa_lista')
    else:
        # form = CaixaForm(instance=caixa_ob)
        form = CaixaForm(instance=caixa_ob, initial={'fk_user': user_id})

    context = {
        'form': form,
        'caixa_ob': caixa_ob
    }
    return render(request, 'caixa/editar.html', context)

@login_required
def caixa_delete(request, id):
    context ={}
    caixa_ob = get_object_or_404(Caixa, id=id)
    if request.method == 'POST':
        # caixa_ob.delete()
        instance = caixa_ob  # Salva a instância antes de excluir
        caixa_id = instance.id  # Obtém o ID do objeto Ano antes de excluir

        caixa_ob.delete()
        # registrar_acao_usuario(request, instance, 'deletou')  # Passa a instância do objeto Ano
        registrar_acao_usuario_deletar(request, f'Caixa', caixa_id) 
        # messages.success(request, 'Registro excluído com sucesso.')
        return redirect('caixa_lista')
    
    context = {
        'caixa_ob': caixa_ob
    }
    
    return render(request, 'caixa/excluir.html', context)

