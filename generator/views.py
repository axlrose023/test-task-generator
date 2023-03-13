import csv
import datetime
import json
import os.path

from django.conf import settings

from .utils import fake_data
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden, FileResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect

from .forms import SchemaForm, SchemaColumnsForm, EditSchemaForm
# Create your views here.
from generator.models import DataSchema, Column, CsvFile


@login_required(login_url='login')
def data_schemas(request):
    user = request.user
    schemas = DataSchema.objects.filter(user=user).order_by('-created_at')
    context = {'schemas': schemas}
    return render(request, 'generator/main.html', context)


@login_required()
def new_schem(request):
    if request.method == 'POST':
        title = request.POST.get('schema_name')
        column_separator = request.POST.get('column_separator')
        string_character = request.POST.get('string_character')
        schema = DataSchema(title=title, column_separator=column_separator,
                            string_character=string_character, user=request.user)
        schema.save()
        return HttpResponse('success')


@login_required(login_url='login')
def add_schema(request):
    if request.method == 'POST':
        column_name = request.POST.get('column_name')
        data_type = request.POST.get('data_type')
        order = request.POST.get('order')
        from_int = request.POST.get('input1')
        to_int = request.POST.get('input2')
        schema = DataSchema.objects.filter(user=request.user).last()
        column = Column(name=column_name, data_type=data_type, order=order, schema=schema, range_min=from_int,
                        range_max=to_int)
        column.save()

        dict = {
            'column_name': column_name,
            'data_type': data_type,
            'order': order,
        }
        return JsonResponse(dict)
    return render(request, 'generator/new_schema.html')


@login_required(login_url='login')
def edit_scheme(request, pk):
    scheme = get_object_or_404(DataSchema, pk=pk)
    columns = Column.objects.filter(schema=scheme)
    if scheme.user != request.user:
        return HttpResponseForbidden()
    form = EditSchemaForm(request.POST, instance=scheme)
    if form.is_valid():
        title = form.cleaned_data['title']
        column_separator = form.cleaned_data['column_separator']
        string_character = form.cleaned_data['string_character']
        form.save()
        messages.success(request, 'Form saved successfully!')
        return redirect('data_schemas')
    if request.method == 'POST':
        rows = request.POST.get('rows')
        data_types = []
        fake_types = []
        for i in range(int(rows)):
            f_data = []
            for column in columns:
                i += 1
                data_type = column.data_type
                if data_type not in data_types:
                    data_types.append(data_type)
                from_int = column.range_min
                to_int = column.range_max
                fake = fake_data(data_type)
                if fake is not None and fake != "":
                    f_data.append(fake)
                column_name = column.name
                order = column.order
            fake_types.append(f_data)
        print(data_types)
        print(fake_types)
        with open(f'media/{scheme.title}.csv', 'a', newline='') as file:
            writer = csv.writer(file, delimiter=scheme.column_separator, quotechar=scheme.string_character)
            writer.writerow(data_types)
            writer.writerows(fake_types)
    file_path = os.path.join(settings.MEDIA_ROOT, f'{scheme.title}.csv')
    if os.path.exists(file_path):
        status = 'Active'
    else:
        status = 'Processing'

    context = {
        'scheme': scheme,
        'columns': columns,
        'form': form,
        'status': status,
    }
    return render(request, 'generator/edit_scheme.html', context)


def download_file(request, filename):
    filename = filename + '.csv'
    file_path = os.path.join(settings.MEDIA_ROOT, filename)
    if os.path.exists(file_path):
        response = FileResponse(open(file_path, 'rb'), as_attachment=True)
        return response
    else:
        raise Http404


@login_required(login_url='login')
def delete_scheme(request, pk):
    scheme = DataSchema.objects.get(pk=pk)
    scheme.delete()
    return redirect('data_schemas')


@login_required(login_url='login')
def delete_column(request, pk):
    column = get_object_or_404(Column, pk=pk)
    column.delete()
    return redirect('edit_scheme', pk=column.schema.pk)


def data_sets(request):
    return render(request, 'generator/data_sets.html')
