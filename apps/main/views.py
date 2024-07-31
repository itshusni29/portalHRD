
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Prosedur
from .forms import ProsedurForm



# =============================
# Views: Home
# =============================
def index(request):
    return render(request, 'main/index.html')

# =============================
# Views: Manajemen Prosedur
# =============================
def daftar_prosedur(request):
    # View untuk menampilkan daftar semua prosedur dengan fungsionalitas pencarian.
    daftar_prosedur = Prosedur.objects.all()

    # Menangani query pencarian
    query_pencarian = request.GET.get('search', '')
    if query_pencarian:
        daftar_prosedur = daftar_prosedur.filter(nama__icontains=query_pencarian)

    return render(request, "main/prosedur/list_prosedur.html", {
        "daftar_prosedur": daftar_prosedur,
        "query_pencarian": query_pencarian,
    })

def unduh_file_prosedur(request, prosedur_id):
    # View untuk mengunduh file prosedur.
    prosedur = get_object_or_404(Prosedur, id=prosedur_id)
    file_path = prosedur.file_upload.path

    with open(file_path, "rb") as f:
        response = HttpResponse(f.read(), content_type="application/octet-stream")
        response["Content-Disposition"] = f"attachment; filename={prosedur.file_upload.name}"
        return response

def buat_prosedur(request):
    # View untuk membuat prosedur baru.
    if request.method == "POST":
        form = ProsedurForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("daftar_prosedur")
    else:
        form = ProsedurForm()
    return render(request, "main/prosedur/create_prosedur.html", {"form": form})

def ubah_prosedur(request, prosedur_id):
    # View untuk memperbarui prosedur yang ada.
    prosedur = get_object_or_404(Prosedur, id=prosedur_id)
    if request.method == "POST":
        form = ProsedurForm(request.POST, request.FILES, instance=prosedur)
        if form.is_valid():
            form.save()
            return redirect("daftar_prosedur")
    else:
        form = ProsedurForm(instance=prosedur)
    return render(request, "main/prosedur/update_prosedur.html", {"form": form})


def hapus_prosedur(request, prosedur_id):
    # View untuk menghapus prosedur
    prosedur = get_object_or_404(Prosedur, id=prosedur_id)
    if request.method == "POST":
        prosedur.delete()
        return redirect("daftar_prosedur")
    return render(request, "main/prosedur/delete_prosedur.html", {"prosedur": prosedur})
