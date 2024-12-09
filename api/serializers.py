from rest_framework import serializers
from account.serializers import UserSerializer
from django.contrib.auth import get_user_model
from . models import (AdsRelatedVideo, ContestTermConditions, EventContestantField, Slider, Add, Category, Event,  Image, VideoCategory, Video, Genre,
                        UserEventVoting, EventVotingSettings, Album, AlbumImage, VideoMenu,
                        PrivacyAndPolicy, TermsAndCondition, VideosForYou)

# Slider Serializer Class
class SliderSerializers(serializers.ModelSerializer):
    image = serializers.SerializerMethodField('get_image_url')

    class Meta:
        model = Slider
        fields =['image']
        

    # def get_image_url(self, obj):
    #     return f'{domain}{obj.image.url}'

    def get_image_url(self, obj):
        request = self.context.get('request')  # Get request from context
        if request is not None:
            return request.build_absolute_uri(obj.image.url)  # Build full URL
        return obj.image.url  # Fallback to relative URL if no request


# Ads Serializer Class
class AddSerializers(serializers.ModelSerializer):
    image = serializers.SerializerMethodField('get_image_url')

    class Meta:
        model = Add
        fields =['image']

    # def get_image_url(self, obj):
    #     return f'{domain}{obj.image.url}'

    def get_image_url(self, obj):
        request = self.context.get('request')  # Get request from context
        if request is not None:
            return request.build_absolute_uri(obj.image.url)  # Build full URL
        return obj.image.url  # Fallback to relative URL if no request


# Category Serializer class 
class CategorySerializers(serializers.ModelSerializer):
    # Nested event serializer to display related events under each category
    events = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'category', 'events']  # Include 'events' field

    def get_events(self, obj):
        events = obj.event_category.all()  # Use related_name to access related events
        return EventListSerializers(events, many=True, context=self.context).data  # Serialize events

# Genre Serializer class 
class GenreSerializers(serializers.ModelSerializer):
    # Nested event serializer to display related events under each category
    # events = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField('get_image_url')
    class Meta:
        model = Genre
        fields = ['id', 'genre', 'image']  # Include 'events' field

    def get_image_url(self, obj):
        request = self.context.get('request')  # Get request from context
        if request is not None:
            return request.build_absolute_uri(obj.image.url)  # Build full URL
        return obj.image.url  # Fallback to relative URL if no request

class GenreDetailSerializers(serializers.ModelSerializer):
    # Nested event serializer to display related events under each category
    events = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField('get_image_url')
    class Meta:
        model = Genre
        fields = ['id', 'genre', 'image', 'events']  # Include 'events' field

    def get_events(self, obj):
        events = obj.event_genre.all()  # Use related_name to access related events
        return EventListSerializers(events, many=True, context=self.context).data  # Serialize events

    def get_image_url(self, obj):
        request = self.context.get('request')  # Get request from context
        if request is not None:
            return request.build_absolute_uri(obj.image.url)  # Build full URL
        return obj.image.url  # Fallback to relative URL if no request




# This serializer is user to display only image and name of the event under categories
class EventListSerializers(serializers.ModelSerializer):
    image = serializers.SerializerMethodField('get_image_url')
    another_image = serializers.SerializerMethodField('get_another_image_url')

    class Meta:
        model = Event
        fields = [
            'id', 'event_name', 'image', 'another_image'
        ]

    def get_image_url(self, obj):
        request = self.context.get('request')  # Get request from context
        if request is not None:
            return request.build_absolute_uri(obj.image.url)  # Build full URL
        return obj.image.url  # Fallback to relative URL if no request

    def get_another_image_url(self, obj):
        request = self.context.get('request')  # Get request from context
        if request is not None:
            return request.build_absolute_uri(obj.image.url)  # Build full URL
        return obj.image.url  # Fallback to relative URL if no request



