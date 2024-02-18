from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer, UserDetailSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

#Update
from rest_framework.permissions import IsAuthenticated
from .serializers import UserUpdateSerializer

from django.contrib.auth import get_user_model


#fast AI 

from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .serializers import PlantImageSerializer
from .models import PlantImage , Detection
from .detection import Plant_Disease_Detection  # Import your model function
from .recommendation import generate_recommendations


#detections
from rest_framework import generics
from .models import Detection
from .serializers import DetectionSerializer
from rest_framework.permissions import IsAuthenticated

class UserRegistrationView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully.", "data": serializer.data}, status=status.HTTP_201_CREATED)
        
        # Handling errors more explicitly
        errors = {}
        for field, value in serializer.errors.items():
            errors[field] = " ".join(value)
        return Response({"errors": errors, "message": "Please correct the errors below."}, status=status.HTTP_400_BAD_REQUEST)

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        token['full_name'] = user.get_full_name()  # Assuming you have a method to get the full name
        token['bio'] = user.bio  # Assuming 'bio' is a field on your user model
        # For 'profile_photo', ensure you add a method or property in your user model to get the full URL if it's not stored as a full URL
        token['profile_photo'] = user.get_profile_photo_url()  # Use the method from the model

        return token

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # If the serializer is valid, return the token and success message
            return Response({
                'message': 'Authentication successful.',
                'status': 'success',
                'token': serializer.validated_data,
            }, status=status.HTTP_200_OK)
        else:
            # If the serializer is not valid, return the error details
            return Response({
                'errors': serializer.errors,
                'message': 'Authentication failed. Please check the provided credentials.',
                'status': status.HTTP_401_UNAUTHORIZED
            }, status=status.HTTP_401_UNAUTHORIZED)
        

class PlantDiseaseDetectionAPIView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)



    def post(self, request, *args, **kwargs):
        file_serializer = PlantImageSerializer(data=request.data)
        if file_serializer.is_valid():
            image_file = request.FILES.get('image')
            prediction, confidence,description = Plant_Disease_Detection(image_file)  # Use the updated function here
            recommendations = generate_recommendations(prediction)
            print(recommendations)

                        # Save the detection details to the database
            Detection.objects.create(
                user=request.user,
                image=image_file,
                prediction=prediction,
                confidence=confidence,
                description=description,
                recommendations=recommendations
            )
            return Response({
                'message': 'Authentication successful.',
                'prediction': prediction,
                'confidence': float(confidence),
                'description': description,
                'recommendations': recommendations,
                # 'status': status,
            }, status=status.HTTP_200_OK)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


class UserUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        user = request.user
        serializer = UserUpdateSerializer(user, data=request.data, partial=True)  # `partial=True` allows partial updates

        if serializer.is_valid():
            serializer.save()
            # Include a custom message with the response data
            response_data = {
                'message': 'User details updated successfully.',
                'update_data': serializer.data,
                'update_status': 'Success' 
            }
            return Response(response_data, status=status.HTTP_200_OK)

        # Include a custom error message along with validation errors from the serializer
        response_data = {
            'message': 'Failed to update user details. Please check the provided data.',
            'errors': serializer.errors
        }
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


#Dashboards
    
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.response import Response
#from your_app.models import Detection, User  # Update with your actual model names
from django.contrib.auth.models import User

# Use Django's way to reference the custom user model
User = get_user_model()
class StatsView(APIView):
    def get(self, request, *args, **kwargs):
        #total_detections = Detection.objects.count()  # Assuming Detection model tracks each detection
        total_users = User.objects.count()
        active_users = User.objects.filter(is_active=True).count()
        
        # Static data for plant diseases as per your specifications
        unique_plants = [
            'Tomato', 'Grape', 'Orange', 'Soybean', 'Squash', 'Potato', 
            'Corn_(maize)', 'Strawberry', 'Peach', 'Apple', 'Blueberry', 
            'Cherry_(including_sour)', 'Pepper,_bell', 'Raspberry'
        ]
        number_of_plants = len(unique_plants)
        number_of_diseases = 26  # Static as per your data
        
        response_data = {
            'total_users': total_users,
            'total_active_users': active_users,
            'number_of_plants': number_of_plants,
            'number_of_diseases': number_of_diseases,
            'unique_plants': unique_plants
        }

        return Response(response_data)
    

#Detection Records
    
class UserDetectionListAPIView(generics.ListAPIView):
    serializer_class = DetectionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Return detections only for the current authenticated user
        return Detection.objects.filter(user=self.request.user)