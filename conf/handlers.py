from django.shortcuts import render


def handler403(request, exception):
    return render(request, 'handler.html', {'error_code': 403})


def handler404(request, exception):
    return render(request, 'handler.html', {'error_code': 404})


def handler500(request):
    return render(request, 'handler.html', {'error_code': 500})