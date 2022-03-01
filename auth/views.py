from django.shortcuts import render

from rest_framework.permissions import IsAuthenticated , IsAdminUser

from rest_framework.response import Response

from rest_framework.views import APIView

from django.contrib.auth.models import User

from .serializers import *

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from rest_framework_simplejwt.views import TokenObtainPairView

from django.contrib.auth.hashers import make_password

from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken


class MyTokenObtainPairSeralizer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializerWithToken(self.user).data

        for k , v in serializer.items():
            data[k] = v

        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSeralizer



class Register(APIView):
    def post(self,request):
        data = request.data

        try:
            user = User.objects.create(
                first_name = data['name'],
                username = data['username'],
                email = data['email'],
                password = make_password(data['password'])
            )
            serializer = UserSerializer(user,many=False)
            return Response(serializer.data)
        except:
            return Response({"msg":'user is already exists'})



class Logout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        token = request.data["token"]
        data = RefreshToken(token)
        data.blacklist()
        return Response("Successful Logout", status=status.HTTP_200_OK)
    
    
    {% extends 'base.html' %}
{% block title %} Carrier Form {% endblock %}


{% block main %}
<script src="/path/to/cdn/jquery.slim.min.js"></script>
{% load static %}

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-ka7Sk0Gln4gmtz2MlQnikT1wXgYsOg+OMhuP+IlRH9sENBO0LRn5q+8nbTov4+1p" crossorigin="anonymous"></script>
<script src="{% static 'assets/js/vendors/jquery-3.6.0.min.js' %}"></script>



<script>


function getCookie(cname) {
     var name = cname + "=";
     var ca = document.cookie.split(';');
     for(var i=0; i<ca.length; i++) {
         var c = ca[i];
         while (c.charAt(0)==' ') c = c.substring(1);
         if(c.indexOf(name) == 0)
            return c.substring(name.length,c.length);
     }
     return "";
}

    var mediaArray = [];

    jQuery(function ($) {

  var selectedMediasId;
  var isMultipleAllowed = false;
  $('#allowmultiple').click(function () {
      isMultipleAllowed = $('#allowmultiple').is(':checked') ? true : false;
      $('.image-checkbox-checked').each(function () {
          $(this).removeClass('image-checkbox-checked');
      });
      mediaArray = [];
      $('#selectedmediapreview').html('');
  });
  $(".image-checkbox").on("click", function (e) {
      var selected = $(this).find('img').attr('su-media-id');
      //console.log(selected);
      if ($(this).hasClass('image-checkbox-checked')) {
          $(this).removeClass('image-checkbox-checked');
          // remove deselected item from array
          mediaArray = $.grep(mediaArray, function (value) {
              return value != selected;
          });
      }
      else {
          if (isMultipleAllowed == false) {
              $('.image-checkbox-checked').each(function () {
                  $(this).removeClass('image-checkbox-checked');
              });
              mediaArray = [];
              mediaArray.push(selected);
          } else {
              if (mediaArray.indexOf(selected) === -1) {
                  mediaArray.push(selected);
              }
          }
          $(this).addClass('image-checkbox-checked');
      }
      //console.log(selected);
      console.log("Media Array",mediaArray);
      selectedMediasId = mediaArray.join(",");


      console.log(selectedMediasId);
      $('#selectedmediapreview').html('<div class="alert alert-success"><pre lang="js">' + JSON.stringify(mediaArray.join(", "), null, 4) + '</pre></div>');
      //console.log(isMultipleAllowed);
      e.preventDefault();
  });



});



function update_button() {
    console.log(mediaArray)
    $.ajaxSetup({
          headers: {
            "X-CSRFToken": getCookie("csrftoken")
          },
        });
    $.ajax({
        type:"POST",
        url: "{% url 'image' %}",
        data: {"img_id":String(mediaArray)},
        success: function(response){
            // do something with response

            response['result']; // equals 'Success or failed';
            response['message'] // equals 'you"re logged in or You messed up';
         }
    });
}



</script>

<style>
.image-checkbox {
  cursor: pointer;
  box-sizing: border-box;
  -moz-box-sizing: border-box;
  -webkit-box-sizing: border-box;
  border: 3px solid transparent;
  box-shadow: 0 0 4px #ccc;
  outline: 0;
  margin: 4px;
  border-radius: 12px;
}

.image-checkbox-checked {
  border-color: #2196f3;
}

img {
  border-radius: 8px;
  max-height: 160px !important;
  max-width: -webkit-fill-available;
}

.image-checkbox i {
  display: none;
  color: #2196f3;
}

.image-checkbox-checked{
  position: relative;
}

.image-checkbox-checked i {
  display: block;
  position: absolute;
  top: 10px;
  right: 10px;
}
</style>

    <section class="content-main">
        <form  onsubmit="update_button()" >
            {% csrf_token %}

            <input type="checkbox"  class="custom-control-input" id="allowmultiple">
            <label class="custom-control-label" for="allowmultiple" style="cursor: pointer;">
            </label>

            <div class="col-lg-5" id="selectedmediapreview"></div>

            <div class="row " style="background-color: white">
                {% for x in image %}

                    <div class="col-lg-3">
                        <label class="image-checkbox">
                          <img su-media-id="{{ x.id }}" height="100px" width="100px" src="{{ x.image.url }}" />
                          <i class="fa fa-check"></i>
                        </label>
                    </div>
                {% endfor %}
            </div>

            <input type="submit" class="btn btn-secondary">
        </form>

       </div>
    </section>
{% endblock %}


    
    
