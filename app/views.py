from django.shortcuts import render,get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import *
from .serializers import *
from django.utils import timezone
from django.contrib.auth.models import User


#---------------------------------------------------------------------------------

class Products(APIView):
    #permission_classes = [IsAuthenticated]
    def get(self,request):
        pro = Product.objects.all()
        serializer = ProductSerializer(pro,many=True)
        return Response(serializer.data)



class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request,pk):
        pro = get_object_or_404(Product,pro_id = pk)

        item , create = AddToCart.objects.get_or_create(user = request.user , pro_id = pro , ordered=False)

        order  = Order.objects.filter(user = request.user ,ordered=False)

        if order.exists():
            order_id  = order[0]

            if order_id.items.filter(pro_id__pro_id = pk, ordered=False):
                item.qty +=1
                item.save()
                serializer = AddTocartSerializer(item,many=False)
                return Response(serializer.data)
            else:
                order_id.items.add(item)
                order_id.save()
                serializer = AddTocartSerializer(item, many=False)
                return Response(serializer.data)

        else:
            order = order.create(user=request.user)
            order.items.add(item)
            order.save()
            serializer = AddTocartSerializer(item,many=False)
            return Response(serializer.data)




class RemoveItemFormCart(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request,pk):
        pro = get_object_or_404(Product,pro_id = pk)

        order = Order.objects.filter(user=request.user,ordered=False)

        if order.exists():
            order_as  = order[0]
            if order_as.items.filter(pro_id__pro_id = pk , ordered = False).exists():
                item = AddToCart.objects.get(pro_id = pro,user=request.user,ordered=False)
                if(item.qty > 1):
                    item.qty -= 1
                    item.save()
                    serializer = AddTocartSerializer(item)
                    return Response(serializer.data)
                else:
                    order_as.items.remove(item)
                    item.delete()
                    return Response({'msg':'data is deleted'})
            else:
                return Response({'msg':'Product Not Avalable'})
        else:
            return Response({'msg':'This is invalid'})



class MyAddress(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        address = Address.objects.filter(user=request.user)
        serializer = AddressSerializer(address,many=True)
        return Response(serializer.data)




class Checkout(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request,pk):

        try:
            address = Address.objects.get(id = pk,user=request.user)
            order = Order.objects.get(user=request.user,ordered=False)
            order.address = address
            order.save()
            serializer = AddressSerializer(address)
            return Response(serializer.data)
        except:
            return Response({'this user address is not avalable'})




class CheckoutByNewAddress(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        data = request.data

        try:
            address = Address.objects.create(
                user = request.user,
                name = data['name'],
                contact= data['contact'],
                address= data['address'],
                city= data['city'],
                pin_code = data['pincode'],
                landmark = data['landmark'],
                email= data['email'],
                alternative_no = data['alternativeno']
            )
        except:
            return Response({'msg':'form is not vaild'})

        try:
            order = Order.objects.get(user=request.user , ordered=False)
            order.address = address
            order.save()
            serializer = AddressSerializer(address)
            return Response(serializer.data)
        except:
            return Response({'this user address is not avalable'})




class PaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        con = Order.objects.get(user = request.user,ordered=False)

        if con.address is not None:
            pay  = Payment()
            pay.user  = request.user
            pay.ordered = True
            pay.order_id = con
            pay.amount = con.get_total_price()
            pay.save()

            data = con.items.all()
            data.update(ordered=True)
            for x in data:
                x.save()

            con.ordered = True
            con.order_date = timezone.now()
            con.save()
            return Response({'msg':'your order Success fully'})




class MyOrder(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        order = Order.objects.filter(user=request.user,ordered=True)
        serializer = OrderSerializer(order)
        return Response(serializer.data)



class MyCart(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self,request):
        content = AddToCart.objects.filter(user=request.user,ordered=False)
        serializer  = AddTocartSerializer(content,many=True)
        return Response(serializer.data)




#https://www.geeksforgeeks.org/how-to-validate-pan-card-number-using-regular-expression/?ref=lbp


# direct json data send by Resonse 
# class UserProfile(APIView):
#     permission_classes = (IsAuthenticated,)
#     def get(self,request):
#         list = []
#         user = User.objects.get(username = request.user)
#         get_state = user.employees_id.states.all()

#         st = StateSerializer(get_state,many=True)

#         data ={
#             'username':user.username,
#             'email':user.employees_id.email,
#             'state':user.employees_id.state.state_name,
#             'states':(st.data)
#         }
#         list.append(data)
#         return Response(list)










