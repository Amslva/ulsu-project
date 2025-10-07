from mainpage.views import menu


def get_menu_context(request):
    return{'main_menu':menu}

