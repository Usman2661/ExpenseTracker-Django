from rest_framework import serializers
from expense.models import Expenses
from rest_framework import viewsets


class ExpenseSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Expenses
        fields = ('User_ID', 'Amount', 'Catagory', 'Date_Time')

class ExpenseViewSet(viewsets.ModelViewSet):

    queryset = Expenses.objects.all()
    serializer_class = ExpenseSerializer