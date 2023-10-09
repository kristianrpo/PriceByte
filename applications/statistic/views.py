import matplotlib.pyplot as plt
from io import BytesIO
import base64
from django.shortcuts import render, redirect
from applications.product.models import Product
from applications.seller.models import Seller
import numpy as np

def bar_chart(request, vendor_name):
    if not request.user.is_authenticated:
        return redirect('loginaccount') 
    try:
        vendor = Seller.objects.get(name_company_seller=vendor_name)
        products_of_vendor = Product.objects.filter(distributed_by_product=vendor)
        
        # Obtener todas las categorías únicas de los productos del vendedor
        categories = set()
        for product in products_of_vendor:
            categories.update(product.categories_product.values_list('name_category', flat=True))

        # Convertir el conjunto de categorías en una lista
        categories_list = list(categories)

        # Contar la cantidad de productos en cada categoría
        product_counts = [products_of_vendor.filter(categories_product__name_category=category).count() for category in categories_list]

        plt.figure(figsize=(8, 4))  # Cambiar el tamaño del gráfico
        
        # Crear ubicaciones numéricas para las barras en el eje x
        x = np.arange(len(categories_list))
        
        # Ajustar el ancho de las barras
        bar_width = 0.5

        # Utilizar la paleta de colores predefinida "Greens"
        colors = plt.cm.Greens(np.linspace(0.2, 1, len(categories_list)))  # Ajusta el rango de colores
        
        plt.bar(x, product_counts, width=bar_width, color=colors)
        plt.xlabel('Categorías')
        plt.ylabel('Cantidad de Productos')
        plt.title('Productos por Categoría')
        
        # Establecer las etiquetas del eje x
        plt.xticks(x, categories_list, rotation=45, ha='right')

        buffer = BytesIO()
        plt.tight_layout()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode()
        buffer.close()

        if hasattr(request.user, 'type'):
            if request.user.type == "vendedor":
                is_seller = "Si"
            else:
                is_seller = "No"
        else:
            is_seller = "No"
        context = {
            'image_base64': image_base64,
            'vendor_name': vendor_name,
            'categories_list': categories_list,
            'is_seller' : is_seller,
        }
        return render(request, 'statistic/chart.html', context)
    except Seller.DoesNotExist:
        return render(request, 'vendor_not_found.html')
