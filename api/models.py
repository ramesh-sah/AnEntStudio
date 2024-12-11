from django.db import models
from ckeditor.fields import RichTextField
from django.db.models.signals import pre_save,pre_delete
from django.dispatch import receiver
from django.utils import timezone
from django.conf import settings
from django.db.models import Q
from django.db.models import Sum
from datetime import date as dates


from account.models import User

# Create your models here.

class Slider(models.Model):
    image = models.ImageField(upload_to='sliderimage/')

    class Meta:
        verbose_name = "Slider"
        verbose_name_plural = "Sliders"
        ordering =['id']

    def __str__(self):
        return str(self.image)

class Add(models.Model):
    image = models.ImageField(upload_to='addimage/')
    title = models.CharField(max_length=255, help_text="Title of the Ads")
    class Meta:
        verbose_name = "Add"
        verbose_name_plural = "Adds"
        ordering =['id']
        
        
class AdsRelatedVideo(models.Model):
    ad = models.ForeignKey(Add, on_delete=models.CASCADE, related_name="videos", help_text="The ad campaign this video is related to")
    description = models.TextField(blank=True, null=True, help_text="Brief description of the video content")
    video_url = models.URLField(help_text="URL of the video")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Time when the video was added")
    updated_at = models.DateTimeField(auto_now=True, help_text="Time when the video was last updated")
    duration_in_seconds = models.IntegerField(blank=True, null=True, help_text="Duration of the video in seconds")
    
    

    def __str__(self):
        return f"{self.title} (Ad: {self.ad.name})"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Ads Related Video"
        verbose_name_plural = "Ads Related Videos"

 

class Category(models.Model):
    category = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering =['order']

    def __str__(self):
        return str(self.category)

class Genre(models.Model):
    genre = models.CharField(max_length=200)
    image = models.ImageField(upload_to='genreimage/')

    class Meta:
        verbose_name = "genre"
        verbose_name_plural = "genres"
        ordering =['id']

    def __str__(self):
        return str(self.genre)
    
# class EventTermConditions(models.Model):
#     """
#     Model representing terms and conditions for a event.
#     """

#     # Link to the authorized user (organizer or admin)
#     user = models.ForeignKey(
#         User,
#         related_name='authorized_user',
#         on_delete=models.CASCADE,  # Delete terms when the user is deleted
#     )

    

#     # Terms and conditions field with rich text support
#     terms_conditions = RichTextField()

#     # Approval status of terms and conditions
#     approved = models.BooleanField(default=False)

#     def __str__(self):
#         return f"Terms and Conditions - {self.approved}"



class Event(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE,related_name='event_category')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE,related_name='event_genre', null=True, blank= True)
    event_name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='eventimage/')
    another_image = models.ImageField(upload_to='eventimage/', null=True, blank=True)
    event_date = models.DateTimeField(null=True, blank=True)
    week_day = models.IntegerField(choices=((0, 'Sunday'), (1, 'Monday'), (2, 'Tuesday'), 
                                            (3, 'Wednesday'), (4, 'Thursday'), (5, 'Friday'), (6, 'Saturday')))

    # Time-related fields for participation and voting
    participate_start_time = models.DateTimeField(null=True, blank=True)
    participate_end_time = models.DateTimeField(null=True, blank=True)
    participate_status = models.BooleanField(default=False)

    voting_start_time = models.DateTimeField(null=True, blank=True)
    voting_end_time = models.DateTimeField(null=True, blank=True)
    voting_status = models.BooleanField(default=False)
    # event_term_condition= models.ForeignKey(EventTermConditions, on_delete=models.CASCADE,related_name='event_terms_condition', null=True, blank= True)

    location = models.CharField(max_length=200)
    latitude = models.FloatField()
    longitude = models.FloatField()
    # location_url = models.URLField(max_length=500)
    description = models.TextField()
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="events", blank=True)
    
    
    # Time-related fields for  contest
    contest_start_time = models.DateTimeField(null=True, blank=True)
    contest_end_time = models.DateTimeField(null=True, blank=True)
    contest_status = models.BooleanField(default=False)

    class Meta:
        verbose_name = "event"
        verbose_name_plural = "events"
        ordering = ['-id']

    def __str__(self):
        return str(self.event_name)

    @property
    def participant_count(self):
        return self.participants.count()

    def update_status(self):
        """
        Automatically update participation and voting status based on the current time.
        If the voting end time has passed, the event is deleted.
        """
        now = timezone.now()

        # Update participation status
        try:
            if self.participate_start_time <= now <= self.participate_end_time:
                self.participate_status = True
            else:
                self.participate_status = False
        except:
            self.participate_status=False
            
            
        # Update contest status
        try:
            if self.contest_start_time <= now <= self.contest_end_time:
                self.contest_status = True
            else:
                self.contest_status = False
        except:
            self.contest_status=False
            

            

        # Update voting_status
        try:
                if self.voting_start_time <= now <= self.voting_end_time:
                    self.voting_status = True
                    
                else:
                    self.voting_status = False
        except:
                self.voting_status=False
            

        self.save()
        
