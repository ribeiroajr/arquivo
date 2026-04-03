from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .views_log import registrar_acao_usuario, registrar_acao_usuario_deletar
from ..forms import DocsForm
from ..models import Docs, Codigos
from django.http import JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q

from rolepermissions.checkers import has_role

@login_required
def doc_lista(request):
    user = request.user

    if has_role(user, "sin") or has_role(user, "arq_admin"):
        qs = Docs.objects.select_related(
            'fk_codigo', 'fk_tipo', 'fk_doc_origem', 'fk_doc_destino',
            'fk_caixa', 'fk_tcu', 'fk_codigo__fk_tipo_guarda', 'fk_user'
        ).all()
    else:
        qs = Docs.objects.select_related(
            'fk_codigo', 'fk_tipo', 'fk_doc_origem', 'fk_doc_destino',
            'fk_caixa', 'fk_tcu', 'fk_codigo__fk_tipo_guarda', 'fk_user'
        ).filter(fk_user=user)

    q  = request.GET.get('q', '').strip()
    q2 = request.GET.get('q2', '').strip()

    if q:
        qs = qs.filter(
            Q(doc_numero__icontains=q) |
            Q(new_file_sigad__icontains=q) |
            Q(fk_codigo__codigo__icontains=q) |
            Q(fk_tipo__tipo__icontains=q) |
            Q(fk_doc_origem__om__icontains=q) |
            Q(fk_doc_destino__om__icontains=q) |
            Q(fk_caixa__caixa__icontains=q) |
            Q(fk_tcu__tcu__icontains=q) |
            Q(doc_data__icontains=q)
        )

    if q2:
        qs = qs.filter(
            Q(doc_numero__icontains=q2) |
            Q(new_file_sigad__icontains=q2) |
            Q(fk_codigo__codigo__icontains=q2) |
            Q(fk_tipo__tipo__icontains=q2) |
            Q(fk_doc_origem__om__icontains=q2) |
            Q(fk_doc_destino__om__icontains=q2) |
            Q(fk_caixa__caixa__icontains=q2) |
            Q(fk_tcu__tcu__icontains=q2) |
            Q(doc_data__icontains=q2)
        )

    qtd_total = qs.count()

    per_page_options = [20, 50, 100, 200, 0]   # 0 = Tudo
    try:
        per_page = int(request.GET.get('per_page', 50))
        if per_page not in per_page_options:
            per_page = 50
    except (ValueError, TypeError):
        per_page = 50

    # Quando per_page == 0 mostra tudo em uma única página
    paginate_by = qtd_total if per_page == 0 else per_page
    paginator = Paginator(qs, max(paginate_by, 1))
    page_num  = request.GET.get('page', 1)
    page_obj  = paginator.get_page(page_num)

    # Resposta AJAX: retorna HTML parcial da tabela + metadados de paginação
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        from django.template.loader import render_to_string
        tabela_html = render_to_string(
            'doc/_tabela_rows.html',
            {'page_obj': page_obj, 'request': request},
            request=request,
        )
        paginacao_html = render_to_string(
            'doc/_paginacao.html',
            {
                'page_obj': page_obj,
                'per_page': per_page,
                'per_page_options': per_page_options,
                'q': q,
                'q2': q2,
                'qtd_total': qtd_total,
            },
            request=request,
        )
        return JsonResponse({
            'tabela_html': tabela_html,
            'paginacao_html': paginacao_html,
            'qtd_total': qtd_total,
        })

    context = {
        "page_obj": page_obj,
        "qtd_docs": qtd_total,
        "per_page": per_page,
        "per_page_options": per_page_options,
        "q": q,
        "q2": q2,
    }
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


@login_required
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
    user = request.user
    doc_ob = get_object_or_404(Docs, id=id)

    # Apenas o dono do documento ou admins podem editar
    if not (has_role(user, 'sin') or has_role(user, 'arq_admin') or doc_ob.fk_user == user):
        messages.error(request, 'Você não tem permissão para editar este documento.')
        return redirect('doc_lista')

    if request.method == 'POST':
        form = DocsForm(request.POST, instance=doc_ob)
        if form.is_valid():
            instance = form.save()
            registrar_acao_usuario(request, instance, 'editou')
            return redirect('doc_lista')
    else:
        form = DocsForm(instance=doc_ob, initial={'fk_user': user.id})

    return render(request, 'doc/editar.html', {'form': form, 'doc_ob': doc_ob})


@login_required
def doc_delete(request, id):
    user = request.user
    doc_ob = get_object_or_404(Docs, id=id)

    # Apenas admins podem excluir
    if not (has_role(user, 'sin') or has_role(user, 'arq_admin')):
        messages.error(request, 'Você não tem permissão para excluir documentos.')
        return redirect('doc_lista')

    if request.method == 'POST':
        doc_id = doc_ob.id
        doc_ob.delete()
        registrar_acao_usuario_deletar(request, 'Docs', doc_id)
        return redirect('doc_lista')

    return render(request, 'doc/excluir.html', {'doc_ob': doc_ob})


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
