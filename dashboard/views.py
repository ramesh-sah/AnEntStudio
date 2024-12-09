#Django imports
from django.shortcuts import render, redirect,get_object_or_404
from django.urls import reverse
from django.views import View
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.forms import PasswordChangeForm
from django.core.paginator import Paginator
from django.http import HttpResponseBadRequest
from django.views import generic
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView, DeleteView
from django.forms import modelform_factory
from django.db.models import Sum
from django.forms import inlineformset_factory
from django.contrib.auth.forms import PasswordChangeForm

# Local imports
from account.models import User
from dashboard.models import *
from dashboard.forms import *
from .decorators import login_required
from api.models import (Slider, Add, Category, Event, Genre,VideoCategory, 
                        EventVotingSettings, UserEventVoting, VideoMenu,
                        Album, AlbumImage, PrivacyAndPolicy, TermsAndCondition,
                        VoteScore)


# Create your views here.
# @admin_required
@login_required
def index(request):
    return render(request,'dashboard/index.html')

'''Slider View'''

## Slider List View
class SliderListView(generic.ListView):
    model = Slider
    template_name ='dashboard/slider/slider_list.html'
    context_object_name ='sliders'

    

## Slider Create views
class BannerCreateView(generic.CreateView):
    model = Slider
    template_name ='dashboard/slider/create_slider.html'
    form_class = SliderForm

    def get_success_url(self) -> str:
        messages.success(self.request,"New Slider image added successfully !")
        return reverse_lazy("dashboard:banner_list")

## Slider Update View
class BannerUpdateDetailView(generic.UpdateView):
    model = Slider
    template_name ='dashboard/slider/create_slider.html'
    context_object_name ='slider'
    pk_url_kwarg ='id'
    form_class = SliderForm
    
    def get_success_url(self):
        messages.success(self.request,'Updated Successfully !')
        return reverse('dashboard:banner_list')

## Slider delete view
def Bannerdelete(request):
    if request.method == "POST":
        id = request.POST.get('bannar_id')
        if not id:
            return HttpResponseBadRequest("Bad Request: No ID provided.")
        instance = get_object_or_404(Slider, id=id)
        instance.delete()
        messages.success(request, "Deleted Successfully!")
        return redirect('dashboard:banner_list')
    else:
        return redirect('dashboard:banner_list')


'''Ads View'''
## Ads List View
class AdsListView(generic.ListView):
    model = Add
    template_name ='dashboard/ads/ads_list.html'
    context_object_name ='adss'

    

## Ads Create views
class AdsCreateView(generic.CreateView):
    model = Add
    template_name ='dashboard/ads/create_ads.html'
    form_class = AdsForm

    def get_success_url(self) -> str:
        messages.success(self.request,"New Ads image added successfully !")
        return reverse_lazy("dashboard:ads_list")

## Ads Update View
class AdsUpdateDetailView(generic.UpdateView):
    model = Add
    template_name ='dashboard/ads/create_ads.html'
    context_object_name ='adss'
    pk_url_kwarg ='id'
    form_class = AdsForm
    
    def get_success_url(self):
        messages.success(self.request,'Updated Successfully !')
        return reverse('dashboard:ads_list')

## Ads delete view
def Adsdelete(request):
    if request.method == "POST":
        id = request.POST.get('ads_id')
        if not id:
            return HttpResponseBadRequest("Bad Request: No ID provided.")
        instance = get_object_or_404(Add, id=id)
        instance.delete()
        messages.success(request, "Deleted Successfully!")
        return redirect('dashboard:ads_list')
    else:
        return redirect('dashboard:ads_list')


'''Event View'''

'''Event Category'''
## Event category List View
class CategoryListView(generic.ListView):
    model = Category
    template_name ='dashboard/event/category_list.html'
    context_object_name ='categories'
    ordering = ['order']  # Ensure categories are ordered by the 'order' field

    def get_queryset(self):
        return Category.objects.all().order_by('order')