class EventContestantField(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='event_contestant_field')
    field_name = models.CharField(max_length=200)
    data_type=models.CharField(max_length=200)
    status=models.BooleanField(default=False)
    created_at=models.DateField(auto_now_add=True)
    updated_at=models.DateField(auto_now=True)


# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
#     def __str__(self):
#         return f"{self.user.email}'s profile"

class Image(models.Model):
    user_profile = models.ForeignKey(User, on_delete=models.CASCADE, related_name='media')
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='userimage/')

    def __str__(self):
        return str(self.title)


class VideoCategory(models.Model):
    category = models.CharField(max_length=200)

    def __str__(self):
        return str(self.category)

class Video(models.Model):
    user_profile = models.ForeignKey(User, on_delete=models.CASCADE, related_name='video')
    category = models.ForeignKey(VideoCategory,on_delete=models.CASCADE, related_name='video_category')
    title = models.CharField(max_length=200)
    video = models.URLField(max_length=500)
    thubnail_image = models.ImageField(upload_to = 'thubnail_image')




### Voting and amount count
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save

# VoteScore Model
class VoteScore(models.Model):
    event = models.ForeignKey('Event', on_delete=models.CASCADE, related_name='vote_scores')
    user_event_voting = models.ForeignKey('UserEventVoting', on_delete=models.CASCADE, related_name='vote_scores')
    vote_count = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('event', 'user_event_voting')

    def __str__(self):
        return f'Vote Score for {self.user_event_voting.user.name} in {self.event.event_name}'

    # def clean(self):
    #     if self.event != self.user_event_voting.event:
    #         raise ValidationError("The UserEventVoting must be associated with the same Event.")

    #     voting_settings = self.event.voting_settings
    #     if self.vote_count < voting_settings.min_vote or self.vote_count > voting_settings.max_vote:
    #         raise ValidationError(f"Vote count must be between {voting_settings.min_vote} and {voting_settings.max_vote}.")

    #     expected_amount = Decimal(self.vote_count) * voting_settings.price_per_vote
    #     if abs(self.amount - expected_amount) > Decimal('0.01'):
    #         raise ValidationError(f"Amount should be {expected_amount} based on the vote count and price per vote.")






# Album detail
class Album(models.Model):
    image = models.ImageField(upload_to='albumimage/')
    title = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200)

    def __str__(self):
        return str(self.title)

class AlbumImage(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='album')
    image = models.ImageField(upload_to='albumimage/')


# Organization Detail
class OrganizationSetting(models.Model):
    organization_name = models.CharField(max_length=150)
    logo = models.ImageField(upload_to="companylogo/", null=True, blank=True)
    address = models.CharField(max_length=150)
    email = models.CharField(max_length=200)
    phone_no = models.IntegerField()

    def __str__(self):
        return self.organization_name


