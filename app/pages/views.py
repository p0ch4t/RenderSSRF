from hashlib import new
from django.shortcuts import render
from django.http import HttpResponse
import requests, ast, re

def home(request):
    return HttpResponse("<html><script>window.location = '/config'</script></html>")

def config(request):
    return render(request, 'config.html')

def generator(request):
    headers = request.split("\r\n\r\n")[0].split("\n")
    data = request.split("\r\n\r\n")[1]
    headersKey = {}
    headersValue = {}
    final_headers = {}

    for i in range(len(headers)):
        if (i == 0):
            headerKey = headers[i].split(" ")[1]
            path = headerKey
        else:
            headersKey[i] = headers[i].split(':')[0]
            headersValue[i] = headers[i].split(': ')[1].split('\r')[0]
            final_headers[headersKey[i]] = headersValue[i]
            headerKey = headers[i].split(":")[0]
            if headerKey == "Host":
                host = 'https://'+headers[i].split(": ")[1].split('\r')[0]

    return host+path, final_headers, data

def resources_call(html, url):
    recursos = re.findall(r"""(['"]\/.*\.(js|css|png|jpg|pdf|svg|gif)['"])""", html)
    
    print(recursos)
    for x in range(len(recursos)):
        recurso = recursos[x][0]
        recurso = re.sub("'", "", recurso)
        recurso = re.sub('"', '', recurso)
        url = re.findall(r"""[(http(s)?):\/\/(www\.)?a-zA-Z0-9@:%._\+~#=-]{2,256}\.[a-z]{2,6}""", url)
        url = "".join(url)
        html = re.sub(recurso, url+recurso, html)

    recursos = re.findall(r"(=\/.*\.(css))", html)
    
    for x in range(len(recursos)):
        recurso = recursos[x][0]
        recurso = re.sub("=", '', recurso)
        html = re.sub(recurso, url+recurso, html)
    
    return html

def render_ssrf(request):  
    if request.method == "POST":
        try:
            if request.POST['old_internal_site'] != '' and request.POST.get('new_internal_site', False) and request.POST['url'] != '' and request.POST['headers'] != '':
                old_internal_site = request.POST['old_internal_site']
                new_internal_site = request.POST['new_internal_site']
                url = request.POST['url']
                headers = ast.literal_eval(request.POST['headers'])
                if request.POST.get('data', False):
                    data = request.POST['data']
                else:
                    data = ''
                if data:
                    data = re.sub(old_internal_site, new_internal_site, data)
                    html = requests.post(url, headers=headers, data=data)
                    html = resources_call(html.text, url)
                    return render(request, 'render_ssrf.html', {"html": html, "old_internal_site": new_internal_site, "url": url, "headers": headers, "data": data})                
                else:
                    url = re.sub(old_internal_site, new_internal_site, url)
                    html = requests.get(url, headers=headers) 
                    html = resources_call(html.text, url)
                    return render(request, 'render_ssrf.html', {"html": html, "old_internal_site": old_internal_site, "url": url, "headers": headers})
        except:
            return HttpResponse("Ocurrio un error. Por favor, revise la configuración del request.")

        if request.POST['generator'] != '' and request.POST['old_internal_site'] != '':
            url, headers, data = generator(request.POST['generator'])
            old_internal_site = request.POST['old_internal_site']
            if data:
                html = requests.post(url, headers=headers, data=data)
                html = resources_call(html.text, url)
                return render(request, 'render_ssrf.html', {"html": html, "old_internal_site": old_internal_site, "url": url, "headers": headers, "data": data})
            else:
                html = requests.get(url, headers=headers) 
                html = resources_call(html.text, url)
                return render(request, 'render_ssrf.html', {"html": html, "old_internal_site": old_internal_site, "url": url, "headers": headers})          
        else:
            return HttpResponse("Missing params.")
    
    if request.method == "GET":
        return render(request, 'render_ssrf.html')