## Event category Create views
class CategoryCreateView(generic.CreateView):
    model = Category
    template_name ='dashboard/event/create_category.html'
    form_class = CategoryForm

    def get_success_url(self) -> str:
        messages.success(self.request,"New event category added successfully !")
        return reverse_lazy("dashboard:category_list")

## Event category Update View
class CategoryUpdateDetailView(generic.UpdateView):
    model = Category
    template_name ='dashboard/event/create_category.html'
    context_object_name ='categories'
    pk_url_kwarg ='id'
    form_class = CategoryForm
    
    def get_success_url(self):
        messages.success(self.request,'Updated Successfully !')
        return reverse('dashboard:category_list')

## Event category delete view
def Categorydelete(request):
    if request.method == "POST":
        id = request.POST.get('category_id')
        if not id:
            return HttpResponseBadRequest("Bad Request: No ID provided.")
        instance = get_object_or_404(Category, id=id)
        instance.delete()
        messages.success(request, "Deleted Successfully!")
        return redirect('dashboard:category_list')
    else:
        return redirect('dashboard:category_list')


'''Évent Genre'''
## Event genre List View
class GenreListView(generic.ListView):
    model = Genre
    template_name ='dashboard/event/genre_list.html'
    context_object_name ='genres'

    

## Event Genre Create views
class GenreCreateView(generic.CreateView):
    model = Genre
    template_name ='dashboard/event/create_genre.html'
    form_class = GenreForm

    def get_success_url(self) -> str:
        messages.success(self.request,"New event genre added successfully !")
        return reverse_lazy("dashboard:genre_list")

## Event genre Update View
class GenreUpdateDetailView(generic.UpdateView):
    model = Genre
    template_name ='dashboard/event/create_genre.html'
    context_object_name ='categories'
    pk_url_kwarg ='id'
    form_class = GenreForm
    
    def get_success_url(self):
        messages.success(self.request,'Updated Successfully !')
        return reverse('dashboard:genre_list')

## Event genre delete view
def Genredelete(request):
    if request.method == "POST":
        id = request.POST.get('genre_id')
        if not id:
            return HttpResponseBadRequest("Bad Request: No ID provided.")
        instance = get_object_or_404(Genre, id=id)
        instance.delete()
        messages.success(request, "Deleted Successfully!")
        return redirect('dashboard:genre_list')
    else:
        return redirect('dashboard:genre_list')


'''Creating Event'''
## Event List View
class EventListView(generic.ListView):
    model = Event
    template_name ='dashboard/event/event_list.html'
    context_object_name ='events'

##Event detail view
class EventDetailView(DetailView):
    model = Event
    template_name = 'dashboard/event/event_detail.html'
    context_object_name = 'event'

## Event Create views
class EventCreateView(generic.CreateView):
    model = Event
    template_name ='dashboard/event/create_event.html'
    form_class = EventForm

    def get_success_url(self) -> str:
        messages.success(self.request,"New event added successfully !")
        return reverse_lazy("dashboard:event_list")

## Event Update View
class EventUpdateDetailView(generic.UpdateView):
    model = Event
    template_name ='dashboard/event/create_event.html'
    context_object_name ='events'
    pk_url_kwarg ='id'
    form_class = EventForm
    
    def get_success_url(self):
        messages.success(self.request,'Updated Successfully !')
        return reverse('dashboard:event_list')

## Event delete view
def Eventdelete(request):
    if request.method == "POST":
        id = request.POST.get('event_id')
        if not id:
            return HttpResponseBadRequest("Bad Request: No ID provided.")
        instance = get_object_or_404(Event, id=id)
        instance.delete()
        messages.success(request, "Deleted Successfully!")
        return redirect('dashboard:event_list')
    else:
        return redirect('dashboard:event_list')



'''Video upload Category'''
## Event category List View
class VideoCategoryListView(generic.ListView):
    model = VideoCategory
    template_name ='dashboard/videoCategory/videocategory_list.html'
    context_object_name ='categories'

