from django.core.paginator import Paginator, EmptyPage

def filter_by_text(queryset, search_text, fields):
    """
    Filtra um queryset com base no texto de pesquisa e nos campos fornecidos.

    Args:
        queryset: O queryset a ser filtrado.
        search_text: O texto de pesquisa.
        fields: Lista de campos a serem verificados.

    Retorna:
        QuerySet: O queryset filtrado.
    """
    for field in fields:
        queryset = queryset.filter(**{f"{field}__icontains": search_text})
    return queryset

def paginate_queryset(queryset, page_size, page_number):
    """
    Pagina um queryset com base no número da página e no tamanho da página.

    Args:
        queryset: O queryset a ser paginado.
        page_size: O número de itens por página.
        page_number: O número da página solicitada.

    Retorna:
        Paginator: O conjunto de resultados paginados.
    """
    paginator = Paginator(queryset, page_size)
    try:
        page = paginator.page(page_number)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    return page
