from django.shortcuts import render

# Create your views here.
def formList(request):
    return render(request, 'forms/formList.html')  # Render the formList.html template