## Event category Create views
class VideoCategoryCreateView(generic.CreateView):
    model = VideoCategory
    template_name ='dashboard/videoCategory/create_videocategory.html'
    form_class = VideoCategoryForm

    def get_success_url(self) -> str:
        messages.success(self.request,"New event category added successfully !")
        return reverse_lazy("dashboard:videocategory_list")

## Event category Update View
class VideoCategoryUpdateDetailView(generic.UpdateView):
    model = VideoCategory
    template_name ='dashboard/videoCategory/create_videocategory.html'
    context_object_name ='videocategories'
    pk_url_kwarg ='id'
    form_class = VideoCategoryForm
    
    def get_success_url(self):
        messages.success(self.request,'Updated Successfully !')
        return reverse('dashboard:videocategory_list')

## Event category delete view
def VideoCategorydelete(request):
    if request.method == "POST":
        id = request.POST.get('videocategory_id')
        if not id:
            return HttpResponseBadRequest("Bad Request: No ID provided.")
        instance = get_object_or_404(VideoCategory, id=id)
        instance.delete()
        messages.success(request, "Deleted Successfully!")
        return redirect('dashboard:videocategory_list')
    else:
        return redirect('dashboard:videocategory_list')


'''Voting'''
## Voting List View
class VotingListView(generic.ListView):
    model = EventVotingSettings
    template_name ='dashboard/voting/voting_list.html'
    context_object_name ='voting'

## voting Create views
class VotingCreateView(generic.CreateView):
    model = EventVotingSettings
    template_name ='dashboard/voting/create_voting.html'
    form_class = VotingForm

    def get_success_url(self) -> str:
        messages.success(self.request,"New event category added successfully !")
        return reverse_lazy("dashboard:voting_list")

## Event category Update View
class VotingUpdateDetailView(generic.UpdateView):
    model = EventVotingSettings
    template_name ='dashboard/voting/create_voting.html'
    context_object_name ='voting'
    pk_url_kwarg ='id'
    form_class = VotingForm
    
    def get_success_url(self):
        messages.success(self.request,'Updated Successfully !')
        return reverse('dashboard:voting_list')

## Event category delete view
def Votingdelete(request):
    if request.method == "POST":
        id = request.POST.get('voting_id')
        if not id:
            return HttpResponseBadRequest("Bad Request: No ID provided.")
        instance = get_object_or_404(EventVotingSettings, id=id)
        instance.delete()
        messages.success(request, "Deleted Successfully!")
        return redirect('dashboard:voting_list')
    else:
        return redirect('dashboard:voting_list')


'''Voting user'''
## Voting List View
class VotingUserListView(generic.ListView):
    model = UserEventVoting
    template_name ='dashboard/voting/votinguser_list.html'
    context_object_name ='votinguser'
    # paginate_by = 10 # Default items per page

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
        
    #     # Get the number of items per page from the request, default to paginate_by
    #     per_page = int(self.request.GET.get('per_page', self.paginate_by))
        
    #     paginator = Paginator(self.get_queryset(), per_page)
    #     page_number = self.request.GET.get('page')
    #     page_obj = paginator.get_page(page_number)

    #     context['page_obj'] = page_obj
    #     context['per_page'] = per_page
        
    #     return context

    # def get_queryset(self):
    #     # Get distinct event names and their associated UserEventVoting
    #     return UserEventVoting.objects.values('event__event_name').distinct()

# def voting_event_list(request):
#     distinct_events = UserEventVoting.objects.values('event').distinct()  # Get distinct events
#     context = {
#         'distinct_events': distinct_events,
#     }
#     return render(request, 'dashboard/voting/votinguser_list.html', context)

## voting Create views
class VotingUserCreateView(generic.CreateView):
    model = UserEventVoting
    template_name ='dashboard/voting/create_votinguser.html'
    form_class = VotingUserForm

    def get_success_url(self) -> str:
        messages.success(self.request,"New voting added successfully !")
        return reverse_lazy("dashboard:votinguser_list")

