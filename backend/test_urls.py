import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

print("Testing imports...")

try:
    from apps.treks.urls import urlpatterns as trek_urls
    print("✅ apps.treks.urls imported successfully")
    print(f"   Trek URLs: {trek_urls}")
except Exception as e:
    print(f"❌ Error importing apps.treks.urls: {e}")

try:
    from apps.treks.views import TrekViewSet
    print("✅ TrekViewSet imported successfully")
except Exception as e:
    print(f"❌ Error importing TrekViewSet: {e}")

try:
    from apps.treks.models import Trek
    print(f"✅ Trek model imported successfully, count: {Trek.objects.count()}")
except Exception as e:
    print(f"❌ Error importing Trek model: {e}")

print("\nIf you see ❌ above, that's what needs to be fixed!")