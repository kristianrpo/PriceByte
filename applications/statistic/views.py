import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import pandas as pd
import base64
from django.shortcuts import render, redirect
from applications.product.models import Product
from applications.seller.models import Seller
from applications.review.models import ProductRating
from django.utils.safestring import mark_safe
from django.db.models import Avg
import math 

def generate_category_chart(vendor):
    products_of_vendor = Product.objects.filter(distributed_by_product=vendor)

    categories = set()
    for product in products_of_vendor:
        categories.update(product.categories_product.values_list('name_category', flat=True))

    categories_list = list(categories)

    product_counts = [products_of_vendor.filter(categories_product__name_category=category).count() for category in categories_list]

    plt.figure(figsize=(8, 4))

    x = np.arange(len(categories_list))
    bar_width = 0.5
    colors = plt.cm.Greens(np.linspace(0.2, 1, len(categories_list)))

    plt.bar(x, product_counts, width=bar_width, color=colors)
    plt.xlabel('Categorías')
    plt.ylabel('Cantidad de Productos')
    plt.title('Productos por categoría')

    plt.xticks(x, categories_list, rotation=45, ha='right')
    plt.yticks(np.arange(max(product_counts) + 1))

    plt.tight_layout(pad=2.0)

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode()
    buffer.close()

    return image_base64, categories_list


def generate_price_rating_chart(vendor):
    products = Product.objects.filter(distributed_by_product=vendor)
    reviews_vendor = ProductRating.objects.filter(product__in=products)

    calificaciones_precio = [calificacion['price_rating'] for calificacion in reviews_vendor.values('price_rating')]

    plt.figure(figsize=(8, 4))
    colors = plt.cm.Greens(np.linspace(0.2, 1, 5))
    bar_width = 0.5
    x = np.arange(1, 6)

    rating_counts = [calificaciones_precio.count(rating) for rating in x]

    plt.bar(x, height=rating_counts, width=bar_width, color=colors)
    plt.xlabel('Calificación por Precio')
    plt.ylabel('Número de Productos')
    plt.title('Calificación por Precio de los Productos')

    plt.yticks(np.arange(max(rating_counts) + 1))

    plt.tight_layout(pad=2.0)

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode()
    buffer.close()

    return image_base64, x


def generate_warranty_rating_chart(vendor):
    products = Product.objects.filter(distributed_by_product=vendor)
    reviews_vendor = ProductRating.objects.filter(product__in=products)

    calificaciones_garantia = [calificacion['warranty_rating'] for calificacion in reviews_vendor.values('warranty_rating')]

    plt.figure(figsize=(8, 4))
    colors = plt.cm.Greens(np.linspace(0.2, 1, 5))
    bar_width = 0.5
    x = np.arange(1, 6)

    rating_counts = [calificaciones_garantia.count(rating) for rating in x]

    plt.bar(x, height=rating_counts, width=bar_width, color=colors)
    plt.xlabel('Calificación por garantía')
    plt.ylabel('Número de Productos')
    plt.title('Calificación por garantía de los Productos')

    plt.yticks(np.arange(max(rating_counts) + 1))

    plt.tight_layout(pad=2.0)

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode()
    buffer.close()

    return image_base64, x


def generate_quality_rating_chart(vendor):
    products = Product.objects.filter(distributed_by_product=vendor)
    reviews_vendor = ProductRating.objects.filter(product__in=products)

    calificaciones_calidad = [calificacion['quality_rating'] for calificacion in reviews_vendor.values('quality_rating')]

    plt.figure(figsize=(8, 4))
    colors = plt.cm.Greens(np.linspace(0.2, 1, 5))
    bar_width = 0.5
    x = np.arange(1, 6)

    rating_counts = [calificaciones_calidad.count(rating) for rating in x]

    plt.bar(x, height=rating_counts, width=bar_width, color=colors)
    plt.xlabel('Calificación por calidad')
    plt.ylabel('Número de Productos')
    plt.title('Calificación por calidad de los Productos')

    plt.yticks(np.arange(max(rating_counts) + 1))

    plt.tight_layout(pad=2.0)

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode()
    buffer.close()

    return image_base64, x

def bar_chart(request, vendor_name):
    if not request.user.is_authenticated:
        return redirect('loginaccount')

    try:
        vendor = Seller.objects.get(name_company_seller=vendor_name)

        
        category_chart_base64, categories_list = generate_category_chart(vendor)
        price_rating_chart_base64, rating_categories = generate_price_rating_chart(vendor)
        warranty_rating_chart_base64, rating_categories = generate_warranty_rating_chart(vendor)
        quality_rating_chart_base64, rating_categories = generate_quality_rating_chart(vendor)

    
        charts_data = {
            'category_chart_base64': category_chart_base64,
            'categories_list': categories_list,
            'price_rating_chart_base64': price_rating_chart_base64,
            'warranty_rating_chart_base64': warranty_rating_chart_base64,
            'quality_rating_chart_base64': quality_rating_chart_base64,
            'rating_categories': rating_categories,
        }

        if hasattr(request.user, 'type'):
            if request.user.type == "vendedor":
                is_seller = "Si"
            else:
                is_seller = "No"
        else:
            is_seller = "No"
        context = {
            'vendor_name': vendor_name,
            'charts_data': charts_data,
            'is_seller':is_seller,
        }

        return render(request, 'statistic/chart.html', context)

    except Seller.DoesNotExist:
        return render(request, 'vendor_not_found.html')

def quality_products(request, vendor_name):

    vendor = Seller.objects.get(name_company_seller=vendor_name)
    products = Product.objects.filter(distributed_by_product=vendor)
    reviews_vendor = ProductRating.objects.filter(product__in=products)

    product_avg_ratings = {}
    for product in products:
        product_reviews = reviews_vendor.filter(product=product)
        avg_rating = product_reviews.aggregate(avg_rating=Avg('quality_rating'))['avg_rating']

        if avg_rating is not None:
            avg_rating_str = f'{avg_rating:.2f}'
        else:
            avg_rating_str = 'No aplica'

        product_avg_ratings[product.name_product] = avg_rating_str

    df = pd.DataFrame(list(product_avg_ratings.items()), columns=['Nombre del Producto', 'Calificación Promedio'])

    plt.style.use('seaborn-darkgrid')
    plt.figure(figsize=(10, 4))  

    ax = plt.subplot(111, frame_on=False)
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)

    table = pd.plotting.table(ax, df, loc='center', colWidths=[0.2, 0.2])

    table.set_fontsize(15)

    table.scale(1.5, 1.5)  

    header_cells = table.get_celld()
    for key, cell in header_cells.items():
        if key[0] == 0:  
            cell.set_fontsize(18)  
            cell.set_text_props(weight='bold', color='white')
            cell.set_facecolor('#537072')  

    
    plt.tight_layout()

    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()

    data_uri = base64.b64encode(buf.read()).decode('utf-8')

    context = {
        'vendor_name': vendor_name,
        'quality_chart_data_uri': f'data:image/png;base64,{data_uri}',
    }

    return render(request, 'statistic/quality.html', context)