## Event category Update View
class VotingUserUpdateDetailView(generic.UpdateView):
    model = UserEventVoting
    template_name ='dashboard/voting/create_votinguser.html'
    context_object_name ='votinguser'
    pk_url_kwarg ='id'
    form_class = VotingUserForm
    
    def get_success_url(self):
        messages.success(self.request,'Updated Successfully !')
        return reverse('dashboard:votinguser_list')

## Event category delete view
def VotingUserdelete(request):
    if request.method == "POST":
        id = request.POST.get('votinguser_id')
        if not id:
            return HttpResponseBadRequest("Bad Request: No ID provided.")
        instance = get_object_or_404(UserEventVoting, id=id)
        instance.delete()
        messages.success(request, "Deleted Successfully!")
        return redirect('dashboard:votinguser_list')
    else:
        return redirect('dashboard:votinguser_list')


## Detail view to display detail of the event user for voting
class VotingDetailView(DetailView):
    model = Event
    template_name = 'dashboard/voting/votinguser_detail.html'
    context_object_name = 'event'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_votes'] = UserEventVoting.objects.filter(event=self.object).select_related('user')
        return context

def add_voting_user(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    if request.method == 'POST':
        form = VotingUserForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            voting_id = form.cleaned_data['voting_id']
            
            # Check if this user already has a voting ID for this event
            if UserEventVoting.objects.filter(event=event, user=user).exists():
                messages.error(request, 'This user already has a voting ID for this event.')
            else:
                try:
                    UserEventVoting.objects.create(event=event, user=user, voting_id=voting_id)
                    messages.success(request, 'Voting User added successfully.')
                    return redirect('dashboard:voting_detail', pk=event.id)
                except IntegrityError:
                    messages.error(request, 'This voting ID is already in use for this event.')
    else:
        form = VotingUserForm()
    
    # Get list of users who don't have a voting ID for this event
    existing_users = UserEventVoting.objects.filter(event=event).values_list('user', flat=True)
    available_users = User.objects.exclude(id__in=existing_users)
    
    context = {
        'form': form,
        'event': event,
        'available_users': available_users,
    }
    return render(request, 'dashboard/voting/create_votinguserevent.html', context)

class UpdateVotingUserDetailView(UpdateView):
    model = UserEventVoting
    form_class = VotingUserForm
    template_name = 'dashboard/voting/update_votinguserevent.html'
    
    def get_success_url(self):
        return reverse_lazy('dashboard:voting_detail', kwargs={'pk': self.object.event.id})

    def form_valid(self, form):
        messages.success(self.request, 'Voting User updated successfully.')
        return super().form_valid(form)


class DeleteVotingUserDetailView(DeleteView):
    model = UserEventVoting
    template_name = 'dashboard/voting/delete_votinguserevent.html'
    
    def get_success_url(self):
        return reverse_lazy('dashboard:voting_detail', kwargs={'pk': self.object.event.id})

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Voting User deleted successfully.')
        return super().delete(request, *args, **kwargs)


# Organization detail
def organizationSettings(request):
    try:
        instance = OrganizationSetting.objects.first()
    except OrganizationSetting.DoesNotExist:
        instance = None

    if request.method == 'POST':
        form = OrganizationSettingForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            if instance:
                messages.success(request, 'OrganizationSetting edited successfully.')
            else:
                messages.success(request, 'OrganizationSetting added successfully.')
            return redirect('dashboard:company_detail')
        else:
            messages.warning(request, 'Form is not valid. Please correct the errors.')
    else:
        form = OrganizationSettingForm(instance=instance)

    context = {'form': form, 'instance': instance}
    return render(request, 'dashboard/organization/organizationDetail_create.html', context)


'''Video View'''
## Video List View
class VideoListView(generic.ListView):
    model = VideoMenu
    template_name ='dashboard/video/video_list.html'
    context_object_name ='videos'

    

## Video Create views
class VideoCreateView(generic.CreateView):
    model = VideoMenu
    template_name ='dashboard/video/create_video.html'
    form_class = VideoMenuForm

    def get_success_url(self) -> str:
        messages.success(self.request,"New Video image added successfully !")
        return reverse_lazy("dashboard:video_list")

## Video Update View
class VideoUpdateDetailView(generic.UpdateView):
    model = VideoMenu
    template_name ='dashboard/video/create_video.html'
    context_object_name ='videos'
    pk_url_kwarg ='id'
    form_class = VideoMenuForm
    
    def get_success_url(self):
        messages.success(self.request,'Updated Successfully !')
        return reverse('dashboard:video_list')

## Video delete view
def Videodelete(request):
    if request.method == "POST":
        id = request.POST.get('video_id')
        if not id:
            return HttpResponseBadRequest("Bad Request: No ID provided.")
        instance = get_object_or_404(VideoMenu, id=id)
        instance.delete()
        messages.success(request, "Deleted Successfully!")
        return redirect('dashboard:video_list')
    else:
        return redirect('dashboard:video_list')


'''Album View'''
## Album List View
class AlbumListView(generic.ListView):
    model = Album
    template_name ='dashboard/album/album_list.html'
    context_object_name ='albums'


## Album create and edit view
def create_or_edit_album(request, album_id=None):
    if album_id:
        album_instance = get_object_or_404(Album, id=album_id)
        AlbumImageFormSet = inlineformset_factory(Album, AlbumImage, form=AlbumImageForm, extra=1)
    else:
        album_instance = Album()
        AlbumImageFormSet = inlineformset_factory(Album, AlbumImage, form=AlbumImageForm, extra=1)
    if request.method == 'POST':
        album_form = AlbumForm(request.POST, request.FILES, instance=album_instance)
        formset = AlbumImageFormSet(request.POST, request.FILES, instance=album_instance)
        if album_form.is_valid() and formset.is_valid():
            album_instance = album_form.save()
            formset.instance = album_instance
            formset.save()
            if album_id:
                messages.success(request, 'Album Updated successfully.')
                return redirect('dashboard:edit_Album', album_id=album_instance.id)
            else:
                messages.success(request, 'Album added successfully.')
                return redirect('dashboard:album_list')
    else:
        album_form = AlbumForm(instance=album_instance)
        formset = AlbumImageFormSet(instance=album_instance)
    context = {
        'album_form': album_form,
        'formset': formset,
        'is_inline_formset_used': True,
    }
    return render(request, 'dashboard/album/create_album.html', context)



## Album delete view
def Albumdelete(request):
    if request.method == "POST":
        id = request.POST.get('album_id')
        if not id:
            return HttpResponseBadRequest("Bad Request: No ID provided.")
        instance = get_object_or_404(Album, id=id)
        instance.delete()
        messages.success(request, "Deleted Successfully!")
        return redirect('dashboard:album_list')
    else:
        return redirect('dashboard:album_list')


#Privacy and policy section

class PrivacyListView(generic.ListView):
    model = PrivacyAndPolicy
    context_object_name = 'privacy'
    template_name = 'dashboard/privacyAndPolicy/privacy.html'

def PolicyAndPrivacy(request):
    instance = None
    try:
        if id:
            instance = PrivacyAndPolicy.objects.first()
    except Exception as e:
        messages.warning(request, 'An error occurred while retrieving the privacy and policy.')
        return redirect('dashboard:add_PolicyAndPrivacy')
    if request.method == 'POST':
        form = PrivacyAndPolicyForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            if instance:  # Edit operation
                messages.success(request, 'PrivacyAndPolicy edited successfully.')
                return redirect('dashboard:privacy')  # Redirect to the edited PrivacyAndPolicy's details page
            else:  # Add operation
                messages.success(request, 'PrivacyAndPolicy added successfully.')
                return redirect('dashboard:privacy')  # Redirect to the page for adding new PrivacyAndPolicy
        else:
            messages.warning(request, 'Form is not valid. Please correct the errors.')
    else:
        form = PrivacyAndPolicyForm(instance=instance)
    context = {'form': form, 'instance': instance}
    return render(request, 'dashboard/privacyAndPolicy/create_privacy.html', context)


# Terms and condition section

class TermsListView(generic.ListView):
    model = TermsAndCondition
    context_object_name = 'terms'
    template_name = 'dashboard/termsAndCondition/terms.html'

def TermssAndCondition(request):
    instance = None
    try:
        if id:
            instance = TermsAndCondition.objects.first()
    except Exception as e:
        messages.warning(request, 'An error occurred while retrieving the Terms And Condition.')
        return redirect('dashboard:add_TermsAndCondition')
    if request.method == 'POST':
        form = TermsAndConditionForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            if instance:  # Edit operation
                messages.success(request, 'TermsAndCondition edited successfully.')
                return redirect('dashboard:add_TermsAndCondition')  # Redirect to the edited TermsAndCondition's details page
            else:  # Add operation
                messages.success(request, 'TermsAndCondition added successfully.')
                return redirect('dashboard:terms')  # Redirect to the page for adding new TermsAndCondition
        else:
            messages.warning(request, 'Form is not valid. Please correct the errors.')
    else:
        form = TermsAndConditionForm(instance=instance)
    context = {'form': form, 'instance': instance}
    return render(request, 'dashboard/termsAndCondition/create_terms.html', context)


##Vote score
def event_list(request):
    events = Event.objects.all().order_by('-id')
    per_page = request.GET.get('per_page', 10)  # Default to 10 items per page
    paginator = Paginator(events, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    for event in page_obj:
        event.total_amount = VoteScore.objects.filter(event=event).aggregate(Sum('amount'))['amount__sum'] or 0
        
    context = {
        'events': page_obj,
        'page_obj': page_obj,
        'per_page': per_page,
    }
    
    return render(request, 'dashboard/voteScore/event_vote_list.html', context)

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    user_votes = UserEventVoting.objects.filter(event=event).select_related('user')
    
    vote_data = []
    for user_vote in user_votes:
        vote_score = VoteScore.objects.filter(event=event, user_event_voting=user_vote).first()
        if vote_score:
            vote_data.append({
                'user_name': user_vote.user.name,
                'voting_id': user_vote.voting_id,
                'vote_count': vote_score.vote_count,
                'amount': vote_score.amount,
            })

    total_amount = VoteScore.objects.filter(event=event).aggregate(Sum('amount'))['amount__sum'] or 0

    context = {
        'event': event,
        'vote_data': vote_data,
        'total_amount': total_amount,
    }
    return render(request, 'dashboard/voteScore/vote_score.html', context)


### User list
class UserListView(generic.ListView):
    model = User
    context_object_name = 'users'
    template_name = 'dashboard/user/user.html'


### Logout
@login_required
def userlogout(request):
    auth.logout(request)
    messages.info(request,"logout successfully..")
    return redirect('dashboard:login')

### Login
def login(request):
    if request.user.is_authenticated:
        if request.user.is_admin:
            return redirect('dashboard:index')
        else:
            auth.logout(request)
            messages.warning(request, "You don't have permission to access the dashboard.")
    
    if request.method == "POST":
        login_form = UserLoginForm(request.POST)
        remember_me = request.POST.get('remember_me', False)
        if login_form.is_valid():
            email = login_form.cleaned_data['email']
            password = login_form.cleaned_data['password']
            user_obj = auth.authenticate(request, email=email, password=password)

            if user_obj is not None:
                if user_obj.is_admin:
                    auth.login(request, user_obj)

                    if remember_me:
                        request.session.set_expiry(settings.SESSION_COOKIE_AGE)
                    else:
                        request.session.set_expiry(0)

                    messages.success(request, "Login successful!")
                    return redirect("dashboard:index")
                else:
                    messages.warning(request, "You don't have permission to access the dashboard.")
            else:
                messages.warning(request, "Invalid email or password.")
        else:
            messages.warning(request, "Invalid form data. Please try again.")
    
    else:
        login_form = UserLoginForm()

    return render(request, "dashboard/login/login.html", {'user_login_form': login_form})

### Change password
@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Your password was successfully updated!')
            return redirect('dashboard:login')
        else:
            messages.error(request, form.errors)
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'dashboard/login/change_password.html', {'form': form})








