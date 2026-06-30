from django.urls import reverse


def navbar_context(request):
    resolver_match = getattr(request, "resolver_match", None)
    url_name = (resolver_match.url_name or "") if resolver_match else ""
    path = request.path or ""

    is_home = path == "/"
    is_create = url_name.endswith("_create") or path.endswith("/crear/")
    is_edit = url_name.endswith("_edit") or "/editar/" in path
    is_merma = "merma" in url_name or "/mermas/" in path
    is_merma_create = url_name == "merma_create" or path.endswith("/mermas/crear/")

    show_sidebar_toggle = not (is_create or is_edit or is_merma)
    show_back_button = is_create or is_edit or is_merma
    show_topbar_actions = is_create or is_edit or is_merma
    show_search_area = not (is_create or is_edit or is_merma or is_home)
    show_user_menu = show_sidebar_toggle
    show_copy_button = is_create and not is_merma_create
    show_form_item_save = is_create and not is_merma_create
    show_upload_button = is_merma and not is_merma_create
    show_form_producto_save = is_merma and not is_merma_create
    show_delete_button = is_edit
    show_merma_create_save = is_merma_create

    if is_merma_create:
        back_url = reverse("inventario:merma_list")
    else:
        back_url = reverse("inventario:inventario_inicio")

    return {
        "navbar_show_sidebar_toggle": show_sidebar_toggle,
        "navbar_show_back_button": show_back_button,
        "navbar_show_topbar_actions": show_topbar_actions,
        "navbar_show_copy_button": show_copy_button,
        "navbar_show_form_item_save": show_form_item_save,
        "navbar_show_upload_button": show_upload_button,
        "navbar_show_form_producto_save": show_form_producto_save,
        "navbar_show_delete_button": show_delete_button,
        "navbar_show_merma_create_save": show_merma_create_save,
        "navbar_show_search_area": show_search_area,
        "navbar_show_user_menu": show_user_menu,
        "navbar_back_url": back_url,
    }
