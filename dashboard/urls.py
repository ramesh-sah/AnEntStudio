from django.urls import path
from . import views 
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from .views import *
# from .views import GetQuestionSetsView


app_name ='dashboard'

urlpatterns = [
        path('',views.index,name='index'),

        ## Slider url
        path('slider',SliderListView.as_view(), name="banner_list"),
        path('slider/add',BannerCreateView.as_view(), name="banner_create"),
        path('slider/update/<int:id>',BannerUpdateDetailView.as_view(), name="bannar_update"),
        path('slider/delete', views.Bannerdelete, name='delete_bannar'),

        ## Ads url
        path('ads',AdsListView.as_view(), name="ads_list"),
        path('ads/create',AdsCreateView.as_view(), name="ads_create"),
        path('ads/update/<int:id>',AdsUpdateDetailView.as_view(), name="ads_update"),
        path('ads/delete', views.Adsdelete, name='delete_ads'),

        ## Event Category url
        path('event/category',CategoryListView.as_view(), name="category_list"),
        path('event/category/create',CategoryCreateView.as_view(), name="category_create"),
        path('event/category/update/<int:id>',CategoryUpdateDetailView.as_view(), name="category_update"),
        path('event/category/delete', views.Categorydelete, name='delete_category'),

        ## Event Genre url
        path('event/genre',GenreListView.as_view(), name="genre_list"),
        path('event/genre/create',GenreCreateView.as_view(), name="genre_create"),
        path('event/genre/update/<int:id>',GenreUpdateDetailView.as_view(), name="genre_update"),
        path('event/genre/delete', views.Genredelete, name='delete_genre'),

        ## Event url
        path('event',EventListView.as_view(), name="event_list"),
        path('event/create',EventCreateView.as_view(), name="event_create"),
        path('event/update/<int:id>',EventUpdateDetailView.as_view(), name="event_update"),
        path('event/delete', views.Eventdelete, name='delete_event'),
        path('event/<int:pk>/', EventDetailView.as_view(), name='event_detail'),

        ## Video Category url
        path('video/category',VideoCategoryListView.as_view(), name="videocategory_list"),
        path('video/category/create',VideoCategoryCreateView.as_view(), name="videocategory_create"),
        path('video/category/update/<int:id>',VideoCategoryUpdateDetailView.as_view(), name="videocategory_update"),
        path('video/category/delete', views.VideoCategorydelete, name='delete_videocategory'),

        ## Voting url
        path('voting',VotingListView.as_view(), name="voting_list"),
        path('voting/create',VotingCreateView.as_view(), name="voting_create"),
        path('voting/update/<int:id>',VotingUpdateDetailView.as_view(), name="voting_update"),
        path('voting/delete', views.Votingdelete, name='delete_voting'),

        ## User to be voted - url
        path('voting/user',VotingUserListView.as_view(), name="votinguser_list"),
        # path('voting/user',views.voting_event_list, name="votinguser_list"),
        path('voting/user/create',VotingUserCreateView.as_view(), name="votinguser_create"),
        path('voting/user/update/<int:id>',VotingUserUpdateDetailView.as_view(), name="votinguser_update"),
        path('voting/user/delete', views.VotingUserdelete, name='delete_votinguser'),
        path('voting/user/detail/<int:pk>/', VotingDetailView.as_view(), name='voting_detail'),
        path('voting/user/<int:event_id>', views.add_voting_user, name='add_voting_user'),

        path('voting/user/update/<int:id>',UpdateVotingUserDetailView.as_view(), name="votinguserdetail_update"),
        path('voting/user/delete/<int:pk>/', DeleteVotingUserDetailView.as_view(), name='delete_votinguserdetail'),

        ### Urls for voting count
        path('voting/count/', views.event_list, name='vote_list'),
        path('voting/count/<int:event_id>/', views.event_detail, name='vote_count'),

        ### Urls for organization setting
        path('company-detail', views.organizationSettings, name='company_detail'),

        ### Urls for video menu
        path('video',VideoListView.as_view(), name="video_list"),
        path('video/upload',VideoCreateView.as_view(), name="video_create"),
        path('video/update/<int:id>',VideoUpdateDetailView.as_view(), name="video_update"),
        path('video/delete', views.Videodelete, name='delete_video'),

        path('album',AlbumListView.as_view(), name="album_list"),
        path('album/add',views.create_or_edit_album, name='add_Album'),
        path('album/update/<int:album_id>/', views.create_or_edit_album, name='edit_Album'),
        path('album/delete', views.Albumdelete, name='delete_album'),

        ### URL for privacy and policy 
        path('privacy-and-policy/add',views.PolicyAndPrivacy, name='add_PolicyAndPrivacy'),
        path('privacy-policy/preview', PrivacyListView.as_view(), name='privacy'),

        ### URL for terms and condition 
        path('terms-and-condition/add',views.TermssAndCondition, name='add_TermsAndCondition'),
        path('terms-and-condition/preview', TermsListView.as_view(), name='terms'),

        ### URL for user
        path('user-list',UserListView.as_view(), name='user'),

        ### Url for logout, login, change password
        path('logout', views.userlogout, name='logout'),
        path('login/',views.login,name='login'),
        path('change-password', views.change_password, name='change_password'),

        

]+ static (settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)