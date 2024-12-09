from django.contrib import admin
from api.models import (Slider, Add, Category, Event, Image, Video, VideoCategory, 
                        Genre,EventVotingSettings, UserEventVoting, OrganizationSetting,
                        AlbumImage, Album, VideoMenu, PrivacyAndPolicy, TermsAndCondition,VoteScore,EventContestantField)
from account.models import User

# Register your models here.

class SliderAdmin(admin.ModelAdmin):
    model =Slider
    list_display=['id','image']
admin.site.register(Slider,SliderAdmin)

class AddAdmin(admin.ModelAdmin):
    model =Add
    list_display=['id','image']
admin.site.register(Add,AddAdmin)

class CategoryAdmin(admin.ModelAdmin):
    model =Category
    list_display=['category', 'order']
admin.site.register(Category,CategoryAdmin)

class GenreAdmin(admin.ModelAdmin):
    model =Genre
    list_display=['genre']
admin.site.register(Genre,GenreAdmin)

class EventAdmin(admin.ModelAdmin):
    model =Event
    list_display=[
            'id','category', 'event_name', 'location','latitude', 'longitude', 'image', 'another_image', 
            'event_date', 'week_day', 'participate_start_time', 'participate_end_time', 
            'participate_status', 'voting_start_time', 'voting_end_time', 'voting_status',
            'participant_count'
        ]
admin.site.register(Event,EventAdmin)

class ImageAdmin(admin.ModelAdmin):
    model =Image
    list_display=['user_profile','title', 'image']
admin.site.register(Image,ImageAdmin)

class VideoCategoryAdmin(admin.ModelAdmin):
    model =VideoCategory
    list_display=['category']
admin.site.register(VideoCategory,VideoCategoryAdmin)

# class Video(admin.ModelAdmin):
#     model = Video
#     list_display = ['user_profile', 'category', 'title', 'video','thubnail_image']
# admin.site.register(Video,VideoAdmin)

admin.site.register(Video)

admin.site.register(EventVotingSettings)
admin.site.register(UserEventVoting)
admin.site.register(OrganizationSetting)


# Define an inline admin descriptor for AlbumImage model
class AlbumImageInline(admin.TabularInline):  # You can also use StackedInline for a different layout
    model = AlbumImage
    extra = 1  # Specifies the number of extra empty forms to display

# Create a custom admin class for Album
class AlbumAdmin(admin.ModelAdmin):
    inlines = [AlbumImageInline]

# Register the Album model with the custom AlbumAdmin
admin.site.register(Album, AlbumAdmin)

class VideoMenuAdmin(admin.ModelAdmin):
    model =VideoMenu
    list_display=['title','video','thubnail_image']
admin.site.register(VideoMenu,VideoMenuAdmin)


admin.site.register(PrivacyAndPolicy)
admin.site.register(TermsAndCondition)
admin.site.register(VoteScore)
admin.register(EventContestantField)
class EventContestantFieldAdmin(admin.ModelAdmin):
    list_display = ('event', 'field_name', 'data_type', 'status', 'created_at', 'updated_at')
    list_filter = ('event', 'status')
    search_fields = ('field_name',)
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)




