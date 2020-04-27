from django.shortcuts import render

def handler404(request, exception):
    '''
        function to handle 404 error in production environment.
    '''
    return render(request, '404.html', status=404)