# Event Serializer Class, this is the detail of each events
class EventSerializers(serializers.ModelSerializer):
    category = CategorySerializers(read_only=True, source='event_category')
    image = serializers.SerializerMethodField('get_image_url')
    another_image = serializers.SerializerMethodField('get_another_image_url')
    participant_count = serializers.SerializerMethodField()
    participants = serializers.SerializerMethodField()  # To get participant details
    is_applied = serializers.SerializerMethodField()  # To get is_applied status

    class Meta:
        model = Event
        fields = [
            'id','category', 'event_name', 'location', 'latitude', 'longitude',  'description', 
            'image', 'another_image', 'event_date','week_day', 
            'participate_status', 'voting_status', 'voting_end_time',
            'participant_count','is_applied', 'participants','contest_status'  # Ensure this field is included
        ]

    def get_image_url(self, obj):
        request = self.context.get('request')  # Get request from context
        if request is not None:
            return request.build_absolute_uri(obj.image.url)  # Build full URL
        return obj.image.url  # Fallback to relative URL if no request

    def get_another_image_url(self, obj):
        request = self.context.get('request')  # Get request from context
        if request is not None:
            return request.build_absolute_uri(obj.image.url)  # Build full URL
        return obj.image.url  # Fallback to relative URL if no request

    def get_participant_count(self, obj):
        return obj.participants.count() 

    def get_participants(self, obj):
        participants = obj.participants.all()[:3]
        return [{"id": user.id, "name": user.name, "avatar": self.get_user_avatar(user)} for user in participants]

    def get_user_avatar(self, user):
        if user.avatar:
            request = self.context.get('request')
            if request is not None:
                return request.build_absolute_uri(user.avatar.url)
            return user.avatar.url
        return None  # If the user doesn't have an avatar

    def get_is_applied(self, obj):
        user = self.context.get('request').user
        return obj.participants.filter(id=user.id).exists()


# class UserProfileSerializer(serializers.ModelSerializer):
#     image = serializers.SerializerMethodField('get_image_url')

#     class Meta:
#         model = UserProfile
#         fields = ['id', 'user', 'title', 'video', 'thubnail_image', 'image']


#     def get_image_url(self, obj):
#         request = self.context.get('request')  # Get request from context
#         if request is not None:
#             return request.build_absolute_uri(obj.image.url)  # Build full URL
#         return obj.image.url  # Fallback to relative URL if no request

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'title', 'image']


class VideoCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoCategory
        fields = ['id', 'category']


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'title', 'video', 'thubnail_image', 'category']

    extra_kwargs = {
            'title': {'required': False},
            'video': {'required': False},
            'thubnail_image': {'required': False},
            'category': {'required': False},
        }

User = get_user_model()
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name']  # Add any other fields you want to be editable
        read_only_fields = ['id']
        extra_kwargs = {'email': {'required': False}, 'name': {'required': False}}

    def update(self, instance, validated_data):
        email = validated_data.get('email')
        if email and email != instance.email:
            if User.objects.filter(email=email).exists():
                raise serializers.ValidationError({"email": "This email is already in use."})
        return super().update(instance, validated_data)
        

from account.serializers import UserProfileSerializer
class UserProfileSerializer(serializers.ModelSerializer):
    # user = UserProfileSerializer(read_only=True)
    # user = serializers.ReadOnlyField(source='user.name')

    name = serializers.CharField(read_only=True)  # Assuming 'username' is used as 'name'
    email = serializers.EmailField(read_only=True)
    phone_No = serializers.CharField(read_only=True)
    avatar = serializers.ImageField(read_only=True)  # Update 'profile.avatar' if needed


    media = ImageSerializer(many=True, read_only=True)
    video = VideoSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'name', 'email','phone_No', 'avatar', 'media', 'video']

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            user_serializer = UserSerializer(instance.user, data=user_data, partial=True)
            if user_serializer.is_valid():
                user_serializer.save()
        return super().update(instance, validated_data)
    
    # def create(self, validated_data):
    #     user_data = validated_data.pop('user')
    #     user = User.objects.create_user(**user_data)
    #     user_profile = UserProfile.objects.create(user=user, **validated_data)
    #     return user_profile


# class UserProfileSerializer(serializers.ModelSerializer):
#     user_email = serializers.EmailField(source='user.email', read_only=True)
#     user_name = serializers.CharField(source='user.name', read_only=True)
#     media = ImageSerializer(many=True, read_only=True)
#     video = VideoSerializer(many=True, read_only=True)

