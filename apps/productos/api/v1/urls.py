from rest_framework.routers import DefaultRouter
from .views import ProductoViewSet
router=DefaultRouter()
router.register('productos', ProductoViewSet)
urlpatterns=router.urls
