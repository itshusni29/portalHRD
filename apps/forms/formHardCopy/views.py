from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from ..models import FormHardcopy
from .forms import FormHardcopyForm

# List all forms for regular users
def form_list(request):
    forms = FormHardcopy.objects.all()
    return render(request, "forms/formHardCopy/formHardCopy.html", {"forms": forms})

# Admin view to list all forms
def form_list_admin(request):
    forms = FormHardcopy.objects.all()
    return render(request, "forms/formHardCopy/admin_formHardCopy.html", {"forms": forms})

# Create a new form hard copy
def form_create(request):
    if request.method == 'POST':
        form = FormHardcopyForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('formHardCopy:form_hard_copy_admin_list')
    else:
        form = FormHardcopyForm()
    return render(request, "forms/formHardCopy/Create_formHardCopy.html", {'form': form})

# Update an existing form hard copy
def form_update(request, pk):
    form_instance = get_object_or_404(FormHardcopy, pk=pk)
    if request.method == 'POST':
        form = FormHardcopyForm(request.POST, request.FILES, instance=form_instance)
        if form.is_valid():
            form.save()
            return redirect('formHardCopy:form_hard_copy_admin_list')
    else:
        form = FormHardcopyForm(instance=form_instance)
    return render(request, "forms/formHardCopy/Update_formHardCopy.html", {'form': form})

# Delete a form hard copy
def form_delete(request, pk):
    form_instance = get_object_or_404(FormHardcopy, pk=pk)
    if request.method == 'POST':
        form_instance.delete()
        return redirect('formHardCopy:form_hard_copy_admin_list')
    return render(request, "forms/formHardCopy/Delete_formHardCopy.html", {'form': form_instance})

# Download a form hard copy file
def download_file(request, form_id):
    form_instance = get_object_or_404(FormHardcopy, id=form_id)
    file_path = form_instance.file_upload.path
    try:
        with open(file_path, "rb") as f:
            response = HttpResponse(f.read(), content_type="application/octet-stream")
            response['Content-Disposition'] = f'attachment; filename="{form_instance.file_upload.name}"'
            return response
    except FileNotFoundError:
        return HttpResponse("File not found.", status=404)