class VideoMenu(models.Model):
    title = models.CharField(max_length=200)
    video = models.URLField(max_length=500)
    thubnail_image = models.ImageField(upload_to = 'thubnail_image')

    def __str__(self):
        return str(self.title)


class PrivacyAndPolicy(models.Model):
    privacy = RichTextField()

class TermsAndCondition(models.Model):
    terms = RichTextField()

from django.db import models
import uuid  # For generating unique UUIDs
from django.utils.translation import gettext_lazy as _  # For translations
from ckeditor.fields import RichTextField  # For rich text fields (terms and conditions)


class ContestTermConditions(models.Model):
    """
    Model representing terms and conditions for a contest.
    """

    # Link to the authorized user (organizer or admin)
    user = models.ForeignKey(
        User,
        related_name='authorized_user',
        on_delete=models.CASCADE,  # Delete terms when the user is deleted
    )

    # Authorized signature image
    authorized_signature = models.ImageField(
        upload_to="contest_authorized_signature",  # Directory for storing authorized signatures
        null=True,  # Allow null values
        blank=True  # Allow blank values
    )

    # Terms and conditions field with rich text support
    terms_conditions = RichTextField()

    # Approval status of terms and conditions
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Terms and Conditions - {self.user.username}"
    
    



class Contest(models.Model):
    """
    Model representing a contest and its contestant details.
    """

    # Link to the user (contest organizer or admin)
    user = models.ForeignKey(
        User,
        related_name='contest_user',
        on_delete=models.CASCADE,  # Delete contest if the user is deleted
    )
    event=models.ForeignKey(Event,related_name="event",on_delete=models.CASCADE)

    # Link to contest terms and conditions
    contest_terms_condition = models.ForeignKey(
        ContestTermConditions,
        related_name='contest_terms_condition',
        on_delete=models.CASCADE,  # Delete contest if terms and conditions are deleted
    )

    # Contestant details
    contestant_photo = models.ImageField(upload_to='contestant_image',null=True)  # Stores contestant's photo
    contestant_first_name = models.CharField(max_length=50)  # First name
    contestant_last_name = models.CharField(max_length=50)  # Last name
    contestant_dob = models.DateField()  # Date of birth
    contestant_city = models.CharField(max_length=100)  # City of residence
    contestant_age = models.PositiveIntegerField()  # Age (only positive numbers allowed)
    contestant_mobile_no = models.CharField(max_length=15, null=True, blank=True)  # Mobile number
    contestant_whatsapp_no = models.CharField(max_length=15, null=True, blank=True)  # WhatsApp number
    contestant_email = models.EmailField(unique=True)  # Email address (must be unique)
    contestant_school_name = models.CharField(max_length=100)  # School name
    contestant_class = models.CharField(max_length=50)  # Class or grade
    contestant_father_name = models.CharField(max_length=100)  # Father's name
    contestant_mother_name = models.CharField(max_length=100)  # Mother's name
    contestant_previous_performance = models.BooleanField(default=False)  # Indicates prior performance

    # Unique contestant number
    contestant_no = models.IntegerField(default=None)
    
    CONTEST_STATUS_CHOICES = [
        ('approved', 'Approved'),
        ('pending', 'Pending'),
        ('rejected', 'Rejected'),
    ]
    
    contest_status = models.CharField(
        max_length=10,
        choices=CONTEST_STATUS_CHOICES,
        default='pending',  # Default status is 'Pending'
    )
    
    
    

   

    # Contest category options
    class ContestCategory(models.TextChoices):
        DANCING = 'dancing', _('Dancing')
        SINGING = 'singing', _('Singing')
        ACTING_COMEDY = 'acting/comedy', _('Acting/Comedy')
        DRAWING = 'drawing', _('Drawing')
        OTHERS = 'others', _('Others')

    contest_category = models.CharField(
        max_length=50,
        choices=ContestCategory.choices,  # Use predefined categories
        default=ContestCategory.OTHERS  # Default to "Others"
    )

    # Timestamps for record tracking
    created_at = models.DateField(auto_now_add=True)  # Automatically set on creation
    
    
    updated_at = models.DateField(auto_now=True)  # Automatically updated on save
    def __str__(self):
        return f"{self.contestant_first_name} {self.contestant_last_name} - {self.get_contest_category_display()}"
    
    def save(self, *args, **kwargs):
        """
        Override save method to assign a unique auto-incrementing value to contestant_no.
        """
        if not self.contestant_no:
            # Get the max existing contestant_no or set to 0 if none exist
            last_contestant_no = Contest.objects.aggregate(
                max_no=models.Max('contestant_no')
            )['max_no'] or 0
            self.contestant_no = last_contestant_no + 1
        super().save(*args, **kwargs)
        
    
        
        
  
