from django.urls import path
from . import views
from . views import (AdsRelatedVideoAPIView, ContestBulkPhotoUploadView, ContestBulkVideoUploadView, ContestantViewOwnContest, EventContestantFieldView, EventSearch, SliderListAPIView, AddListAPIView, EventListAPIView,CategoryListAPIView,
                    CategoryDetailAPIView,CategoryEventDetailAPIView, EventParticipationAPIView,
                    UserProfileListCreateAPIView, UserProfileDetailAPIView, 
                    ImageUploadAPIView, VideoUploadAPIView, GenreListAPIView, GenreDetailAPIView,
                    GenreEventDetailAPIView, UserParticipatedEventsView,
                    ImageDetailAPIView, VideoDetailAPIView, VideoCategoryAPIView,
                    EventVotingSettingsListView,EventVotingSettingsDetailView,
                    InitiateKhaltiPayment, VerifyKhalti, AlbumListCreateView,
                    AlbumRetrieveUpdateDestroyView, AlbumImagesView, 
                    PrivacyAndPolicyListAPIView, TermsAndConditionListAPIView, VideosForYouAPIView,
                    create_vote_score, VideoMenuListAPIView,ContestantLikeAPIView, ContestantFollowAPIView
                    )



urlpatterns = [
    path('sliders', SliderListAPIView.as_view(), name='sliders'),
    path('adds', AddListAPIView.as_view(), name='adds'),
    path('ads-related-videos',AdsRelatedVideoAPIView.as_view(),name='ads-related-videos-getAll'),
    path('ads-related-videos/<int:id>/',AdsRelatedVideoAPIView.as_view(),name='ads-related-videos-getSpecific'),
  
   
   
    path('events', EventListAPIView.as_view(), name='events'),
    path('events/<int:id>', EventListAPIView.as_view(), name='events'),
    path('events/participation/<int:event_id>', EventParticipationAPIView.as_view(), name='participants'),

    ## Search url
    # path('event/search/', EventSearchAPIView.as_view(), name='event-search'),
    path('events/search/<str:event_name>/', EventSearch.as_view(), name='events_search'),

    path('categories/', CategoryListAPIView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailAPIView.as_view(), name='category-detail'),
    path('categories/<int:category_pk>/<int:event_pk>/', CategoryEventDetailAPIView.as_view(), name='category-event-detail'),


    path('genre/', GenreListAPIView.as_view(), name='genre-list'),
    path('genre/<int:pk>/', GenreDetailAPIView.as_view(), name='genre-detail'),
    path('genre/<int:genre_pk>/<int:event_pk>/', GenreEventDetailAPIView.as_view(), name='genre-event-detail'),

    path('user-profiles/', UserProfileListCreateAPIView.as_view(), name='user-profile-list-create'),
    path('user-profiles/<int:pk>/', UserProfileDetailAPIView.as_view(), name='user-profile-detail'),
    path('user-profiles/image/', ImageUploadAPIView.as_view(), name='image-upload'),
    path('user-profiles/image/<int:pk>/', ImageDetailAPIView.as_view(), name='image-detail'),
    path('user-profiles/video/', VideoUploadAPIView.as_view(), name='video-upload'),
    path('user-profiles/video/category', VideoCategoryAPIView.as_view(), name='video-category'),
    path('user-profiles/video/<int:pk>/', VideoDetailAPIView.as_view(), name='video-detail'),
    
    ### Video menu 
    path('video-menu', VideoMenuListAPIView.as_view(), name='videomenu'),


    path('user/participated-events/', UserParticipatedEventsView.as_view(), name='user-participated-events'),

    path('voting/', EventVotingSettingsListView.as_view(), name='event-settings-list'),
    path('voting/<int:event_id>/', EventVotingSettingsDetailView.as_view(), name='event-settings-detail'),

    path('khalti/initiate/', InitiateKhaltiPayment.as_view(), name='verify-khalti-payment'),
    path('khalti/verify/', VerifyKhalti.as_view(), name='verify_payment'),

    path('album/', AlbumListCreateView.as_view(), name='album-list'),
    path('album/<int:pk>/', AlbumRetrieveUpdateDestroyView.as_view(), name='album-detail'),
    path('album/image/<int:pk>/', AlbumImagesView.as_view(), name='album-images'),


    path('privacy-and-policy/', PrivacyAndPolicyListAPIView.as_view(), name='sliders'),
    path('terms-and-condition/', TermsAndConditionListAPIView.as_view(), name='adds'),

    path('vote-count/', views.create_vote_score, name='votecountt'),
    

    # path('initiate',views.init_khalti_payment,name="initiate"),
    # path('verify',views.verify_khalti_payment,name="verify"),
    path('contest-term-conditions/', views.ContestTermConditionsView.as_view(), name='contest-term-conditions'),
    path('contest-term-conditions/<int:pk>/', views.ContestTermConditionsView.as_view(), name='contest-term-conditions'),
    
    path('contest/', views.ContestView.as_view(), name='contest'),
    path('contest/event-fields/<int:event_id>/', views.ContestDetailView.as_view(), name='event_contest_fields_detail '),
    path('contest/<int:pk>/', views.ContestView.as_view(), name='contest'),
    path('contestant-likes/', ContestantLikeAPIView.as_view(), name='contestant-like'),
    path('contestant-follows/', ContestantFollowAPIView.as_view(), name='contestant-follow'),
    path('contestant-all-contest/',ContestantViewOwnContest.as_view(),name='contestant-view-all-own-contest'),
    
    path('contest/<int:contest_id>/upload-photos/', ContestBulkPhotoUploadView.as_view(), name='bulk-photo-upload'),
    path('contest/<int:contest_id>/upload-videos-url/', ContestBulkVideoUploadView.as_view(), name='bulk-video-upload'),
    
    path('event-contestant-fields/<int:pk>/', EventContestantFieldView.as_view(), name='event-contestant-field-detail'),
    path('event-contestant-fields/', EventContestantFieldView.as_view(), name='event-contestant-field-detail'),
    
     path('videos-for-you/', VideosForYouAPIView.as_view(), name='videos_for_you_list'),
    path('videos-for-you/<int:pk>/', VideosForYouAPIView.as_view(), name='videos_for_you_detail'),
     
     
]


