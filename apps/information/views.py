
import os
import glob
from django import forms
from django.conf import settings


from django import template
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, FileResponse, Http404
from django.template import loader
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from datetime import datetime, timedelta
import pandas as pd
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse



from .models import (
    JadwalBusM,
    MenuKantinM,
    PengumumanM,    
)


from .forms import (
    JadwalBusF,
    MenuKantinF,
    PengumumanF,
    SearchForm
    
)



# ======================================================================================================================
# Views: Manajemen Kehadiran
# ======================================================================================================================
def kehadiran(request):
    # View untuk menampilkan daftar semua kehadiran.
    return render(request, "information/Kehadiran/indexsKehadiran.html")


# ======================================================================================================================
# Views: Manajemen Komite
# ======================================================================================================================
def komite(request):
    # View untuk menampilkan daftar semua komite.
    return render(request, "information/Komite/Komite.html")


# ======================================================================================================================
# Views: Manajemen Jadwal Bus
# ======================================================================================================================
def jadwal_bus(request):
    # View untuk menampilkan daftar semua jadwal bus.
    jadwal_bus_list = JadwalBusM.objects.all()
    return render(request, "information/Jadwal_bus/jadwalbus1.html", {
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


# ======================================================================================================================
# Views: Manajemen Pengumuman
# ======================================================================================================================

def pengumuman_list(request):
    # View untuk menampilkan daftar semua pengumuman dengan opsi pencarian.
    pengumuman_list = PengumumanM.objects.all()
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

def pengumuman_create(request):
    # View untuk membuat pengumuman baru.
    if request.method == "POST":
        form = PengumumanF(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Menyimpan formulir dan membuat instance baru
            return redirect("information:pengumuman_list")  # Redirect ke daftar pengumuman
    else:
        form = PengumumanF()
    return render(request, "information/Pengumuman/Create_pengumuman.html", {"form": form})

def pengumuman_update(request, pk):
    # View untuk memperbarui pengumuman yang ada.
    pengumuman = get_object_or_404(PengumumanM, pk=pk)
    if request.method == "POST":
        form = PengumumanF(request.POST, request.FILES, instance=pengumuman)
        if form.is_valid():
            form.save()  # Menyimpan perubahan pada instance yang ada
            return redirect("information:pengumuman_list")  # Redirect ke daftar pengumuman
    else:
        form = PengumumanF(instance=pengumuman)
    return render(request, "information/Pengumuman/Update_pengumuman.html", {"form": form})

def pengumuman_delete(request, pk):
    # View untuk menghapus pengumuman.
    pengumuman = get_object_or_404(PengumumanM, pk=pk)
    if request.method == "POST":
        pengumuman.delete()  # Menghapus instance dari database
        return redirect("information:pengumuman_list")  # Redirect ke daftar pengumuman
    return render(request, "information/Pengumuman/Delete_pengumuman.html", {"pengumuman": pengumuman})

def file_pengumuman_download(request, pengumuman_id):
    # View untuk mengunduh file pengumuman.
    pengumuman_instance = get_object_or_404(PengumumanM, id=pengumuman_id)
    file_path = pengumuman_instance.file_pengumuman.path
    with open(file_path, "rb") as f:
        response = HttpResponse(f.read(), content_type="application/octet-stream")
        response["Content-Disposition"] = (
            "attachment; filename=" + pengumuman_instance.file_pengumuman.name
        )
    return response



# ======================================================================================================================
# Views: Manajemen Menu Kantin
# ======================================================================================================================
def upload_csv(request):
    if request.method == "POST":
        form = MenuKantinF(request.POST, request.FILES)
        if form.is_valid():
            # Save the uploaded file
            form.save()
            return redirect("menuKantin")  # Assuming 'menuKantin' is the URL pattern name for menuKantin view
    else:
        form = MenuKantinF()
    return render(request, "information/Menu_kantin/create_menukantin.html", {"form": form})

def delete_csv(request, file_id):
    # Retrieve the MenuKantinM instance
    file_instance = MenuKantinM.objects.get(pk=file_id)

    # Get the file path
    file_path = file_instance.alamat_file.path

    # Delete the file from the storage
    if os.path.exists(file_path):
        os.remove(file_path)

    # Delete the MenuKantinM instance
    file_instance.delete()

    return redirect("menuKantin")

def menuKantin(request):
    csv_file_path = get_most_recent_csv_file()
    menus = MenuKantinM.objects.all()

    if csv_file_path:
        df = pd.read_csv(csv_file_path, delimiter=";")
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce", format="%d/%m/%Y")
        df["Date"].fillna(df["Date"].apply(lambda x: pd.to_datetime(x, errors="coerce", format="%d/%m")), inplace=True)

        today_date = datetime.now().strftime("%d/%m/%Y")
        tomorrow_date = (datetime.now() + timedelta(days=1)).strftime("%d/%m/%Y")

        today_data = df[df["Date"].dt.strftime("%d/%m/%Y") == today_date]
        tomorrow_data = df[df["Date"].dt.strftime("%d/%m/%Y") == tomorrow_date]

        today_data_list = []
        for _, row in today_data.iterrows():
            today_data_list.append({
                "Date": row["Date"].strftime("%d/%m/%Y"),
                "Pilihan": row["PILIHAN"].replace(",", "<br>"),
                "Breakfast": row["BREAKFAST"].replace(",", "<br>"),
                "Shift3": row["SHIFT 3"].replace(",", "<br>"),
                "Shift1": row["SHIFT 1"].replace(",", "<br>"),
                "Shift2": row["SHIFT 2"].replace(",", "<br>"),
            })

        tomorrow_data_list = []
        for _, row in tomorrow_data.iterrows():
            tomorrow_data_list.append({
                "Date": row["Date"].strftime("%d/%m/%Y"),
                "Pilihan": row["PILIHAN"].replace(",", "<br>"),
                "Breakfast": row["BREAKFAST"].replace(",", "<br>"),
                "Shift3": row["SHIFT 3"].replace(",", "<br>"),
                "Shift1": row["SHIFT 1"].replace(",", "<br>"),
                "Shift2": row["SHIFT 2"].replace(",", "<br>"),
            })

        return render(
            request,
            "information/Menu_kantin/Menu_kantin.html",
            {
                "today_data": today_data_list,
                "tomorrow_data": tomorrow_data_list,
                "menus": menus,
            },
        )
    else:
        return render(request, "information/Menu_kantin/menu_nodata.html")

def get_most_recent_csv_file():
    # Get a list of CSV files in the 'media/uploads/menuKantin' directory and subdirectories
    csv_files = glob.glob(
        os.path.join(settings.MEDIA_ROOT, "uploads/menuKantin/**/*.csv"), recursive=True
    )

    # Sort the list of files by modification time (most recent first)
    csv_files.sort(key=os.path.getmtime, reverse=True)

    # Check if any CSV files were found
    if csv_files:
        # Return the path to the most recently modified CSV file
        return csv_files[0]
    else:
        return None