class ContestantLike(models.Model):
    user = models.ForeignKey(
        User,
        related_name='contest_likes',  # Unique related_name for likes
        on_delete=models.CASCADE,  # Delete likes if the user is deleted
    )
    contest = models.ForeignKey(
        Contest,  # Assuming you have a Contest model defined elsewhere
        related_name='likes',
        on_delete=models.CASCADE,  # Delete likes if the contest is deleted
    )
    like = models.IntegerField(default=1)

    def __str__(self):
        return f"Like by {self.user.username} for Contest ID {self.contest.id}"


class ContestantFollow(models.Model):
    user = models.ForeignKey(
        User,
        related_name='contest_follows',  # Unique related_name for follows
        on_delete=models.CASCADE,  # Delete follows if the user is deleted
    )
    contest = models.ForeignKey(
        Contest,  # Assuming you have a Contest model defined elsewhere
        related_name='follows',
        on_delete=models.CASCADE,  # Delete follows if the contest is deleted
    )
    follow = models.IntegerField(default=1)

    def __str__(self):
        return f"Follow by {self.user.username} for Contest ID {self.contest.id}"
    
    
class ContestPhoto(models.Model):
    """
    Model for storing multiple photos related to a contest.
    """
    contest = models.ForeignKey(
        Contest,
        related_name='photos',
        on_delete=models.CASCADE
    )
    photo = models.ImageField(upload_to='contest_photos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo for Contest: {self.contest.id}"


class ContestVideo(models.Model):
    """
    Model for storing multiple video URLs related to a contest.
    """
    contest = models.ForeignKey(
        Contest,
        related_name='videos',
        on_delete=models.CASCADE
    )
    video_title=models.CharField(max_length=255)
    video_url = models.URLField()
    
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Video for Contest: {self.contest.id}"



# Event Voting Settings Model
class EventVotingSettings(models.Model):
    event = models.OneToOneField(Event, on_delete=models.CASCADE, related_name='voting_settings')
    
    max_vote = models.IntegerField()
    min_vote = models.IntegerField()
    price_per_vote = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Voting Settings for {self.event.event_name}'
    
    

from django.core.validators import MinValueValidator


# User Event Voting Model
class UserEventVoting(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_votes')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='user_event_votes')
    voting_id = models.IntegerField()
    contest=models.ForeignKey(Contest,on_delete=models.CASCADE, related_name='contest')

    def __str__(self):
        return f'Voting ID {self.voting_id} for {self.user.name} in {self.event.event_name}'

    @property
    def name(self):
        return self.user.name

    @property
    def avatar(self):
        # Assuming the user has a profile with an avatar field
        return self.user.profile.avatar
    
    
    
from django.db import models


class VideosForYou(models.Model):
    title = models.CharField(max_length=255, help_text="Title of the video")
    description = models.TextField(blank=True, null=True, help_text="Description of the video")
    video_url = models.URLField(help_text="URL of the video")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the video was added")
    updated_at = models.DateTimeField(auto_now=True, help_text="Timestamp when the video was last updated")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Video for You"
        verbose_name_plural = "Videos for You"





