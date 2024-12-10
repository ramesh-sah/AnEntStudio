from django.shortcuts import render, HttpResponse

from api.models import (Slider, Add,Category, Event, Genre, Image, Video,  VideoCategory, EventVotingSettings, 
                        UserEventVoting, Album, AlbumImage, PrivacyAndPolicy, TermsAndCondition, VoteScore, VideoMenu)
from account.models import User
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import AdsRelatedVideoSerializer, ContestImageUploadSerializer, ContestSerializer, ContestVideoUploadUrlSerializer, EventContestantFieldSerializer, EventSearchSerializers, UserVotingDetailSerializer, VideosForYouSerializer
from .models import AdsRelatedVideo, Contest, EventContestantField, VideosForYou

from rest_framework.views import APIView
from rest_framework import filters
from rest_framework import viewsets
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view, permission_classes, authentication_classes

from rest_framework.response import Response
from django.shortcuts import redirect
import uuid
import json
import requests
from .utils import ContestField
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ContestTermConditionsSerializer
from .models import ContestTermConditions


# Importing permissions to ensure only authenticated users can access this view
from rest_framework.permissions import IsAuthenticated
from .serializers import (ContestSerializer, ContestTermConditionsSerializer, SliderSerializers, AddSerializers, CategorySerializers,
                            EventSerializers, UserProfileSerializer, ImageSerializer,
                            VideoSerializer, GenreSerializers, GenreDetailSerializers,
                            ParticipatedEventListSerializers, EventVotingSettingsSerializer,
                            VideoCategorySerializer, KhaltiVerificationSerializer,
                            AlbumImageSerializer,AlbumDetailSerializer, AlbumSerializer,
                             EventListSerializers, PrivacyAndPolicySerializers,
                            TermsAndConditionSerializers, VideoMenuSerializers)



# Create your views here.


