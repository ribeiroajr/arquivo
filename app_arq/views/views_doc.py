from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .views_log import registrar_acao_usuario, registrar_acao_usuario_deletar
from ..forms import DocsForm
from ..models import Docs, Codigos
from django.http import JsonResponse
from django.contrib import messages
# Create your views here.

# @login_required
# def doc_lista(request):
#     dataset = Docs.objects.all()
#     #qtd de docs
#     qtd_docs = dataset.count()
#     context = {"dataset": dataset, 'qtd_docs' : qtd_docs}
#     print(dataset)
#     return render(request, 'doc/lista.html', context)

from rolepermissions.checkers import has_role

@login_required
def doc_lista(request):
    user = request.user  

    if has_role(user, "sin") or has_role(user, "arq_admin"):
        dataset = Docs.objects.all()
    else:
        dataset = Docs.objects.filter(fk_user=user)

    qtd_docs = dataset.count()
    context = {"dataset": dataset, "qtd_docs": qtd_docs}
    return render(request, 'doc/lista.html', context)

## ok
# @login_required
# def doc_novo(request):
#     if request.method == 'POST':
#         form = DocsForm(request.POST)
#         if form.is_valid():
#             # Pegar o ano do doc_data enviado via post
#             doc_data = form.cleaned_data.get('doc_data')
#             if not doc_data:
#                 return render(request, 'doc/erro.html', {'mensagem': 'Data do documento não informada'})
            
#             doc_data_ano = doc_data.year
#             print(f'doc_data_ano: {doc_data_ano}')

#             # Pegar o fk_codigo enviado via post
#             fk_codigo = form.cleaned_data.get('fk_codigo')
#             if not fk_codigo:
#                 return render(request, 'doc/erro.html', {'mensagem': 'Código não informado'})
            
#             print(f'fk_codigo: {fk_codigo}')

#             try:
#                 # Recuperar na model Codigos de acordo com fk_codigo enviado
#                 codigos = Codigos.objects.get(pk=fk_codigo.pk)
#             except Codigos.DoesNotExist:
#                 # Trate a exceção caso o objeto não exista
#                 # Aqui você pode redirecionar para uma página de erro ou fazer o que for apropriado para o seu aplicativo
#                 return render(request, 'doc/erro.html', {'mensagem': 'Código não encontrado'})

#             # Verificar se os campos em Codigos estão preenchidos
#             # if (codigos.fase_corrente_ano is None or
#             #         codigos.fase_intermediaria_ano is None or
#             #         codigos.destinacao_final_ano is None):
#             #     return render(request, 'doc/erro.html', {'mensagem': 'Campos em Codigos não estão preenchidos'})

#             # Calcular o novo valor composto
#             novo_valor_composto = (
#                 (codigos.fase_corrente_ano or 0) +
#                 (codigos.fase_intermediaria_ano or 0) +
#                 (codigos.destinacao_final_ano or 0) +
#                 (doc_data_ano or 0)
#             )

#             print(f'novo_valor_composto: {novo_valor_composto}')

#             # Atribuir o novo valor composto ao campo doc_eliminacao_ano no formulário
#             form.cleaned_data['doc_eliminacao_ano'] = novo_valor_composto
#             # print(f'novo_valor_composto: {novo_valor_composto}')


#             # Salvar o formulário sem atribuir diretamente o objeto Codigos
#             doc = form.save(commit=False)
#             doc.fk_codigo = codigos  # Atribuir o objeto Codigos ao campo fk_codigo
            

            
#             # doc.fk_codigo_id = fk_codigo_id  # Atribuir o ID da chave estrangeira ao objeto Docs
#             doc.fase
#             doc.doc_eliminacao_ano = novo_valor_composto  # Atribuir o novo valor composto a doc_eliminacao_ano
#             doc.save()

#             return redirect('doc_lista')  # Redirecione para a lista após criar
#     else:
#         form = DocsForm()

#     return render(request, 'doc/criar.html', {'form': form})


# views.py


#@login_required
def get_codigo_details(request):
    codigo_id = request.GET.get('codigo_id', None)
    if codigo_id:
        codigo = Codigos.objects.filter(pk=codigo_id).first()
        if codigo:
            data = {
                'fase_corrente_ano': codigo.fase_corrente_ano,
                'fase_intermediaria_ano': codigo.fase_intermediaria_ano,
                'destinacao_final_ano': codigo.destinacao_final_ano,
            }
            return JsonResponse(data)
    return JsonResponse({'error': 'Código não encontrado.'})



@login_required
def doc_novo(request):

    # Obtendo o ID do usuário logado
    user_id = request.user.id
    user = request.user
    print(request.POST)
    if request.method == 'POST':
        form = DocsForm(request.POST)
        if form.is_valid():
            # form.save()
            instance = form.save()
            registrar_acao_usuario(request, instance, f'cadastrou')  # Passa a instância do objeto Ano e a ação
    
            messages.success(request, 'Doc cadastrado com sucesso.')
            return redirect('doc_novo')  # Redirecione para a lista após criar
        else:
            print("Erros de validação no formulário:")
            print(form.errors)  # Exibir erros de validação no console
    else:
        # form = DocsForm()
        # Passando o ID do usuário logado para o formulário
        form = DocsForm(initial={'fk_user': user_id})
    
    print("Renderizando o formulário...")
    print(request.method)  # Verificar se a página está sendo acessada com o método POST
    
    
    return render(request, 'doc/criar.html', {'form': form})




# @login_required
# def doc_detalhes(request, pk):
#     doc_ob = get_object_or_404(AnoForm, pk=pk)
#     return render(request, 'ano/detalhes.html', {'doc_ob': doc_ob})

@login_required
def doc_editar(request, id):
    user_id = request.user.id
    user = request.user

    context ={}
    doc_ob = get_object_or_404(Docs, id=id)
    if request.method == 'POST':
        form = DocsForm(request.POST, instance=doc_ob)
        if form.is_valid():
            # form.save()
            instance = form.save()
            registrar_acao_usuario(request, instance, f'editou')  # Passa a instância do objeto Ano e a ação
      
            return redirect('doc_lista')
    else:
        # form = DocsForm(instance=doc_ob)
        form = DocsForm(instance=doc_ob, initial={'fk_user': user_id})
    context = {
        'form': form,
        'doc_ob': doc_ob
    }
    return render(request, 'doc/editar.html', context)

@login_required
def doc_delete(request, id):
    context ={}
    doc_ob = get_object_or_404(Docs, id=id)
    if request.method == 'POST':
        # doc_ob.delete()
        instance = doc_ob  # Salva a instância antes de excluir
        doc_id = instance.id  # Obtém o ID do objeto Ano antes de excluir

        doc_ob.delete()
        # registrar_acao_usuario(request, instance, 'deletou')  # Passa a instância do objeto Ano
        registrar_acao_usuario_deletar(request, f'Docs', doc_id) 

        # messages.success(request, 'Registro excluído com sucesso.')
        return redirect('doc_lista')
    
    context = {
        'doc_ob': doc_ob
    }
    
    return render(request, 'doc/excluir.html', context)


# views.py
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

@login_required
@require_POST
def toggle_status_doc(request, pk):
    try:
        doc = Docs.objects.get(pk=pk)

        # alterna o status
        doc.status_doc = not doc.status_doc
        doc.save()

        return JsonResponse({
            "success": True,
            "status": doc.status_doc
        })
    except Docs.DoesNotExist:
        return JsonResponse({"success": False, "error": "Documento não encontrado"}, status=404)
