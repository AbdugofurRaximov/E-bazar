from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Products, ProductsImage, Comment
from .forms import NewProductForm, ProductForm

@login_required(login_url='login')
def new_product(request):
    if request.method == 'GET':
        form = NewProductForm()
        return render(request, 'product_new.html', {'form': form})

    elif request.method == "POST":
        form = NewProductForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            products = form.save(request)

            for image in request.FILES.getlist('images'):
                ProductsImage.objects.create(image=image, products=products)

            messages.success(request, 'Successfully Created!')
            return redirect('main:index')
        return render(request, 'product_new.html', {'form': form})


def product_detail(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    return render(request, 'product_detail.html', {'product': product})


@login_required(login_url='login')
def product_update(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    if request.user == product.author:
        if request.method == 'GET':

            form = ProductForm(instance=product)
            return render(request, 'product_update.html', {'form': form, 'pr': product})

        elif request.method == "POST":
            form = ProductForm(instance=product, data=request.POST, files=request.FILES)
            if form.is_valid():
                form.save()
                if request.FILES.getlist('images'):
                    ProductsImage.objects.filter(product=product).delete()
                for image in request.FILES.getlist('images'):
                    ProductsImage.objects.create(image=image, product=product)

                messages.success(request, 'Successfully Updated!')
                return redirect('products:detail', product_id)
            return render(request, 'product_update.html', {'form': form , 'pr': product})

    else:
        messages.error(request, 'Access denied! ')
        return redirect('main:index')

@login_required(login_url='login')

def product_delete(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    if request.user == product.author:
        if request.method == 'POST':
            product.delete()
            messages.info(request, 'Successfully Deleted!')
            return redirect('main:index')
        return render(request, 'product_delete.html', {'product': product})
    else:
        messages.error(request, 'Access Denied!')
        return redirect('main:index')


@login_required(login_url='login')
def new_comment(request, product_id):
    products = get_object_or_404(Products, id=product_id)
    if request.method == 'POST':
        Comment.objects.create(
            author=request.user,
            products=products,
            body=request.POST['body']
        )

        messages.info(request, 'Successfully Sended!')
        return redirect('products:detail', product_id)
    return HttpResponse('Add comment')


@login_required(login_url='login')

def delete_comment(request, product_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user == comment.author:
        comment.delete()
        messages.info(request, 'Successfully Deleted!')
        return redirect('products:detail', product_id)
    return redirect('products:detail', product_id)
