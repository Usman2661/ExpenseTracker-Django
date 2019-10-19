from django.db import models
from rest_framework import serializers
from expense.models import Expenses
from django.db.models import Sum
from rest_framework import viewsets


class ExpenseSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Expenses
        fields = ('User_ID_id','Amount', 'Catagory', 'Date_Time',)

class ExpenseViewSet(viewsets.ModelViewSet):

    Model = Expenses
    serializer_class = ExpenseSerializer

    def get_queryset(self):

        id = self.request.query_params.get('UserID')
        if id is None:
            queryset = Expenses.objects.aggregate(Sum('Amount'))
        else:
            queryset = Expenses.objects.filter(User_ID_id=id).aggregate(Sum('Amount'))
        return queryset
