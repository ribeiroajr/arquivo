from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from ..forms import CodigosForm
from ..models import Codigos
from django.http import JsonResponse
from django.core.paginator import Paginator
from .views_log import registrar_acao_usuario, registrar_acao_usuario_deletar


# Create your views here.
#@login_required
def cod_lista(request):
    dataset = Codigos.objects.all()
    # codigos_pag = Paginator(dataset, 10)
    # page_num = request.GET.get('page')
    # page = codigos_pag.get_page(page_num)
    context = {"dataset": dataset}
    # print(dataset)
    return render(request, 'codigos/lista.html', context)

@login_required
def cod_novo(request):
    user_id = request.user.id
    user = request.user
    if request.method == 'POST':
        form = CodigosForm(request.POST)
        if form.is_valid():
            # form.save()
            instance = form.save()
            registrar_acao_usuario(request, instance, f'cadastrou')  # Passa a instância do objeto Ano e a ação
     
            return redirect('cod_lista')  # Redirecione para a lista após criar
    else:
        # form = CodigosForm()
        form = CodigosForm(initial={'fk_user': user_id})

    
    return render(request, 'codigos/criar.html', {'form': form})


@login_required
def cod_editar(request, id):
    user_id = request.user.id
    user = request.user

    context ={}
    cod_ob = get_object_or_404(Codigos, id=id)
    if request.method == 'POST':
        form = CodigosForm(request.POST, instance=cod_ob)
        if form.is_valid():
            # form.save()
            instance = form.save()
            registrar_acao_usuario(request, instance, f'editou')  # Passa a instância do objeto Ano e a ação
    
            return redirect('cod_lista')
    else:
        # form = CodigosForm(instance=cod_ob)
        form = CodigosForm(instance=cod_ob, initial={'fk_user': user_id})

    context = {
        'form': form,
        'cod_ob': cod_ob
    }
    return render(request, 'codigos/editar.html', context)

@login_required
def cod_delete(request, id):
    context ={}
    cod_ob = get_object_or_404(Codigos, id=id)
    if request.method == 'POST':
        # cod_ob.delete()
        instance = cod_ob  # Salva a instância antes de excluir
        cod_id = instance.id  # Obtém o ID do objeto Ano antes de excluir

        cod_ob.delete()
        # registrar_acao_usuario(request, instance, 'deletou')  # Passa a instância do objeto Ano
        registrar_acao_usuario_deletar(request, f'Codigos', cod_id) 

        # messages.success(request, 'Registro excluído com sucesso.')
        return redirect('cod_lista')
    
    context = {
        'cod_ob': cod_ob
    }
    
    return render(request, 'codigos/excluir.html', context)



def sgc_ajax_load_related_data(request):
    codigo_id = int(request.GET.get('codigo_id'))
    print(f'codigo_id - {codigo_id}')
    print( type(codigo_id))

    # Recupere o objeto de Código correspondente ao ID
    # codigo = Codigos.objects.filter(id=codigo_id).all()
    codigo = Codigos.objects.filter(id=codigo_id).first()

    # codigo = get_object_or_404(Codigos, pk=codigo_id)
    # codigo = Codigos.objects.get(pk=codigo_id)
    print(f'codigo - {codigo}')
    print(f'codigo fase_corrente_ano - {codigo.fase_corrente_ano}')
    print(f'codigo fase_intermediaria_ano - {codigo.fase_intermediaria_ano}')
    print(f'codigo destinacao_final_ano - {codigo.destinacao_final_ano}')
    print(f'codigo observacoes_ano - {codigo.observacoes_ano}')
    print(f'fk_cod_guarda - {codigo.fk_tipo_guarda.tipo_guarda_descricao}')
#    print(f'cod_guarda_descricao - {codigo.fk_cod_guarda.cod_guarda_descricao}')
    
#    print(f'codigo observacoes_ano - {codigo.observacoes_ano}')
    doc_eliminacao_ano = (codigo.fase_corrente_ano + codigo.fase_intermediaria_ano + codigo.destinacao_final_ano + codigo.observacoes_ano)

    # Construa o dicionário de dados para retornar como JSON
    data = {
        'doc_corrente_ano': codigo.fase_corrente_ano,
        'doc_intermediario_ano': codigo.fase_intermediaria_ano,
        'doc_destinacao_final_ano': codigo.destinacao_final_ano,
        'doc_obs_ano': codigo.observacoes_ano,
        'doc_eliminacao_ano' : doc_eliminacao_ano,
        'tipo_guarda_descricao' : codigo.fk_tipo_guarda.tipo_guarda_descricao,
   #     'cod_guarda_descricao' : codigo.fk_cod_guarda.cod_guarda_descricao,
	    'fk_tipo_guarda' : codigo.fk_tipo_guarda.id,
    }
    print(f'data - {data}')
    return JsonResponse(data)

@login_required
def pagination(request):
    return render(request, 'pagination.html')

# data - {'doc_corrente_ano': None, 'doc_intermediario_ano': None, 'doc_destinacao_final_ano': None, 'doc_obs_ano': None}
