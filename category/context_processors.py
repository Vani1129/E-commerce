from .models import Category

def menu_links(request):
    links = Category.objects.all()
    # print(f'links= {links}')
    return dict(links=links)