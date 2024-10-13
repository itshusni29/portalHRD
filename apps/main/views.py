
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from django.contrib.sessions.models import Session
from django.utils import timezone

from django.http import FileResponse
from .models import AturanM, ProsedurM, Visitor, kegiatanM, Banner
from .forms import AturanF, ProsedurF, SearchForm, kegiatanF, BannerForm







# Views: Tim Kami
# ======================================================================================================================
def dashboard(request):
    return render(request, "main/dashboard.html")

# Views: Tim Kami
# ======================================================================================================================
def timKami(request):
    return render(request, "main/Tim_Kami.html")

# Views: Kontak
# ======================================================================================================================
def kontak(request):
    return render(request, "main/Kontak.html")


# Views: Home
# ======================================================================================================================
# Utility Function: Get Client IP
def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip

# Utility Function: Date Ranges
def get_date_range():
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    this_month_start = datetime(today.year, today.month, 1).date()
    this_year_start = datetime(today.year, 1, 1).date()
    return today, yesterday, this_month_start, this_year_start

# View: Home Page with Visitor Counter
def index(request):
    # Get date ranges for statistics
    today, yesterday, this_month_start, this_year_start = get_date_range()

    # Visitor statistics
    today_count = Visitor.objects.filter(timestamp__date=today).count()
    yesterday_count = Visitor.objects.filter(timestamp__date=yesterday).count()
    this_month_count = Visitor.objects.filter(timestamp__date__gte=this_month_start).count()
    this_year_count = Visitor.objects.filter(timestamp__date__gte=this_year_start).count()
    total_hits_count = Visitor.objects.all().count()

    # Online users based on session expiry
    online_users = Session.objects.filter(expire_date__gte=timezone.now()).count()

    # Record the current visitor's IP address
    current_visitor_ip = get_client_ip(request)
    Visitor.objects.create(ip_address=current_visitor_ip)

    # Fetch banners based on their position
    left_banners = Banner.objects.filter(posisi='left')
    right_banners = Banner.objects.filter(posisi='right')

    # Context for rendering the template
    context = {
        "segment": "index",
        "today_count": today_count,
        "yesterday_count": yesterday_count,
        "this_month_count": this_month_count,
        "this_year_count": this_year_count,
        "total_hits_count": total_hits_count,
        "online_users": online_users,
        "left_banners": left_banners,
        "right_banners": right_banners,
    }

    return render(request, "main/index.html", context)

# Views: Search
# ======================================================================================================================
# View: Form Model Detail
def formmodel_detail(request, pk, model_type):
    model_mapping = {
        'prosedur': ProsedurM,
        'aturan': AturanM,
    }

    model = model_mapping.get(model_type)
    if model:
        instance = get_object_or_404(model, pk=pk)
        return render(request, 'main/Search_detail.html.html', {'instance': instance, 'model_type': model_type})
    else:
        return render(request, 'main/Search_noresult.html', {'model_type': model_type})

# View: Search
def search(request):
    form = SearchForm(request.GET)
    results = []

    if form.is_valid():
        query = form.cleaned_data.get('query', '')

        if query:
            # Search across all relevant models
            results += list(Formmodel.objects.filter(nama_form__icontains(query)))
            results += list(ProsedurM.objects.filter(nama__icontains=query))
            results += list(Pengumuman.objects.filter(nama_pengumuman__icontains(query)))
            results += list(AturanM.objects.filter(judul__icontains=query))

    context = {
        'form': form,
        'results': results,
        'empty_query': not bool(query),
    }

    return render(request, 'main/search_result.html', context)

# Views: Manajemen Prosedur
# ======================================================================================================================

def admin_prosedur(request):
    daftar_prosedur = ProsedurM.objects.all()
    return render(request, "main/prosedur/admin_prosedur.html", {"daftar_prosedur": daftar_prosedur})


def daftar_prosedur(request):
    # View untuk menampilkan daftar semua prosedur dengan fungsionalitas pencarian.
    daftar_prosedur = ProsedurM.objects.all()

    # Menangani query pencarian
    query_pencarian = request.GET.get('search', '')
    if query_pencarian:
        daftar_prosedur = daftar_prosedur.filter(nama__icontains=query_pencarian)

    return render(request, "main/prosedur/list_prosedur.html", {
        "daftar_prosedur": daftar_prosedur,
        "query_pencarian": query_pencarian,
    })


def unduh_file_prosedur(request, pk):
    # View untuk mengunduh file PDF prosedur.
    prosedur = get_object_or_404(ProsedurM, pk=pk)
    return FileResponse(prosedur.file_upload, as_attachment=True)

def buat_prosedur(request):
    # View to handle both GET (display the form) and POST (save the form data).
    if request.method == "POST":
        form = ProsedurF(request.POST, request.FILES)
        if form.is_valid(): 
            form.save()
            return redirect("admin_prosedur")  # Redirect to the procedure list view after saving
    else:
        form = ProsedurF()
    
    return render(request, "main/prosedur/create_prosedur.html", {"form": form})


