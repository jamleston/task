from django.views.generic.list import ListView
from django.utils.dateparse import parse_date
from django.db import models

from .forms import ExpenseSearchForm
from .models import Expense, Category
from .reports import summary_per_category, summary_per_month


class ExpenseListView(ListView):
    model = Expense
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = object_list if object_list is not None else self.object_list

        form = ExpenseSearchForm(self.request.GET)
        if form.is_valid():
            name = form.cleaned_data.get('name', '').strip()
            date_from = form.cleaned_data.get('date_from')
            date_to = form.cleaned_data.get('date_to')
            categories = form.cleaned_data.get('categories')

            if name:
                queryset = queryset.filter(name__icontains=name)
            if date_from:
                queryset = queryset.filter(date__gte=date_from)
            if date_to:
                queryset = queryset.filter(date__lte=date_to)
            if categories.exists():
                queryset = queryset.filter(category__in=categories)
        
        sort_by = self.request.GET.get('sort_by', 'date')  
        order = self.request.GET.get('order', 'asc')

        if sort_by == "category":
            queryset = queryset.order_by('category__name' if order == 'asc' else '-category__name')
        elif sort_by == "date":
            queryset = queryset.order_by('date' if order == 'asc' else '-date')

        total_spent = queryset.aggregate(total=models.Sum('amount'))['total'] or 0

        summary_per_month_data = summary_per_month(queryset)

        return super().get_context_data(
            form=form,  
            object_list=queryset,  
            summary_per_category=summary_per_category(queryset), 
            summary_per_month_data=summary_per_month_data, 
            sort_by=sort_by,
            order=order,
            total_spent=total_spent,
            **kwargs
        )

class CategoryListView(ListView):
    model = Category
    paginate_by = 5

