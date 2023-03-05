import io
from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.files.images import ImageFile
from .forms import UploadFileForm
from .models import MarketChart, Script
from utils.main_sc import main
from utils.handle_csv_file import get_data_from_csv



def create_script_name(name):
        """
        Create Transaction for this request
        """
        return Script.objects.create(
            name=name,
        )


def index(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            script_name = form.cleaned_data['title']
            csv_file = form.cleaned_data['file']
            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'File is not CSV type')
                return redirect('index')
            # If file is too large
            if csv_file.multiple_chunks():
                messages.error(request, 'Uploaded file is too big (%.2f MB)' %(csv_file.size(1000*1000),))
                return redirect('index')
            asins, marketplaces, zipcodes, brands = get_data_from_csv(csv_file)
            fig=main(asins, marketplaces, zipcodes, brands)
            img_html = fig.to_html()
            # img_bytes = fig.to_image(format='png')
            # img_file = ImageFile(io.BytesIO(img_bytes), name='chart.png')
            sc = create_script_name(script_name)
            cg = MarketChart.objects.create(script=sc, chart_img=img_html)
            return redirect('chart')
            
    else:
        form = UploadFileForm()
    return render(request, 'helium10/index.html', {'form': form})


def chart(request):
    charts = MarketChart.objects.all()
    return render(request, 'helium10/chart.html', {'charts': charts})

def chart_detail(request, id):
    img = MarketChart.objects.filter(id=id).first()
    return render(request, 'helium10/chart_detail.html', {'img': img, 'request':request})