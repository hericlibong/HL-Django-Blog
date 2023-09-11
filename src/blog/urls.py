
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from authentication.views import LoginPageView, logout_user, signup_page, sucess_connexion, upload_profile_photo
from posts.views import BlogHome, BlogPostCreate, BlogPostUpdate, BlogPostDetail, BlogPostDelete,  AdCommentPostView, BlogPostByCategory
from blog import settings
#from froala_editor import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', BlogHome.as_view(), name = 'home'),
    path('categorie/', BlogPostByCategory.as_view(), name = 'order_category'),
    path('create/', BlogPostCreate.as_view(), name = 'create'),
    path('edit/<str:slug>/', BlogPostUpdate.as_view(), name = 'edit'),
    path('blog/<str:slug>/', BlogPostDetail.as_view(), name = 'post'),
    path('comment/<str:slug>/', AdCommentPostView.as_view(), name = 'post_comment'),
    path('delete/<str:slug>/', BlogPostDelete.as_view(), name = 'delete'),
   
    
    
    
    path('', LoginPageView.as_view(), name ='login'),
    path('signup/', signup_page, name ='signup'),
    path('success/', sucess_connexion, name ='success'),
    path('profile/photo/', upload_profile_photo, name = 'profile-photo'),
    
    path('logout/', logout_user, name = 'logout'),
    #path('froala_editor/',include('froala_editor.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
