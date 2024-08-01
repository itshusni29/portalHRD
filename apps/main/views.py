
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Prosedur
from .forms import ProsedurForm


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from .models import AturanM, ProsedurM
from .forms import AturanF, ProsedurF, SearchForm




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
    today, yesterday, this_month_start, this_year_start = get_date_range()

    today_count = Visitor.objects.filter(timestamp__date=today).count()
    yesterday_count = Visitor.objects.filter(timestamp__date=yesterday).count()
    this_month_count = Visitor.objects.filter(timestamp__date__gte=this_month_start).count()
    this_year_count = Visitor.objects.filter(timestamp__date__gte=this_year_start).count()
    total_hits_count = Visitor.objects.all().count()

    online_users = Session.objects.filter(expire_date__gte=timezone.now()).count()

    # Record the current visitor
    current_visitor_ip = get_client_ip(request)
    Visitor.objects.create(ip_address=current_visitor_ip)

    context = {
        "segment": "index",
        "today_count": today_count,
        "yesterday_count": yesterday_count,
        "this_month_count": this_month_count,
        "this_year_count": this_year_count,
        "total_hits_count": total_hits_count,
        "online_users": online_users,
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
def daftar_prosedur(request):
    # View untuk menampilkan daftar semua prosedur dengan fungsionalitas pencarian.
    daftar_prosedur = Prosedurm.objects.all()

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


# Views: Manajemen Aturan
# ======================================================================================================================
def daftar_aturan(request):
    # View untuk menampilkan daftar semua aturan.
    aturans = Aturan.objects.all()
    return render(request, "main/aturan/daftar_aturan.html", {"aturans": aturans})

def unduh_file_aturan(request, pk):
    # View untuk mengunduh file PDF aturan.
    aturan = get_object_or_404(Aturan, pk=pk)
    return FileResponse(aturan.file_pdf, as_attachment=True)

def buat_aturan(request):
    # View untuk membuat aturan baru.
    if request.method == "POST":
        form = AturanForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("aturan_list")
    else:
        form = AturanForm()
    return render(request, "main/aturan/form_aturan.html", {"form": form, "title": "Buat Aturan"})

def ubah_aturan(request, pk):
    # View untuk memperbarui aturan yang ada.
    aturan = get_object_or_404(Aturan, pk=pk)
    if request.method == "POST":
        form = AturanForm(request.POST, request.FILES, instance=aturan)
        if form.is_valid():
            form.save()
            return redirect("aturan_list")
    else:
        form = AturanForm(instance=aturan)
    return render(request, "main/aturan/form_aturan.html", {"form": form, "title": "Ubah Aturan"})

def hapus_aturan(request, pk):
    # View untuk menghapus aturan.
    aturan = get_object_or_404(Aturan, pk=pk)
    if request.method == "POST":
        aturan.delete()
        return redirect("aturan_list")
    return render(request, "main/aturan/konfirmasi_hapus_aturan.html", {"aturan": aturan})
