
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from authentication.views import LoginPageView, logout_user, signup_page, sucess_connexion, upload_profile_photo
from posts.views import BlogHome, BlogPostCreate, BlogPostUpdate, BlogPostDetail, BlogPostDelete, photo_upload
from blog import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', BlogHome.as_view(), name = 'home'),
    path('create/', BlogPostCreate.as_view(), name = 'create'),
    path('edit/<str:slug>/', BlogPostUpdate.as_view(), name = 'edit'),
    path('blog/<str:slug>/', BlogPostDetail.as_view(), name = 'post'),
    path('delete/<str:slug>/', BlogPostDelete.as_view(), name = 'delete'),
    path('photo/upload/', photo_upload, name='photo_upload'),
    
    
    path('', LoginPageView.as_view(), name ='login'),
    path('signup/', signup_page, name ='signup'),
    path('success/', sucess_connexion, name ='success'),
    path('profile/photo/', upload_profile_photo, name = 'profile-photo'),
    
    path('logout/', logout_user, name = 'logout')
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
