from django.db import models
from rest_framework import serializers
from expense.models import Expenses
from django.db.models import Sum
from rest_framework import viewsets


class ExpenseSerializer(serializers.ModelSerializer):

    totalExpense = serializers.IntegerField()
    many=True

    class Meta:
        model = Expenses
        fields = ['User_ID_id', 'Catagory', 'Date_Time','totalExpense']

class ExpenseViewSet(viewsets.ModelViewSet):

    Model = Expenses
    # queryset = Expenses.objects.all()
    serializer_class = ExpenseSerializer

    def get_queryset(self):

        type = self.request.query_params.get('type')
        if type=='pie':
            queryset= Expenses.objects.values('Catagory').annotate(totalExpense=Sum('Amount')).order_by('-totalExpense')
        else:
            queryset = Expenses.objects.values('Date_Time__date').annotate(totalExpense=Sum('Amount')).order_by('Date_Time__date')
        return queryset