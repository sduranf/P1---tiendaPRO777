from django.db.models import Q
from django.shortcuts import get_list_or_404, get_object_or_404, render, redirect
from django.core.files.base import ContentFile
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from openai import OpenAI, OpenAIError  # Add OpenAIError here
from .models import Category, Item
from .forms import ItemForm
from .services import get_item_details
import uuid

# Create your views here.
def index(request):
    items = Item.objects.filter(is_sold=False)[:8]
    return render(
        request,
        "items/index.html",
        {
            "items": items,
        },
    )


def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    return render(
        request,
        "items/detail.html",
        {
            "item": item,
        },
    )


def browse(request):
    query = request.GET.get("query", "")
    category_id = request.GET.get("category", "0")
    categories = Category.objects.all()
    items = Item.objects.filter(is_sold=False)

    if category_id and category_id != "0":
        items = items.filter(category_id=category_id)

    if query:
        items = items.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

    return render(
        request,
        "items/browse.html",
        {
            "items": items,
            "query": query,
            "categories": categories,
            "category_id": int(category_id),
        },
    )

def about(request):
    return render(request, "items/about.html")

@login_required
def create_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            try:
                item = form.save(commit=False)
                ai_prompt = form.cleaned_data.get('ai_prompt')
                
                try:
                    # Get AI-generated content
                    ai_content = get_item_details(ai_prompt)
                    
                    # Set the description and price
                    item.description = ai_content['description']
                    item.price = ai_content['price']
                    
                    # Save the generated image
                    image_name = f"ai_generated_{uuid.uuid4()}.png"
                    item.image.save(image_name, ContentFile(ai_content['image_content']), save=False)
                    
                    item.save()
                    messages.success(request, 'Successfully created new clothes with AI-generated content!')
                    return redirect('items:index')
                    
                except OpenAIError as e:
                    messages.error(request, str(e))
                    return render(request, 'items/create_item.html', {
                        'form': form,
                        'title': 'Create New Clothes'
                    })
                    
            except Exception as e:
                messages.error(request, f'Error creating item: {str(e)}')
                return render(request, 'items/create_item.html', {
                    'form': form,
                    'title': 'Create New Clothes'
                })
    else:
        form = ItemForm()
    
    return render(request, 'items/create_item.html', {
        'form': form,
        'title': 'Create New Clothes'
    })