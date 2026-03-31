# Changelog — S-ARQ

Registro de mudanças significativas. Versões anteriores ao primeiro commit documentado
tinham mensagens de commit inconsistentes e estão agrupadas por tema.

---

## [Atual] — 2025

### Segurança
- `doc_editar`: usuário comum só edita documentos próprios; tentativa de editar documento alheio redireciona com erro
- `doc_delete`: restrito a papéis `sin` e `arq_admin`
- `listar_logs`, `sgc_ajax_load_related_data`, `get_codigo_details`: adicionado `@login_required`
- View e URL de reset de senha removidas (autenticação delegada ao LDAP)

### Performance
- `doc_lista`: busca migrada para o backend com AJAX + paginação configurável (20/50/100/200 por página); `select_related` elimina N+1 queries
- `listar_logs`: N+1 queries por usuário substituídas por uma única query com `annotate`
- `caixa_lista`: 4 queries de contagem substituídas por um único `aggregate`
- `gerar_graficos`: iteração sobre objetos substituída por `.values()` + `DataFrame.from_records()`
- Migration `0003`: índices adicionados em `doc_data`, `doc_eliminacao_ano`, `status_doc`, `create_at`

### Correções
- `doc_editar`: campo `doc_data` aparecia vazio — corrigido formato do widget para `YYYY-MM-DD`
- `doc_editar` / `doc_novo`: cálculo de anos usava `parseInt(date_string)` retornando `NaN` — corrigido para extrair apenas o ano com `split('-')[0]`
- Recálculo de anos ao alterar a data manualmente no formulário

### Funcionalidades
- `/doc_lista/`: busca dinâmica com dois campos (geral + sub-filtro), paginação configurável, sem recarregar a página
- `/listar_logs/`: filtro por período (data início/fim) e por usuário; cards de totais; tabela por usuário com total diário e mensal
- `/dashboard/`: nova página com 4 gráficos (documentos por tipo, por caixa, cadastros por dia, produtividade por usuário) e 3 cards de resumo
- Menu: links Dashboard e Relatório visíveis apenas para `sin` e `arq_admin`

### CSS / Visual
- Formulários `criar.html` (om, tipo, caixa, ano, tcu, status): card Bootstrap com header escuro, espaçamento correto abaixo do menu
- Formulários `doc/criar.html` e `doc/editar.html`: mesmo padrão de card
- Tabela de documentos: compacta (`table-sm`), fonte menor, `white-space: nowrap`
- Partial `partials/form_style.html`: estilo de formulário centralizado e reutilizável

---

## Histórico anterior (pré-documentação)

| Tema | Commits relacionados |
|---|---|
| Pesquisa dinâmica na tabela de documentos | `alteração_pesquisa*` |
| Controle de quantidade de documentos/caixas | `qtd_docs*`, `qtd_cx*` |
| Exibição de nome de usuário na tabela | `add_nome_usuario` |
| Checkbox de conferência de documentos | `checkbox` |
| Correções no formulário de caixa | `forms_caixa` |
| Correções gerais de arquivo/upload | `erro_arquivo*` |
| Edição de usuário | `user_edit*` |
| Conferência de documentos | `conferencia*` |
| Estrutura inicial do projeto | `primeiro`, `segundo`, `3`, `4` |

---

## Convenção de commits (a partir de agora)

```
<tipo>: <resumo curto>

feat     nova funcionalidade
fix      correção de bug
refactor refatoração sem mudança de comportamento
perf     melhoria de performance
style    CSS / formatação visual
docs     documentação
chore    manutenção (deps, config, deploy)
```
