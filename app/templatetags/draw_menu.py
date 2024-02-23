from django import template
from ..models import Node
from django.urls import get_resolver

register = template.Library()

@register.simple_tag(takes_context=True)
def draw_menu(context, x):
    # Формирование меню
    global allURLs
    allURLs = listOfURLs(get_resolver().url_patterns)
    y = {'x':x, 'url':None}
    global menuNodes
    menuNodes = Node.objects.raw('SELECT app_node.id, app_node.name, app_node.parentElem_id, app_node.url, app_menu.name FROM app_node JOIN app_menu ON app_node.menu_id = app_menu.id WHERE app_node.menu_id = (SELECT id FROM app_menu WHERE name = "' + x + '")')
    for c in menuNodes:
        targ = None
        if (c.parentElem != None):
            for c2 in menuNodes:
                if (c2.id == c.parentElem.id):
                    targ = c2.name
                    break
        y = add_sub(c, y, targ)
    del targ, allURLs

    # Исключение лишних пунктов
    request = context['request']
    path = request.path
    for c in range(1, len(y)-1):
        if (len(y[c]) > 2):
            y[c] = findExeciveNodes(y[c], path)
            y[c]['re'] = True
    y['re'] = True

    # Формирование HTML
    htmlOutp = '<div><ul>' + htmlGenRecursion(y, 1) + '</ul></div>'
    # del menuNodes
    return htmlOutp

def add_sub(x, obj, targ):
    if (targ == None):
        obj[len(obj)-1] = {'x':x.name, 'url':hijackNamedURL(x.url, allURLs)}
    else:
        for c in range(1, len(obj)-1):
            ke = obj[c]
            if (ke['x'] == targ):
                obj[c][len(obj[c])-1] = {'x':x.name, 'url':hijackNamedURL(x.url, allURLs)}
                break
            elif (len(ke)>2):
                obj[c] = add_sub(x, obj[c], targ)
    return obj

def findExeciveNodes(x, path):
    re = x
    boole = False
    if (len(x) > 2):
        for c in range(1, len(x)-1):
            re[c] = findExeciveNodes(x[c], path)
            if (re[c]['re'] == True):
                boole = True
    if (x['url'] == path or boole == True):
        re['re'] = True
        for c in range(1, len(x)-2):
            re[c]['re'] = True
    else:
        re['re'] = False
    return re

def listOfURLs(urllist):
    x = []
    for entry in urllist:
        if (entry.pattern._route == 'admin/'):
            continue
        x.append({'name': entry.name, 'path': entry.pattern._route})
    return x

def htmlGenRecursion(x, iteration):
    htmlOutp = ''
    for c in range(1, len(x)-2):
        if (x[c]['re'] == True):
            htmlOutp += '<li><a href = ' + x[c]['url'] + '>' + x[c]['x'] + '</a></li>'
            if (len(x[c]) > 3):
                htmlOutp += '<ul>' + htmlGenRecursion(x[c], iteration+1) + '</ul>'
    return htmlOutp

def hijackNamedURL(x, list):
    for c in list:
        if (x[:1] == "'"):
            if (c['name'] == x[1:-1]):
                z ='/' + c['path']
                return z
    return x
    