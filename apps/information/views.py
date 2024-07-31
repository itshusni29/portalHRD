

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import JadwalBusM
from .forms import JadwalBusF
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Pengumuman
from .forms import PengumumanForm
from .forms import SearchForm


# =============================
# Views: Manajemen Jadwal Bus
# =============================
def jadwal_bus(request):
    # View untuk menampilkan daftar semua jadwal bus.
    jadwal_bus_list = JadwalBusM.objects.all()
    return render(request, "information/Jadwal_bus/jadwalBusJemputan.html", {
        "jadwal_bus_list": jadwal_bus_list,
    })


def jadwal_bus_create(request):
    # View untuk membuat jadwal bus baru.
    if request.method == "POST":
        form = JadwalBusF(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Menyimpan formulir dan membuat instance baru
            return redirect("jadwal_bus_list")  # Redirect ke daftar jadwal bus
    else:
        form = JadwalBusF()
    return render(request, "information/Jadwal_bus/Create_jadwal.html", {"form": form})


def jadwal_bus_update(request, pk):
    # View untuk memperbarui jadwal bus yang ada.
    jadwal = get_object_or_404(JadwalBusM, pk=pk)
    if request.method == "POST":
        form = JadwalBusF(request.POST, request.FILES, instance=jadwal)
        if form.is_valid():
            form.save()  # Menyimpan perubahan pada instance yang ada
            return redirect("jadwal_bus_list")  # Redirect ke daftar jadwal bus
    else:
        form = JadwalBusF(instance=jadwal)
    return render(request, "information/Jadwal_bus/Update_jadwal.html", {"form": form})


def jadwal_bus_delete(request, pk):
    # View untuk menghapus jadwal bus.
    jadwal = get_object_or_404(JadwalBusM, pk=pk)
    if request.method == "POST":
        jadwal.delete()  # Menghapus instance dari database
        return redirect("jadwal_bus_list")  # Redirect ke daftar jadwal bus
    return render(request, "information/Jadwal_bus/Delete_jadwal.html", {"jadwal": jadwal})


# =============================
# Views: Manajemen Pengumuman
# =============================

def daftar_pengumuman(request):
    # View untuk menampilkan daftar semua pengumuman dengan opsi pencarian.
    pengumuman_list = Pengumuman.objects.all()

    # Menangani kueri pencarian
    search_form = SearchForm(request.GET)
    if search_form.is_valid():
        search_query = search_form.cleaned_data.get("search_query")
        if search_query:
            pengumuman_list = pengumuman_list.filter(nama_pengumuman__icontains=search_query)

    return render(
        request, "information/Pengumuman/pengumumanList.html", {
            "pengumuman_list": pengumuman_list,
            "search_form": search_form
        }
    )


def buat_pengumuman(request):
    # View untuk membuat pengumuman baru.
    if request.method == "POST":
        form = PengumumanForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Menyimpan formulir dan membuat instance baru
            return redirect("pengumuman_list")  # Redirect ke daftar pengumuman
    else:
        form = PengumumanForm()
    return render(request, "information/Pengumuman/Create_pengumuman.html", {"form": form})


def ubah_pengumuman(request, pk):
    # View untuk memperbarui pengumuman yang ada.
    pengumuman = get_object_or_404(Pengumuman, pk=pk)
    if request.method == "POST":
        form = PengumumanForm(request.POST, request.FILES, instance=pengumuman)
        if form.is_valid():
            form.save()  # Menyimpan perubahan pada instance yang ada
            return redirect("pengumuman_list")  # Redirect ke daftar pengumuman
    else:
        form = PengumumanForm(instance=pengumuman)
    return render(request, "information/Pengumuman/Update_pengumuman.html", {"form": form})


def hapus_pengumuman(request, pk):
    # View untuk menghapus pengumuman.
    pengumuman = get_object_or_404(Pengumuman, pk=pk)
    if request.method == "POST":
        pengumuman.delete()  # Menghapus instance dari database
        return redirect("pengumuman_list")  # Redirect ke daftar pengumuman
    return render(request, "information/Pengumuman/Delete_pengumuman.html", {"pengumuman": pengumuman})

def unduh_file_pengumuman(request, pengumuman_id):
    # View untuk mengunduh file pengumuman.
    pengumuman_instance = get_object_or_404(Pengumuman, id=pengumuman_id)
    file_path = pengumuman_instance.file_pengumuman.path
    with open(file_path, "rb") as f:
        response = HttpResponse(f.read(), content_type="application/octet-stream")
        response["Content-Disposition"] = (
            "attachment; filename=" + pengumuman_instance.file_pengumuman.name
        )
    return response
