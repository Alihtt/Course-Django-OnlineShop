from django.urls import path, include
from . import views

app_name = 'home'

bucket_urls = [
    path('', view=views.BucketHome.as_view(), name='bucket'),
    path('delete_obj/<str:key>/', view=views.DeleteBucketObject.as_view(),
         name='delete_obj_bucket'),
    path('download_obj/<str:key>/',
         view=views.DownloadBucketObject.as_view(), name='download_obj_bucket')
]

urlpatterns = [
    path('', view=views.HomeView.as_view(), name='home'),
    path('bucket/', include(bucket_urls)),
    path('category/<slug:category_slug>/',
         views.HomeView.as_view(), name='category_filter'),
    path('<slug:slug>/', view=views.ProductDetailView.as_view(), name='product_detail')
]
