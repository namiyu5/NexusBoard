from django.shortcuts import render

def vue_app(request):
    return render(request, "nexus_board/index.html")