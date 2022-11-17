from rest_framework import serializers
from authApp.models.user import User
from authApp.models.account import Account
from authApp.serializers.accountSerializer import AccountSerializer

class UserSerializer(serializers.ModelSerializer):
    account = AccountSerializer()
    class Meta:
        model = User
        fields = ['id','username','password','name','email','account']

    def create (self, validated_data): #Deserializaci√≥n JSON a OBjeto Python
        accountData = validated_data.pop('account')
        userInstance = User.objects.create(**validated_data)
        Account.objects.create(user = userInstance,**accountData)
        return userInstance
    
    def to_representation(self, obj): # Serializaci√≥n objeto Python a JSON
        user = User.objects.get(id = obj.id)
        account = Account.objects.get(user = obj.id)
        return {
            'id':user.id,
            'username': user.username,
            'name': user.name,
            'email': user.email,
            'acount':{#por este error saca error en el frontend
                'id':account.id,
                'balance':account.balance,
                'lastChangeDate': account.lastChangeDate,
                'isActive': account.isActive
            }
        }
    