from django.core.management.base import BaseCommand
from django.db import transaction
from properties.models import Property, Location, Amenity, Image
from django.conf import settings
import os
import shutil
import psycopg2

class Command(BaseCommand):
    help = 'Migrate data from Scrapy PostgreSQL database to Django'

    def handle(self, *args, **kwargs):
        # Connect to the Scrapy PostgreSQL database
        conn = psycopg2.connect(service='scrapy_db')
        cur = conn.cursor()

        # Fetch all hotels from Scrapy database
        cur.execute("SELECT * FROM hotels")
        hotels = cur.fetchall()

        # Define the source and destination directories
        scrapy_image_dir = '/home/w3e63/Desktop/w3 assignment/scrapy-crawl/Scrapy-assignment/images'
        django_media_root = settings.MEDIA_ROOT

        with transaction.atomic():
            for hotel in hotels:
                hotelId, hotelName, description, lat, lon, rating, amenities_str, images_str, address, city_name = hotel

                # Create or get the city location
                city, _ = Location.objects.get_or_create(
                    name=city_name,
                    type='city',
                    defaults={'latitude': lat, 'longitude': lon}
                )

                # Create the property, using hotel_id as the primary key
                property, created = Property.objects.update_or_create(
                    property_id=hotelId,
                    defaults={
                        'title': hotelName,
                        'description': description
                    }
                )
                property.locations.add(city)

                # Add amenities
                if amenities_str:
                    amenities = [a.strip() for a in amenities_str.split(',') if a.strip()]
                    for amenity_name in amenities:
                        amenity, _ = Amenity.objects.get_or_create(name=amenity_name)
                        property.amenities.add(amenity)

                # Add images
                if images_str:
                    images = [img.strip() for img in images_str.split(',') if img.strip()]
                    for image_path in images:
                        # Construct the full source path
                        source_path = os.path.join(scrapy_image_dir, image_path)
                        
                        # Construct the destination path
                        rel_path = os.path.join('properties', image_path)
                        dest_path = os.path.join(django_media_root, rel_path)
                        
                        # Ensure the destination directory exists
                        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                        
                        # Copy the image file
                        if os.path.exists(source_path):
                            shutil.copy2(source_path, dest_path)
                        
                            # Create the Image object with the relative path
                            Image.objects.get_or_create(property=property, image=rel_path)
                        else:
                            self.stdout.write(self.style.WARNING(f'Image not found: {source_path}'))

        cur.close()
        conn.close()

        self.stdout.write(self.style.SUCCESS('Successfully migrated data from Scrapy to Django'))