#     class Meta:
#         model = UserProfile
#         fields = ['id', 'user_email','user_name', 'media', 'video']

#     def update(self, instance, validated_data):
#         # Optional: Handle any custom updates here if necessary
#         return super().update(instance, validated_data)




### Serializer to show the list of upcoming events that the user has participated and the list of events that has already ended.
User = get_user_model()

class ParticipatedEventListSerializers(serializers.ModelSerializer):
    image = serializers.SerializerMethodField('get_image_url')
    another_image = serializers.SerializerMethodField('get_another_image_url')

    class Meta:
        model = Event
        fields = [
            'id', 'event_name', 'image', 'another_image'
        ]

    def get_image_url(self, obj):
        request = self.context.get('request')  # Get request from context
        if obj.image:
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return None

    def get_another_image_url(self, obj):
        request = self.context.get('request')  # Get request from context
        if obj.another_image:
            return request.build_absolute_uri(obj.another_image.url) if request else obj.another_image.url
        return None


### Serializer for voting

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['event_name']

class UserVotingDetailSerializer(serializers.ModelSerializer):
    user_id = serializers.ReadOnlyField(source='user.id')
    name = serializers.ReadOnlyField(source='user.name')
    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = UserEventVoting
        fields = ['user_id', 'name', 'avatar_url', 'voting_id']

    def get_avatar_url(self, obj):
        request = self.context.get('request')  # Get the request context
        if obj.user.avatar:
            # Build the full URL for the avatar image
            avatar_url = obj.user.avatar.url
            return request.build_absolute_uri(avatar_url) if request else avatar_url
        return None  # Return None if no avatar is available

class EventVotingSettingsSerializer(serializers.ModelSerializer):
    event = EventSerializer()  # Nested serializer to show event details
    # users_voting = serializers.SerializerMethodField()  # Add a field for users voting details
    event_id = serializers.IntegerField(source='event.id')

    class Meta:
        model = EventVotingSettings
        fields = "__all__"
        
        

    def get_users_voting(self, obj):
        # Fetch all users who are part of this event
        user_voting_queryset = UserEventVoting.objects.filter(event=obj.event)
        return UserVotingDetailSerializer(user_voting_queryset, many=True).data

class KhaltiVerificationSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=255)
    amount = serializers.IntegerField(min_value=1)


## Serializer for album
class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ['id', 'title', 'company_name', 'image']

class AlbumImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlbumImage
        fields = ['id', 'image']  # Use only the AlbumImage model fields

class AlbumDetailSerializer(serializers.ModelSerializer):
    album_images = serializers.SerializerMethodField()

    class Meta:
        model = Album
        fields = ['id', 'title', 'company_name', 'image', 'album_images']

    def get_album_images(self, obj):
        images = obj.album.all()  # This is where the fix is made: using `related_name='album'`
        return AlbumImageSerializer(images, many=True).data

class VideoMenuSerializers(serializers.ModelSerializer):
    image = serializers.SerializerMethodField('get_image_url')

    class Meta:
        model = VideoMenu
        fields = ['id', 'title', 'video', 'image']

    def get_image_url(self, obj):
        request = self.context.get('request')  # Get request from context
        if request is not None:
            return request.build_absolute_uri(obj.thubnail_image.url)  # Build full URL
        return obj.thubnail_image.url  # Fallback to relative URL if no request




### Privacy policy
class PrivacyAndPolicySerializers(serializers.ModelSerializer):
    class Meta:
        model = PrivacyAndPolicy
        fields =['privacy']

### Terms and condition
class TermsAndConditionSerializers(serializers.ModelSerializer):
    class Meta:
        model = TermsAndCondition
        fields =['terms']
        


### Vote count
# class VoteCounttSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = VoteCountt
#         fields = ['event', 'voting_id', 'votes', 'total_amount']

#     def create(self, validated_data):
#         # Custom save logic if needed
#         return VoteCountt.objects.create(**validated_data)


class ContestTermConditionsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=ContestTermConditions
        fields="__all__"
        read_only_fields = ['id']
        
        
        
from rest_framework import serializers
from .models import Contest
from .models import ContestTermConditions  # Make sure to import the model

