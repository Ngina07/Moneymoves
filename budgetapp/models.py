from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

class Project(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    budget = models.IntegerField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

# Auto generates slug
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Project,self).save(*args, **kwargs)

    def budget_left(self):
        expense_list = Expense.objects.filter(project=self)
        total_expense_amount = 0
        for expense in expense_list:
            total_expense_amount += expense.amount

        return self.budget - total_expense_amount


    def total_transactions(self):
        expense_list = Expense.objects.filter(project=self)
        return len(expense_list)

    def __str__(self):
        return self.name

class Category(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Expense(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE,related_name='expenses')
    title = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-amount',)