# Slider List 
class SliderListAPIView(generics.ListAPIView):
    serializer_class = SliderSerializers
    
    

    def get_queryset(self):
        return Slider.objects.all()

    def get(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.serializer_class(queryset, many=True)
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)
        
        except ValidationError as e:  # Import from rest_framework.exceptions
            return Response({'message': 'Validation error', 'errors': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({'message': 'Something went wrong!', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Add List 
class AddListAPIView(generics.ListAPIView):
    serializer_class = AddSerializers

    def get_queryset(self):
        return Add.objects.all()

    def get(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.serializer_class(queryset, many=True)
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)
        
        except ValidationError as e:  # Import from rest_framework.exceptions
            return Response({'message': 'Validation error', 'errors': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({'message': 'Something went wrong!', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Event List


# List all categories with related events
class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers
    permission_classes = [IsAuthenticated]  # Restrict access to authenticated users

# Retrieve a specific category with related events by its pk
class CategoryDetailAPIView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers
    lookup_field = 'pk'  # The field used to retrieve the category, defaults to 'pk'
    permission_classes = [IsAuthenticated]  # Restrict access to authenticated users


class CategoryEventDetailAPIView(generics.RetrieveAPIView):
    serializer_class = EventSerializers
    # filter_backends = (DjangoFilterBackend,)
    # filterset_fields = ('event_name')

    def get_object(self):
        category_id = self.kwargs['category_pk']
        event_id = self.kwargs['event_pk']
        category = get_object_or_404(Category, pk=category_id)
        return get_object_or_404(Event, pk=event_id, category=category)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.update_status()  # Update event status
        serializer = self.get_serializer(instance)
        return Response({
            "event": serializer.data,
            "success": True
        })


# List all genre with related events
class GenreListAPIView(generics.ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializers
    permission_classes = [IsAuthenticated]  # Restrict access to authenticated users

# Retrieve a specific category with related events by its pk
class GenreDetailAPIView(generics.RetrieveAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreDetailSerializers
    lookup_field = 'pk'  # The field used to retrieve the Genre, defaults to 'pk'
    permission_classes = [IsAuthenticated]  # Restrict access to authenticated users


class GenreEventDetailAPIView(generics.RetrieveAPIView):
    serializer_class = EventSerializers

    def get_object(self):
        genre_id = self.kwargs['genre_pk']
        event_id = self.kwargs['event_pk']
        genre = get_object_or_404(Genre, pk=genre_id)
        return get_object_or_404(Event, pk=event_id, genre=genre)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.update_status()  # Update event status
        serializer = self.get_serializer(instance)
        return Response({
            "event": serializer.data,
            "success": True
        })

 # Correct import for DjangoFilterBackend
from django_filters import rest_framework as filters

class EventListAPIView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializers
    
    
    

    def list(self, request, *args, **kwargs):
        if 'id' in kwargs:
            # Fetch a specific event by ID
            event = Event.objects.get(id=kwargs['id'])
            event.update_status()  # Update event statuses
            # Pass the request context to include is_applied status
            event_serializer = EventSerializers(event, context={'request': request})

            response_data = {
                "event": event_serializer.data,
                "success": True
            }
        else:
            # Fetch all events
            queryset = self.get_queryset()
            for event in queryset:
                event.update_status()  # Update event statuses

            # Pass the request context to include is_applied status for all events
            serializer = EventSerializers(queryset, many=True, context={'request': request})
            response_data = {
                "data": serializer.data,
                "success": True
            }

        return Response(response_data, status=status.HTTP_200_OK)

    def get_queryset(self):
        return Event.objects.all()

class EventParticipationAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, event_id):
        try:
            # Get the event
            event = Event.objects.get(id=event_id)
            now = timezone.now()

            # Check if participation is allowed
            if event.participate_start_time <= now <= event.participate_end_time:
                user = request.user
                
                # Check if user is authenticated
                if not user.is_authenticated:
                    return Response({'error': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

                # Add the user to participants
                event.participants.add(user)
                event.save()
                
                return Response({'message': 'User added to event'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Participation time has ended or not started yet'}, status=status.HTTP_400_BAD_REQUEST)

        except Event.DoesNotExist:
            return Response({'error': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)


## Event that fetch the list of event that the user has participated
class UserParticipatedEventsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ParticipatedEventListSerializers

    def get(self, request, *args, **kwargs):
        now = timezone.now()
        user = request.user

        # Query for upcoming events the user has participated in
        upcoming_events = Event.objects.filter(
            participants=user,
            participate_status=True,
            participate_end_time__gt=now
        )

        # Query for events whose participation time has timed out
        timed_out_events = Event.objects.filter(
            participants=user,
            participate_end_time__lt=now
        )

        # Serialize the data
        upcoming_serializer = self.get_serializer(upcoming_events, many=True, context={'request': request})
        timed_out_serializer = self.get_serializer(timed_out_events, many=True, context={'request': request})

        # Return the response with participant name, upcoming and timed-out events
        return Response({
            # 'participant': user.name,
            'upcoming_events': upcoming_serializer.data,
            'timed_out_events': timed_out_serializer.data,
        })


class UserProfileListCreateAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

class UserProfileDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save()

class ImageUploadAPIView(APIView):
    def post(self, request, format=None):
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_profile=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ImageDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save(user_profile=self.request.user)

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

class VideoCategoryAPIView(generics.ListAPIView):
    queryset = VideoCategory.objects.all()
    serializer_class = VideoCategorySerializer
    permission_classes = [IsAuthenticated]

class VideoUploadAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = VideoSerializer(data=request.data)
        if serializer.is_valid():
            # Get or create the user profile
            # user_profile, created = UserProfile.objects.get_or_create(user=request.user)
            
            # Save the video with the user profile
            serializer.save(user_profile=request.user)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VideoDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save(user_profile=self.request.user)

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
        

#### Views for video menu list
class VideoMenuListAPIView(generics.ListAPIView):
    serializer_class = VideoMenuSerializers  # Fix the typo here

    def get_queryset(self):
        return VideoMenu.objects.all()

    def get(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)  # Use self.get_serializer()
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)
        
        except ValidationError as e:  # Import from rest_framework.exceptions
            return Response({'message': 'Validation error', 'errors': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({'message': 'Something went wrong!', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


### Views for voting 
# class EventVotingSettingsListView(generics.ListCreateAPIView):
#     queryset = EventVotingSettings.objects.all()
#     serializer_class = EventVotingSettingsSerializer
#     permission_classes = [IsAuthenticated]
from .models import EventVotingSettings
from .serializers import EventVotingSettingsSerializer

class EventVotingSettingsListView(APIView):
    """
    View to list all Event Voting Settings and create a new one.
    Supports both GET and POST requests.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Handle GET request to retrieve all Event Voting Settings.
        """
        # Fetch all EventVotingSettings objects
        event_voting_settings = UserEventVoting.objects.all()

        # Serialize the data
        serializer = UserVotingDetailSerializer(event_voting_settings, many=True)

        # Return the serialized data as a response
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
        Handle POST request to create a new Event Voting Settings.
        """
        # Deserialize the incoming data
        serializer = UserVotingDetailSerializer(data=request.data)

        if serializer.is_valid():
            # Save the validated data to the database
            serializer.save()

            # Return a response with the created data
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # Return a response with errors if the data is invalid
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class EventVotingSettingsDetailView(generics.RetrieveUpdateDestroyAPIView):
#     # queryset = EventVotingSettings.objects.all()
#     serializer_class = EventVotingSettingsSerializer
#     # permission_classes = [IsAuthenticated]

#     def get_object(self):
#         # Get the event_id from the URL
#         event_id = self.kwargs['pk']
#         # Fetch the EventVotingSettings object using the event_id
#         return generics.get_object_or_404(EventVotingSettings, event_id=event_id)
        

        
class EventVotingSettingsDetailView(APIView):
    """
    Handle GET request for EventVotingSettings based on event_id.
    """
   
    # permission_classes = [IsAuthenticated]  # Uncomment if needed

    def get(self, request, event_id=None, *args, **kwargs):
        try:
            # Fetch the EventVotingSettings object for the given event_id
            voting_settings = EventVotingSettings.objects.get(event_id=event_id)

            # Serialize the voting settings object
            voting_settings_serializer = EventVotingSettingsSerializer(voting_settings)
            
           

            # Fetch and serialize approved contests
            contest_list = Contest.objects.filter(contest_status="approved")
            contest_serializer = ContestSerializer(contest_list, many=True)

            # Create a list of contestants with specific attributes
            approved_contests = [
                {
                    "contestant_id": contest["contestant_no"],
                    "contestant_first_name": contest["contestant_first_name"],
                    "contestant_last_name": contest["contestant_last_name"],
                    "contestant_photo": contest["contestant_photo"],

                    
                   
                }
                for contest in contest_serializer.data
            ]
           
            # Combine the results and return the response
            return Response(
                {
                    "voting_settings": voting_settings_serializer.data,
                    "approved_contests": approved_contests,
                    
                
                },
                status=status.HTTP_200_OK,
            )

        except EventVotingSettings.DoesNotExist:
            # Handle the case where the EventVotingSettings object does not exist
            return Response(
                {"error": f"EventVotingSettings with event_id {event_id} does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )

        except Exception as e:
            # Log the error for debugging
            return Response(
                {"error": "An unexpected error occurred.", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def put(self, request, pk, *args, **kwargs):
        """
        Update the EventVotingSettings object for the given event_id.
        """
        try:
            # Fetch the EventVotingSettings object
            voting_settings = EventVotingSettings.objects.get(event_id=pk)
            
            # Deserialize and validate the input data
            serializer = self.serializer_class(voting_settings, data=request.data, partial=True)
            if serializer.is_valid():
                # Save the updated object
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except EventVotingSettings.DoesNotExist:
            # Handle the case where the object does not exist
            return Response({"error": "EventVotingSettings not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # Handle unexpected errors and return an appropriate response
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk, *args, **kwargs):
        """
        Delete the EventVotingSettings object for the given event_id.
        """
        try:
            # Fetch the EventVotingSettings object
            voting_settings = EventVotingSettings.objects.get(event_id=pk)
            
            # Delete the object
            voting_settings.delete()
            return Response({"message": "EventVotingSettings deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        
        except EventVotingSettings.DoesNotExist:
            # Handle the case where the object does not exist
            return Response({"error": "EventVotingSettings not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # Handle unexpected errors and return an appropriate response
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





# Initialize Khalti Payment API View
# from django.http import JsonResponse

# @api_view(['POST'])
# def init_khalti_payment(request):
#     url = "https://a.khalti.com/api/v2/epayment/initiate/"
    
#     # Your Khalti secret key (consider storing this in environment variables)
#     headers = {
#         'Authorization': 'test_public_key_784023b3364e43b8a62c27d787a36e2b',
#         'Content-Type': 'application/json'
#     }
    
#     # Extract and validate required data
#     return_url = request.data.get('return_url')
#     website_url = request.data.get('website_url')
#     amount = request.data.get('amount')
#     purchase_order_id = request.data.get('purchase_order_id')
#     purchase_order_name = request.data.get('purchase_order_name')
#     customer_info = request.data.get('customer_info', {})
    
#     # Validate required fields
#     required_fields = [return_url, website_url, amount, purchase_order_id, purchase_order_name]
#     if not all(required_fields):
#         return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)
    
#     # Prepare the request data
#     data = {
#         "return_url": return_url,
#         "website_url": website_url,
#         "amount": amount,
#         "purchase_order_id": purchase_order_id,
#         "purchase_order_name": purchase_order_name,
#         "customer_info": {
#             "name": customer_info.get('name', ''),
#             "email": customer_info.get('email', ''),
#             "phone": customer_info.get('phone', '')
#         }
#     }
    
#     try:
#         # Make the request to Khalti
#         response = requests.post(url, headers=headers, json=data, timeout=30)
#         response.raise_for_status()  # Raises an HTTPError for bad responses
        
#         return Response(response.json(), status=status.HTTP_200_OK)
    
#     except requests.exceptions.Timeout:
#         return Response({'error': 'Request to Khalti API timed out'}, status=status.HTTP_504_GATEWAY_TIMEOUT)
#     except requests.exceptions.ConnectionError:
#         return Response({'error': 'Connection error occurred'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
#     except requests.exceptions.RequestException as e:
#         return Response({'error': f'Unable to initiate payment: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# # Verify Khalti Payment API View
# @api_view(['POST'])
# def verify_khalti_payment(request):
#     url = "https://a.khalti.com/api/v2/epayment/lookup/"
#     pidx = request.data.get('pidx')  # This is the transaction identifier returned by Khalti

#     if not pidx:
#         return Response({"error": "pidx is required"}, status=400)

#     headers = {
#         'Authorization': 'test_public_key_784023b3364e43b8a62c27d787a36e2b',  # Replace with your Khalti secret key
#         'Content-Type': 'application/json',
#     }
#     data = json.dumps({'pidx': pidx})

#     # Send request to Khalti to verify payment
#     response = requests.post(url, headers=headers, data=data)

#     if response.status_code == 200:
#         verification_response = response.json()
        
#         if verification_response['status'] == 'Completed':
#             # Payment is successful, perform your DB interactions here
#             # Save or update user or order status
#             return Response({"message": "Payment verified successfully", "data": verification_response})
#         else:
#             return Response({"message": "Payment verification failed", "data": verification_response})
#     else:
#         return Response({"error": "Unable to verify payment"}, status=response.status_code)

#### Khaltiiiiii
import logging
from django.conf import settings

logger = logging.getLogger(__name__)
class InitiateKhaltiPayment(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        url = "https://a.khalti.com/api/v2/epayment/initiate/"
        payload = {
            "return_url": request.data.get('return_url'),
            "website_url": request.data.get('website_url'),
            "amount": request.data.get('amount'),
            "purchase_order_id": request.data.get('purchase_order_id'),
            "purchase_order_name": "test",
            "customer_info": {
                "name": request.data.get('full_name'),
                "email": 'test@gmail.com',
                "phone": request.data.get('phone_number')
            }
        }

        headers = {
            'Authorization': f'key {settings.KHALTI_SECRET_KEY}',
            'Content-Type': 'application/json',
        }

        logger.info(f"Initiating Khalti payment with payload: {payload}")

        try:
            response = requests.post(url, headers=headers, json=payload)
            response_data = response.json()

            logger.info(f"Khalti API response: {response_data}")

            if response.status_code == 200 and 'payment_url' in response_data:
                return Response({'redirect_url': response_data['payment_url']}, status=status.HTTP_200_OK)
            else:
                error_message = response_data.get('detail', 'Unknown error occurred')
                logger.error(f"Khalti API error: {error_message}")
                return Response({'error': error_message}, status=response.status_code)

        except requests.RequestException as e:
            logger.error(f"Request to Khalti API failed: {str(e)}")
            return Response({'error': 'Failed to connect to payment service'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except json.JSONDecodeError:
            logger.error("Failed to decode JSON response from Khalti API")
            return Response({'error': 'Invalid response from payment service'}, status=status.HTTP_502_BAD_GATEWAY)
        except Exception as e:
            logger.error(f"Unexpected error in InitiateKhaltiPayment: {str(e)}")
            return Response({'error': 'An unexpected error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class VerifyKhalti(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,*args,**kwargs):
        url = "https://a.khalti.com/api/v2/epayment/lookup/"
        if request.method == 'GET':
            headers = {
                'Authorization': 'key 63645526dd524fdb9b8742e886c1c81e',
                'Content-Type': 'application/json',
            }
            pidx = request.GET.get('pidx')
            cat_id = kwargs.get('cat_id')
            print("cat__id=====",cat_id)
            data = json.dumps({
                'pidx':pidx
            })
            res = requests.request('POST',url,headers=headers,data=data)
            print(res)
            print(res.text)

            new_res = json.loads(res.text)
            print(new_res)

            if new_res['status'] == 'Completed':
                try:
                    
                    category = Category.objects.get(id=cat_id)

                    user = User.objects.get(id=kwargs.get('userid'))
                    print("category===",category)
                    Upgrade.objects.create(user=user,category=category,payment_status=new_res['status'])
                except Exception as e:
                    print("exception===",e)
                    return Response({'data':{'message':'Url modified. Couldnot upgrade user. Please contact administration.'}},status=status.HTTP_400_BAD_REQUEST)
            
            elif new_res['status'] == 'Pending':
                try:
                    category = Category.objects.get(id=cat_id)
                    Upgrade.objects.create(user=self.request.user,category=category,payment_status=new_res['status'])
                except Exception as e:
                    return Response({'data':{'message':'Url modified'}},status=status.HTTP_400_BAD_REQUEST)
            elif new_res['status'] == 'Expired':
                return Response({'data':{'message':'Pidx expired'}},status=status.HTTP_400_BAD_REQUEST)
            elif new_res['status'] == 'Initiated':
                
                return Response({'data':{'message':'Payment didnot succed.Please contace support center.'}},status=status.HTTP_400_BAD_REQUEST)
            elif new_res['status'] == 'Refunded':
                
                return Response({'data':{'message':'Payment refunded.'}},status=status.HTTP_400_BAD_REQUEST)
            elif new_res['status'] == 'User canceled':
                
                return Response({'data':{'message':'User cancelled payment request'}},status=status.HTTP_400_BAD_REQUEST)
            elif new_res['status'] == 'Partially Refunded':
                
                return Response({'data':{'message':'Payment partially refunded'}},status=status.HTTP_400_BAD_REQUEST)
            else:
                
                return Response({'data':{'message':'Payment didnot succed.Please contace support center.'}},status=status.HTTP_400_BAD_REQUEST)

            return redirect(os.environ.get('FRONTEND_BASE_URL'))


# from django.conf import settings
# class KhaltiPaymentVerify(APIView):
#     def post(self, request):
#         serializer = KhaltiVerificationSerializer(data=request.data)
#         if not serializer.is_valid():
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
#         token = serializer.validated_data['token']
#         amount = serializer.validated_data['amount']

#         payload = {
#             'token': token,
#             'amount': amount
#         }

#         headers = {
#             'Authorization': f'Key {settings.KHALTI_SECRET_KEY}'
#         }

#         response = requests.post(settings.KHALTI_VERIFY_URL, payload, headers=headers)
        
#         if response.status_code == 200:
#             return Response({
#                 'success': True,
#                 'message': 'Payment verified successfully',
#                 'data': response.json()
#             })
#         else:
#             return Response({
#                 'success': False,
#                 'message': 'Payment verification failed',
#                 'details': response.json()
#             }, status=status.HTTP_400_BAD_REQUEST)



class AlbumListCreateView(generics.ListCreateAPIView):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer  # Only album fields for list and create

class AlbumRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Album.objects.all()

    def get_serializer_class(self):
        # Use AlbumDetailSerializer to show images for the detailed view
        if self.request.method == 'GET':
            return AlbumDetailSerializer
        return AlbumSerializer

class AlbumImagesView(generics.ListAPIView):
    # serializer_class = AlbumImageSerializer

    # def get_queryset(self):
    #     # Filter AlbumImage objects based on the album's primary key
    #     album_id = self.kwargs['pk']
    #     return AlbumImage.objects.filter(album__id=album_id)
    serializer_class = AlbumImageSerializer

    def get_queryset(self):
        # Handle the case where `swagger_fake_view` is True (during schema generation)
        if getattr(self, 'swagger_fake_view', False):
            return AlbumImage.objects.none()

        # Filter AlbumImage objects based on the album's primary key
        album_id = self.kwargs.get('pk')  # Use `.get()` to avoid KeyError
        if album_id is None:
            raise ValueError("Album ID (pk) is required.")
        return AlbumImage.objects.filter(album__id=album_id)


## Priavacy and policy
class PrivacyAndPolicyListAPIView(generics.ListAPIView):
    serializer_class = PrivacyAndPolicySerializers

    def get_queryset(self):
        return PrivacyAndPolicy.objects.all()

    def get(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.serializer_class(queryset, many=True)
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)
        
        except ValidationError as e:  # Import from rest_framework.exceptions
            return Response({'message': 'Validation error', 'errors': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({'message': 'Something went wrong!', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


### Terms and condition
class TermsAndConditionListAPIView(generics.ListAPIView):
    serializer_class = TermsAndConditionSerializers

    def get_queryset(self):
        return TermsAndCondition.objects.all()

    def get(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.serializer_class(queryset, many=True)
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)
        
        except ValidationError as e:  # Import from rest_framework.exceptions
            return Response({'message': 'Validation error', 'errors': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({'message': 'Something went wrong!', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


### Vote count

# class VoteCounttCreateView(APIView):
#     def post(self, request, *args, **kwargs):
#         serializer = VoteCounttSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'message': 'Voting count saved successfully!'}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from decimal import Decimal
from django.db import transaction

# @api_view(['POST'])
# def create_vote_score(request):
#     # Retrieve data from request
#     event_id = request.data.get('event_id')
#     voting_id = request.data.get('voting_id')
#     vote_count = request.data.get('vote_count')
#     amount = request.data.get('amount')

#     # Check if all required fields are provided
#     missing_fields = []
#     if not event_id:
#         missing_fields.append('event_id')
#     if not voting_id:
#         missing_fields.append('voting_id')
#     if not vote_count:
#         missing_fields.append('vote_count')
#     if not amount:
#         missing_fields.append('amount')

#     if missing_fields:
#         return Response({'error': f'Missing required field(s): {", ".join(missing_fields)}'}, status=status.HTTP_400_BAD_REQUEST)

#     try:
#         # Get the event based on event_id
#         event = Event.objects.get(id=event_id)
#     except Event.DoesNotExist:
#         return Response({'error': 'Invalid event_id'}, status=status.HTTP_400_BAD_REQUEST)

#     # Check if the event has voting settings
#     try:
#         voting_settings = event.voting_settings
#     except EventVotingSettings.DoesNotExist:
#         return Response({'error': 'This event does not have voting settings configured'}, status=status.HTTP_400_BAD_REQUEST)

#     try:
#         # Retrieve the voting for the user
#         user_event_voting = UserEventVoting.objects.select_related('user').get(event_id=event_id, voting_id=voting_id)
#     except UserEventVoting.DoesNotExist:
#         return Response({'error': 'No vote found for the associated user and event'}, status=status.HTTP_400_BAD_REQUEST)

#     try:
#         expected_amount = Decimal(vote_count) * voting_settings.price_per_vote

#         if amount != expected_amount:
#             return Response({
#                 'error': f'Invalid amount. Expected {expected_amount} based on vote count {vote_count} and price per vote {voting_settings.price_per_vote}'
#             }, status=status.HTTP_400_BAD_REQUEST)

#         # Validate vote count against EventVotingSettings
#         if vote_count < voting_settings.min_vote or vote_count > voting_settings.max_vote:
#             return Response({
#                 'error': f'Vote count must be between {voting_settings.min_vote} and {voting_settings.max_vote}.'
#             }, status=status.HTTP_400_BAD_REQUEST)

#         # Use a transaction to ensure atomic updates
#         with transaction.atomic():
#             vote_score, created = VoteScore.objects.get_or_create(
#                 event=event,
#                 user_event_voting=user_event_voting,
#                 defaults={'vote_count': 0, 'amount': Decimal('0.00')}
#             )
            
#             vote_score.vote_count += vote_count
#             vote_score.amount += amount
#             vote_score.save()

#         # Prepare the response with user details
#         response_data = {
#             'message': 'Vote score updated successfully',
#             'vote_score_id': vote_score.id,
#             'event_id': event.id,
#             'event_name': event.event_name,
#             'voting_id': voting_id,
#             'total_vote_count': vote_score.vote_count,
#             'total_amount': vote_score.amount,
#             'user': {
#                 'id': user_event_voting.user.id,
#                 'name': user_event_voting.user.name,
#                 'avatar': user_event_voting.user.avatar.url if user_event_voting.user.avatar else None
#             }
#         }

#         return Response(response_data, status=status.HTTP_200_OK)

#     except ValidationError as e:
#         return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


# @permission_classes([IsAuthenticated])
# @api_view(['POST'])
# @transaction.atomic
# def create_vote_score(request):
#     event_id = request.data.get('event_id')
#     voting_id = request.data.get('voting_id')  # This represents the user being voted for.
#     vote_count = request.data.get('vote_count')
#     amount = request.data.get('amount')

#     # Debugging: Print received data
#     print(f"Received data: event_id={event_id}, voting_id={voting_id}, vote_count={vote_count}, amount={amount}")

#     # Check for missing fields
#     required_fields = ['event_id', 'voting_id', 'vote_count', 'amount']
#     missing_fields = [field for field in required_fields if not request.data.get(field)]
#     if missing_fields:
#         return Response({'error': f'Missing required field(s): {", ".join(missing_fields)}'}, status=status.HTTP_400_BAD_REQUEST)

#     try:
#         event = Event.objects.get(id=event_id)
#         voting_settings = event.voting_settings
#         print(f"Event voting settings: min_vote={voting_settings.min_vote}, max_vote={voting_settings.max_vote}, price_per_vote={voting_settings.price_per_vote}")
#     except Event.DoesNotExist:
#         return Response({'error': 'Invalid event_id'}, status=status.HTTP_400_BAD_REQUEST)
#     except EventVotingSettings.DoesNotExist:
#         return Response({'error': 'This event does not have voting settings configured'}, status=status.HTTP_400_BAD_REQUEST)

#     try:
#         user_event_voting = UserEventVoting.objects.select_related('user').get(event_id=event_id, voting_id=voting_id)
#     except UserEventVoting.DoesNotExist:
#         return Response({'error': 'No vote found for the associated user and event'}, status=status.HTTP_400_BAD_REQUEST)

#     try:
#         vote_count = int(vote_count)
#         amount = Decimal(amount)

#         # Debugging: Print converted values
#         print(f"Converted values: vote_count={vote_count}, amount={amount}")

#         expected_amount = Decimal(vote_count) * voting_settings.price_per_vote
#         if abs(amount - expected_amount) > Decimal('0.01'):
#             return Response({
#                 'error': f'Invalid amount. Expected {expected_amount} based on vote count {vote_count} and price per vote {voting_settings.price_per_vote}'
#             }, status=status.HTTP_400_BAD_REQUEST)

#         # Ensure vote_count is within allowed range
#         if vote_count < voting_settings.min_vote or vote_count > voting_settings.max_vote:
#             return Response({
#                 'error': f'Vote count must be between {voting_settings.min_vote} and {voting_settings.max_vote}.'
#             }, status=status.HTTP_400_BAD_REQUEST)

#         # Fetch existing vote score for this user and event
#         vote_score, created = VoteScore.objects.get_or_create(
#             event=event,
#             user_event_voting=user_event_voting,
#             defaults={'vote_count': 0, 'amount': Decimal('0.00')}
#         )

#         # Check if the new votes would exceed the maximum allowed votes per user
#         if vote_score.vote_count + vote_count > voting_settings.max_vote:
#             return Response({
#                 'error': f'You can only vote up to {voting_settings.max_vote} for this user. '
#                             f'Current vote count: {vote_score.vote_count}, Additional votes: {vote_count}'
#             }, status=status.HTTP_400_BAD_REQUEST)

#         # Update the vote count and amount
#         vote_score.vote_count += vote_count
#         vote_score.amount += amount

#         # Debugging: Print values before saving
#         print(f"Before saving: vote_count={vote_score.vote_count}, amount={vote_score.amount}")

#         try:
#             vote_score.full_clean()
#             vote_score.save()
#         except ValidationError as ve:
#             print(f"Validation error: {ve}")
#             return Response({'error': str(ve)}, status=status.HTTP_400_BAD_REQUEST)

#         response_data = {
#             'message': 'Vote score updated successfully',
#             # Include more details if necessary
#         }

#         return Response(response_data, status=status.HTTP_200_OK)

#     except Exception as e:
#         print(f"Unexpected error: {str(e)}")
#         return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)



# @permission_classes([IsAuthenticated])
# @api_view(['POST'])
# def create_vote_score(request):
#     event_id = request.data.get('event_id')
#     voting_id = request.data.get('voting_id')
#     vote_count = int(request.data.get('vote_count'))
#     amount = Decimal(request.data.get('amount'))

#     try:
#         event = Event.objects.get(id=event_id)
#     except Event.DoesNotExist:
#         return Response({'error': 'Invalid event_id'}, status=status.HTTP_400_BAD_REQUEST)

#     try:
#         user_event_voting = UserEventVoting.objects.select_related('user').get(event_id=event_id, voting_id=voting_id)
#     except UserEventVoting.DoesNotExist:
#         return Response({'error': 'No vote found for the associated user and event'}, status=status.HTTP_400_BAD_REQUEST)

#     try:
#         voting_settings = event.voting_settings
#         expected_amount = Decimal(vote_count) * voting_settings.price_per_vote

#         if amount != expected_amount:
#             return Response({
#                 'error': f'Invalid amount. Expected {expected_amount} based on vote count {vote_count} and price per vote {voting_settings.price_per_vote}'
#             }, status=status.HTTP_400_BAD_REQUEST)

#         with transaction.atomic():
#             vote_score, created = VoteScore.objects.get_or_create(
#                 event=event,
#                 user_event_voting=user_event_voting,
#                 defaults={'vote_count': 0, 'amount': Decimal('0.00')}
#             )
            
#             vote_score.vote_count += vote_count
#             vote_score.amount += amount
#             vote_score.save()

#         # Prepare the response with user details
#         response_data = {
#             'message': 'Vote score updated successfully',
#             # 'vote_score_id': vote_score.id,
#             # 'event_id': event.id,
#             # 'event_name': event.event_name,
#             # 'voting_id': voting_id,
#             # 'total_vote_count': vote_score.vote_count,
#             # 'total_amount': vote_score.amount,
#             # 'user': {
#             #     'id': user_event_voting.user.id,
#             #     'name': user_event_voting.user.name,
#             #     'avatar': user_event_voting.user.avatar.url if user_event_voting.user.avatar else None
#             # }
#         }

#         return Response(response_data, status=status.HTTP_200_OK)
#     except ValidationError as e:
#         return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@permission_classes([IsAuthenticated])
@api_view(['POST'])
def create_vote_score(request):
    user = request.user
    event_id = request.data.get('event_id')
    voting_id = request.data.get('voting_id')
    vote_count = int(request.data.get('vote_count'))
    amount = Decimal(request.data.get('amount'))

    try:
        # Check if the event exists
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        return Response({'error': 'Invalid event_id'}, status=status.HTTP_400_BAD_REQUEST)

    # Check if the user has participated in the event and can vote
    # try:
    #     user_event_voting = UserEventVoting.objects.get(user=user, event=event)
    # except UserEventVoting.DoesNotExist:
    #     return Response({'error': 'User has not participated in this event'}, status=status.HTTP_403_FORBIDDEN)

    # Check if the voting target exists for this event
    try:
        voting_target = UserEventVoting.objects.get(event=event, voting_id=voting_id)
    except UserEventVoting.DoesNotExist:
        return Response({'error': 'Invalid voting_id'}, status=status.HTTP_400_BAD_REQUEST)

    # Check if the authenticated user has already voted for this voting_id in this event
    # user_event_voting = UserEventVoting.objects.get(user=user, event=event)
    # try:
    #     existing_vote = VoteScore.objects.get(
    #         event=event,
    #         user_event_voting=user_event_voting,  # The voting by the authenticated user
    #         user_event_voting__voting_id=voting_id  # Ensure it's for the same voting_id
    #     )
    #     return Response({
    #         'error': 'You have already voted for this user in this event and cannot vote again.'
    #     }, status=status.HTTP_400_BAD_REQUEST)
    # except VoteScore.DoesNotExist:
    #     pass  # No existing vote, so allow the user to vote

    try:
        # Retrieve the voting settings to enforce the max_vote rule
        voting_settings = event.voting_settings
        expected_amount = Decimal(vote_count) * voting_settings.price_per_vote

        if amount != expected_amount:
            return Response({
                'error': f'Invalid amount. Expected {expected_amount} based on vote count {vote_count} and price per vote {voting_settings.price_per_vote}'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve or create the VoteScore for this user and voting target
        with transaction.atomic():
            vote_score, created = VoteScore.objects.get_or_create(
                event=event,
                user_event_voting=voting_target,
                defaults={'vote_count': 0, 'amount': Decimal('0.00')}
            )

            # Check if the user is exceeding the max_vote limit
            if  vote_count > voting_settings.max_vote:
                return Response({
                    'error': f'Cannot give more than {voting_settings.max_vote} votes to this user.'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Update vote count and amount
            vote_score.vote_count += vote_count
            vote_score.amount += amount
            vote_score.save()

        # Prepare the response
        response_data = {
            'message': 'Vote score updated successfully',
            'event_name': event.event_name,
            'voting_id': voting_id,
        }

        return Response(response_data, status=status.HTTP_200_OK)
    
    except ValidationError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


# @permission_classes([IsAuthenticated])  # Ensure only authenticated users can vote
# @api_view(['POST'])
# def create_vote_score(request):
#     user = request.user  # The authenticated user
#     event_id = request.data.get('event_id')
#     voting_id = request.data.get('voting_id')
#     vote_count = int(request.data.get('vote_count'))
#     amount = Decimal(request.data.get('amount'))

#     try:
#         # Check if the event exists
#         event = Event.objects.get(id=event_id)
#     except Event.DoesNotExist:
#         return Response({'error': 'Invalid event_id'}, status=status.HTTP_400_BAD_REQUEST)

#     # Check if the authenticated user has participated in the event
#     try:
#         user_event_voting = UserEventVoting.objects.get(user=user, event=event)
#     except UserEventVoting.DoesNotExist:
#         return Response({'error': 'User has not participated in this event'}, status=status.HTTP_403_FORBIDDEN)

#     # # Check if the authenticated user has already voted for this voting_id in this event
#     # try:
#     #     existing_vote = VoteScore.objects.get(
#     #         event=event,
#     #         user_event_voting=user_event_voting,  # Use the user_event_voting object defined above
#     #         user_event_voting__voting_id=voting_id  # Ensure it's for the same voting_id
#     #     )
#     #     return Response({
#     #         'error': 'You have already voted for this user in this event and cannot vote again.'
#     #     }, status=status.HTTP_400_BAD_REQUEST)
#     # except VoteScore.DoesNotExist:
#     #     pass  # No existing vote, so allow the user to vote

#     # Ensure the vote count doesn't exceed the max_vote limit
#     voting_settings = event.voting_settings
#     if vote_count > voting_settings.max_vote:
#         return Response({
#             'error': f'Cannot give more than {voting_settings.max_vote} votes to this user.'
#         }, status=status.HTTP_400_BAD_REQUEST)

#     # Ensure the correct amount is being sent based on the vote_count
#     expected_amount = Decimal(vote_count) * voting_settings.price_per_vote
#     if amount != expected_amount:
#         return Response({
#             'error': f'Invalid amount. Expected {expected_amount} based on vote count {vote_count} and price per vote {voting_settings.price_per_vote}'
#         }, status=status.HTTP_400_BAD_REQUEST)

#     # Create the vote score since the user hasn't voted for this voting_id yet
#     try:
#         with transaction.atomic():
#             vote_score = VoteScore.objects.create(
#                 event=event,
#                 user_event_voting=user_event_voting,  # Link the vote to the authenticated user
#                 vote_count=vote_count,
#                 amount=amount
#             )

#         # Prepare the response
#         response_data = {
#             'message': 'Vote score created successfully',
#             'vote_score_id': vote_score.id,
#             'event_id': event.id,
#             'voting_id': voting_id,
#             'total_vote_count': vote_score.vote_count,
#             'total_amount': vote_score.amount,
#         }
#         return Response(response_data, status=status.HTTP_200_OK)

#     except Exception as e:
#         return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


from django.db.models import Count
from .models import Contest

from django.db.models import Sum

class ContestTermConditionsView(APIView):
    """
    Handles CRUD operations for ContestTermConditions.
    """
    # permission_classes=[IsAuthenticated]

    def get(self, request, pk=None, *args, **kwargs):
        """
        Retrieve a single ContestTermConditions or all if no ID is provided.
        """
        if pk:
            try:
                obj = ContestTermConditions.objects.get(id=pk)
                serializer = ContestTermConditionsSerializer(obj)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ContestTermConditions.DoesNotExist:
                return Response({"error": "ContestTermConditions not found"}, status=status.HTTP_404_NOT_FOUND)
        obj_list = ContestTermConditions.objects.all()
        serializer = ContestTermConditionsSerializer(obj_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
        Create a new ContestTermConditions object.
        """
        serializer = ContestTermConditionsSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"success": "ContestTermConditions created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, *args, **kwargs):
        """
        Fully update a ContestTermConditions object.
        """
        try:
            obj = ContestTermConditions.objects.get(id=pk)
            serializer = ContestTermConditionsSerializer(obj, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({"success": "ContestTermConditions updated successfully"}, status=status.HTTP_200_OK)
        except ContestTermConditions.DoesNotExist:
            return Response({"error": "ContestTermConditions not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, *args, **kwargs):
        """
        Partially update a ContestTermConditions object.
        """
        try:
            obj = ContestTermConditions.objects.get(id=pk)
            serializer = ContestTermConditionsSerializer(obj, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({"success": "ContestTermConditions updated successfully"}, status=status.HTTP_200_OK)
        except ContestTermConditions.DoesNotExist:
            return Response({"error": "ContestTermConditions not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        """
        Delete a ContestTermConditions object.
        """
        try:
            obj = ContestTermConditions.objects.get(id=pk)
            obj.delete()
            return Response({"success": "ContestTermConditions deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except ContestTermConditions.DoesNotExist:
            return Response({"error": "ContestTermConditions not found"}, status=status.HTTP_404_NOT_FOUND)


from .models import ContestPhoto , ContestVideo

class ContestDetailView(APIView):
    """
    Handles CRUD operations for ContestDetail.
    """
    def get(self, request, event_id, format=None):
        """
        Retrieve event contestant fields and contest terms & conditions for a specific event.
        """
        # Get all contest term conditions
        obj_list = ContestTermConditions.objects.all()
        serializer = ContestTermConditionsSerializer(obj_list, many=True)

        # Get event contestant fields filtered by event_id and status
        event_contestant_field = EventContestantField.objects.filter(status=False, event=event_id)
        event_contestant_serializer = EventContestantFieldSerializer(event_contestant_field, many=True)

        # Extract only the 'field_name' and 'data_type'
        filtered_event_contestant_fields = {
            item["field_name"]: item["data_type"]
            for item in event_contestant_serializer.data
        }

        # Combine the data into a response dictionary
        response_data = {
            "event_contestant_fields": filtered_event_contestant_fields,
            "contest_term_conditions": serializer.data,
        }

        return Response(response_data, status=status.HTTP_200_OK)


class ContestView(APIView):
    permission_classes=[IsAuthenticated]
    """
    Handles CRUD operations for Contest.
    
    """
    # permission_classes=[IsAuthenticated]
    def get(self, request, pk=None, *args, **kwargs):
        """
        Retrieve a single Contest or all if no ID is provided.
        """
        if pk:
            try:
                obj = Contest.objects.get(id=pk)
                serializer = ContestSerializer(obj)

                # Sum of 'like' for the Contest
                contest_like_sum = ContestantLike.objects.filter(contest=pk).aggregate(total_likes=Sum('like'))

                # Sum of 'follow' for the Contest
                contest_follow_sum = ContestantFollow.objects.filter(contest=pk).aggregate(total_follows=Sum('follow'))

                # Get contest images
                contest_images = ContestPhoto.objects.filter(contest_id=pk)
                contest_images_serializer = ContestImageUploadSerializer(contest_images, many=True)

                # Get contest videos
                contest_videos = ContestVideo.objects.filter(contest_id=pk)
                contest_videos_serializer = ContestVideoUploadUrlSerializer(contest_videos, many=True)

                # Prepare response data
                like_follow = {
                    'likes': contest_like_sum['total_likes'] or 0,
                    'follows': contest_follow_sum['total_follows'] or 0
                }
                videosUrl_images = {
                    'contest_images': contest_images_serializer.data,
                    'contest_videos': contest_videos_serializer.data
                }

                return Response({
                    "contest": serializer.data,
                    "stats": like_follow,
                    "media": videosUrl_images
                }, status=status.HTTP_200_OK)

            except Contest.DoesNotExist:
                return Response({"error": "Contest not found"}, status=status.HTTP_404_NOT_FOUND)
        
        obj_list = Contest.objects.all()
        serializer = ContestSerializer(obj_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
        
        
       
        
        
    def post(self, request, *args, **kwargs):
        """
        Create a new Contest object.
        """
        serializer = ContestSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response({"success": "Contest created successfully", "contest_id": serializer.data['id']}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, *args, **kwargs):
        """
        Fully update a Contest object.
        """
        try:
            obj = Contest.objects.get(id=pk)
            serializer = ContestSerializer(obj, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(user=request.user)
                return Response({"success": "Contest updated successfully"}, status=status.HTTP_200_OK)
        except Contest.DoesNotExist:
            return Response({"error": "Contest not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, *args, **kwargs):
        """
        Partially update a Contest object.
        """
        try:
            obj = Contest.objects.get(id=pk)
            serializer = ContestSerializer(obj, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save(user=request.user)
                return Response({"success": "Contest updated successfully"}, status=status.HTTP_200_OK)
        except Contest.DoesNotExist:
            return Response({"error": "Contest not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class ContestantViewOwnContest(APIView):
    
    permission_classes= [IsAuthenticated]
    def get(self, request, format=None):
        user = request.user
        
        # Retrieve contests related to the logged-in user
        contests = Contest.objects.filter(user_id=user.id)

        # Check if contests exist
        if contests.exists():
            serializer = ContestSerializer(contests, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response([],status=status.HTTP_200_OK)



from .models import ContestantLike, ContestantFollow
from .serializers import ContestantLikeSerializer, ContestantFollowSerializer

class ContestantLikeAPIView(APIView):
    def get(self, request, *args, **kwargs):
        likes = ContestantLike.objects.all()
        serializer = ContestantLikeSerializer(likes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
        Create a like for a contest, ensuring the user can only like a contest once.
        """
        # First, check if this user already liked this contest
        user = request.data.get('user')
        
        
        if ContestantLike.objects.filter(user=user).exists():
            return Response(
                {"error": "You have already liked this contest."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # If not, proceed to save the like
        serializer = ContestantLikeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ContestantFollowAPIView(APIView):
    def get(self, request, *args, **kwargs):
        follows = ContestantFollow.objects.all()
        serializer = ContestantFollowSerializer(follows, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
        Create a like for a contest, ensuring the user can only like a contest once.
        """
        # First, check if this user already liked this contest
        user = request.data.get('user')
        
        
        if ContestantFollow.objects.filter(user=user).exists():
            return Response(
                {"error": "You have already liked this contest."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # If not, proceed to save the like
        serializer = ContestantFollowSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
from .models import Contest
from .serializers import ContestPhotoUploadSerializer, ContestVideoUrlUploadSerializer

class ContestBulkPhotoUploadView(APIView):
    def post(self, request, contest_id):
        try:
            contest = Contest.objects.get(id=contest_id)
        except Contest.DoesNotExist:
            return Response({"error": "Contest not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ContestPhotoUploadSerializer(data=request.data, context={'contest': contest})
        if serializer.is_valid():
            photos = serializer.save()
            return Response(
                {"photos": [photo.photo.url for photo in photos]}, 
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContestBulkVideoUploadView(APIView):
    def post(self, request, contest_id):
        # Try to get the contest object based on the provided contest_id
        try:
            contest = Contest.objects.get(id=contest_id)
        except Contest.DoesNotExist:
            raise ValidationError("Contest not found")

        # Get the list of video data from the request
        video_data = request.data.get('videos', [])
        
        if not video_data:
            return Response({"error": "No video data provided"}, status=status.HTTP_400_BAD_REQUEST)

        # Initialize a list to hold the serialized video objects
        serializer_list = []

        # Loop through each video data and serialize
        for video in video_data:
            # Add the contest ID to the video data to associate it with the contest
            video['contest'] = contest.id

            serializer = ContestVideoUrlUploadSerializer(data=video)
            if serializer.is_valid():
                # Save the video to the database
                serializer.save()
                serializer_list.append(serializer.data)
            else:
                return Response({"error": "Invalid video data", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        # Return the list of serialized videos that were saved
        return Response({"message": "Videos created successfully", "videos": serializer_list}, status=status.HTTP_201_CREATED)
    
    
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import EventContestantField
from .serializers import EventContestantFieldSerializer

class EventContestantFieldView(APIView):
    """
    API view to handle EventContestantField objects.
    Supports retrieving all or a specific EventContestantField, creating and updating EventContestantField.
    """
    
    def get(self, request, pk=None, format=None):
        """
        Retrieve a specific EventContestantField by ID, or all if no ID is provided.
        If no ID is provided, returns a list of all EventContestantField instances.
        """
        if pk:
            # If pk is provided, retrieve the specific EventContestantField
            try:
                event_contestant_field = EventContestantField.objects.get(id=pk)
                serializer = EventContestantFieldSerializer(event_contestant_field)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except EventContestantField.DoesNotExist:
                return Response({"detail": "EventContestantField not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            # If no pk is provided, retrieve all EventContestantField instances
            event_contestant_fields = EventContestantField.objects.all()
            serializer = EventContestantFieldSerializer(event_contestant_fields, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        """
        Create a new EventContestantField.
        If the input data is valid, a new EventContestantField is created.
        """
        serializer = EventContestantFieldSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk, format=None):
        """
        Update an existing EventContestantField.
        The EventContestantField with the given pk is updated with the provided data.
        """
        try:
            # Retrieve the EventContestantField object to update
            event_contestant_field = EventContestantField.objects.get(id=pk)
            serializer = EventContestantFieldSerializer(event_contestant_field, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except EventContestantField.DoesNotExist:
            return Response({"detail": "EventContestantField not found."}, status=status.HTTP_404_NOT_FOUND)



class AdsRelatedVideoAPIView(APIView):
    """
    Handles fetching all videos or a single video based on the ID provided.
    """

    def get(self, request, pk=None):
        """
        GET all videos if no ID is provided; otherwise, get a single video by ID.
        """
        if pk:
            # Fetch a single video by ID
            try:
                video = AdsRelatedVideo.objects.get(pk=pk)
                serializer = AdsRelatedVideoSerializer(video)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except AdsRelatedVideo.DoesNotExist:
                return Response({"error": "Video not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            # Fetch all videos
            videos = AdsRelatedVideo.objects.all()
            serializer = AdsRelatedVideoSerializer(videos, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
class VideosForYouAPIView(APIView):
    """
    Handles fetching all videos or a single video based on the ID provided.
    """

    def get(self, request, pk=None):
        """
        GET all videos if no ID is provided; otherwise, get a single video by ID.
        """
        if pk:
            # Fetch a single video by ID
            try:
                video = VideosForYou.objects.get(pk=pk)
                serializer = VideosForYouSerializer(video)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except VideosForYou.DoesNotExist:
                return Response({"error": "Video not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            # Fetch all videos
            videos = VideosForYou.objects.all()
            serializer = VideosForYouSerializer(videos, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        
        



class EventSearch(APIView):
    def get(self, request, event_name=None):
        try:
            if event_name:
                # Filter events based on event_name
                queryset = Event.objects.filter(event_name__icontains=event_name)
            else:
                # Return all events if no event_name is provided
                queryset = Event.objects.all()

            # Pass the request context to the serializer
            serializer = EventSearchSerializers(queryset, many=True, context={'request': request})
            filtered_data = [{'event_name': item['event_name'], 'category': item['category'],'image':item['image'], 'another_image':item['another_image'],'event_date':item[ 'event_date']} for item in serializer.data]

            return Response({'data': filtered_data, 'success': True}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