class ContestSerializer(serializers.ModelSerializer):
    # Nested serializer for related fields (User and ContestTermConditions)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())  # Foreign key to User
    # contest_terms_condition = serializers.PrimaryKeyRelatedField(queryset=ContestTermConditions.objects.all())  # Foreign key to ContestTermConditions
    


    class Meta:
        
        model = Contest
        fields = [
            'user',
            'event',
            'contest_terms_condition',
            'contestant_photo',
            'contestant_first_name',
            'contestant_last_name',
            'contestant_dob',
            'contestant_city',
            'contestant_age',
            'contestant_mobile_no',
            'contestant_whatsapp_no',
            'contestant_email',
            'contestant_school_name',
            'contestant_class',
            'contestant_father_name',
            'contestant_mother_name',
            'contestant_previous_performance',
            'contestant_no',
            "contest_status"
            
        ]
        read_only_fields = ['id']

    def validate_contestant_email(self, value):
        """
        Validate if the email is already in use.
        """
        if Contest.objects.filter(contestant_email=value).exists():
            raise serializers.ValidationError("This email is already used by another contestant.")
        return value

    def validate_contestant_mobile_no(self, value):
        """
        Validate if the mobile number is already in use.
        """
        if Contest.objects.filter(contestant_mobile_no=value).exists():
            raise serializers.ValidationError("This mobile number is already used by another contestant.")
        return value

    def validate_contestant_whatsapp_no(self, value):
        """
        Validate if the WhatsApp number is already in use.
        """
        if Contest.objects.filter(contestant_whatsapp_no=value).exists():
            raise serializers.ValidationError("This WhatsApp number is already used by another contestant.")
        return value

    def create(self, validated_data):
        """
        Create a new contest entry.
        """
        return Contest.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update an existing contest entry.
        """
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

        
        
        
from .models import ContestantLike, ContestantFollow

class ContestantLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContestantLike
        fields = ['id', 'user', 'contest', 'like']
        read_only_fields = ['id']

class ContestantFollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContestantFollow
        fields = ['id', 'user', 'contest', 'follow']
        read_only_fields = ['id']
        
        
        
from .models import ContestPhoto

class ContestPhotoUploadSerializer(serializers.Serializer):
    images = serializers.ListField(
        child=serializers.ImageField(),
        allow_empty=False
    )

    def create(self, validated_data):
        contest = self.context['contest']  # Retrieve contest from the context
        photos = []
        for image in validated_data['images']:
            photo = ContestPhoto.objects.create(contest=contest, photo=image)
            photos.append(photo)
        return photos
    
class ContestImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model=ContestPhoto
        fields ="__all__"
    
from .models import ContestVideo

class ContestVideoUrlUploadSerializer(serializers.Serializer):
    video_urls = serializers.ListField(
        child=serializers.URLField(),
        allow_empty=False
    )

    def create(self, validated_data):
        contest = self.context['contest']  # Retrieve contest from the context
        videos = []
        for url in validated_data['video_urls']:
            video = ContestVideo.objects.create(contest=contest, video_url=url)
            videos.append(video)
        return videos
class ContestVideoUploadUrlSerializer(serializers.ModelSerializer):
    class Meta:
        model=ContestVideo
        fields ="__all__"   


class EventContestantFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model=EventContestantField
        fields = ['event','field_name' ,'data_type' ,'status']

class AdsRelatedVideoSerializer(serializers.ModelSerializer):
    ad = AddSerializers(read_only=True)  # Include related ad details

    class Meta:
        model = AdsRelatedVideo
        fields = [
            'id', 'ad', 'title', 'description', 'video_url',
            'duration_in_seconds', 'created_at', 'updated_at'
        ]
        
class VideosForYouSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideosForYou
        fields = ['title', 'description','video_url','created_at','updated_at']
        
        
        

class EventSearchSerializers(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            'id', 'category', 'event_name', 'location', 'latitude', 'longitude', 
            'description', 'image', 'another_image', 'event_date', 'week_day', 
            'participate_status', 'voting_status', 'voting_end_time',
            'participant_count', 'participants', 'contest_status'
        ]