def ubah_prosedur(request, prosedur_id):
    # View untuk memperbarui prosedur yang ada.
    prosedur = get_object_or_404(ProsedurM, id=prosedur_id)
    if request.method == "POST":
        form = ProsedurF(request.POST, request.FILES, instance=prosedur)
        if form.is_valid():
            form.save()
            return redirect("admin_prosedur")
    else:
        form = ProsedurF(instance=prosedur)
    return render(request, "main/prosedur/update_prosedur.html", {"form": form})

def hapus_prosedur(request, prosedur_id):
    # View untuk menghapus prosedur
    prosedur = get_object_or_404(ProsedurM, id=prosedur_id)
    if request.method == "POST":
        prosedur.delete()
        return redirect("admin_prosedur")
    return render(request, "main/prosedur/delete_prosedur.html", {"prosedur": prosedur})


# Views: Manajemen Aturan
# ======================================================================================================================
def admin_aturan(request):
    aturans = AturanM.objects.all()
    return render(request, "main/aturan/admin_aturan.html", {"aturans": aturans})

def daftar_aturan(request):
    # View untuk menampilkan daftar semua aturan.
    aturans = AturanM.objects.all()
    return render(request, "main/aturan/aturan.html", {"aturans": aturans})

def unduh_file_aturan(request, pk):
    # View untuk mengunduh file PDF aturan.
    aturan = get_object_or_404(AturanM, pk=pk)
    return FileResponse(aturan.file_pdf, as_attachment=True)

def buat_aturan(request):
    # View untuk membuat aturan baru.
    if request.method == "POST":
        form = AturanF(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("admin_aturan")
    else:
        form = AturanF()
    
    # Jika form tidak valid atau request GET
    return render(request, "main/aturan/Create_aturan.html", {"form": form, "title": "Buat Aturan"})


def ubah_aturan(request, pk):
    aturan = get_object_or_404(AturanM, pk=pk)  # Ambil data AturanM berdasarkan primary key (pk)
    
    if request.method == "POST":
        form = AturanF(request.POST, request.FILES, instance=aturan)
        if form.is_valid():
            form.save()  # Jika valid, simpan data yang diubah
            return redirect("admin_aturan")  # Redirect ke halaman daftar aturan setelah berhasil update
    else:
        form = AturanF(instance=aturan)  # Tampilkan form dengan data yang sudah ada

    return render(request, "main/aturan/Update_aturan.html", {"form": form, "title": "Ubah Aturan", "aturan": aturan})


def hapus_aturan(request, pk):
    # View untuk menghapus aturan.
    aturan = get_object_or_404(AturanM, pk=pk)
    if request.method == "POST":
        aturan.delete()
        return redirect("admin_aturan")
    return render(request, "main/aturan/Delete_aturan.html", {"aturan": aturan})



# Views: Manajemen Aturan
# ======================================================================================================================
def admin_kegiatan(request):
    kegiatans = kegiatanM.objects.all()
    return render(request, "main/Kegiatan/admin_kegiatan.html", {"kegiatans": kegiatans})

def list_kegiatan(request):
    kegiatans = kegiatanM.objects.all().order_by('-created_at')
    kegiatandict = {'kegiatans': kegiatans}
    return render(request, 'main/Kegiatan/Kegiatan.html', context=kegiatandict)

def Create_kegiatan(request):
    kegiatans = {}
    form = kegiatanF(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('admin_kegiatan')
    
    kegiatans['form'] = form
    return render(request, 'main/Kegiatan/Create_kegiatan.html', kegiatans)


def Update_kegiatan(request, id):
    kegiatan_rec = get_object_or_404(kegiatanM, id=id)  # Use get_object_or_404 for better error handling
    form = kegiatanF(request.POST or None, request.FILES or None, instance=kegiatan_rec)

    if form.is_valid():
        form.save()
        return redirect('admin_kegiatan')  # Redirect after successful form submission

    # Pass the form and record to the template for rendering
    context = {'form': form, 'kegiatan_rec': kegiatan_rec}
    return render(request, 'main/Kegiatan/Update_kegiatan.html', context)


def Delete_kegiatan(request, id):
    kegiatan_rec = kegiatanM.objects.get(id=id)
    if request.method == 'POST':
        kegiatan_rec.delete()
        return redirect('admin_kegiatan')
    return render(request, 'main/Kegiatan/Delete_kegiatan.html')


# Views: Manajemen Banner halaman depan
# ======================================================================================================================

def admin_banner(request):
    banners = Banner.objects.all()
    return render(request, "main/Banner/admin_banner.html", {"banners": banners})

def create_banner(request):
    form = BannerForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('admin_banner')

    return render(request, 'main/Banner/create_banner.html', {'form': form})

def update_banner(request, id):
    banner = get_object_or_404(Banner, id=id)
    form = BannerForm(request.POST or None, request.FILES or None, instance=banner)

    if form.is_valid():
        form.save()
        return redirect('admin_banner')

    return render(request, 'main/Banner/update_banner.html', {'form': form, 'banner': banner})

def delete_banner(request, id):
    banner = get_object_or_404(Banner, id=id)
    if request.method == 'POST':
        banner.delete()
        return redirect('admin_banner')

    return render(request, 'main/Banner/delete_banner.html', {'banner': banner})
