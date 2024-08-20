import os
import shutil
import configparser
import psycopg2
from django.core.management.base import BaseCommand
from django.db import transaction
from django.conf import settings
from properties.models import Property, Location, Amenity, Image

class Command(BaseCommand):
    help = 'Migrate data from Scrapy PostgreSQL database to Django'

    def handle(self, *args, **kwargs):
        # Load configuration
        config = configparser.ConfigParser()
        config.read(os.path.expanduser('~/.pg_service.conf'))

        # Get the scrapy_image_dir from the config file
        scrapy_image_dir = config.get('scrapy_settings', 'scrapy_image_dir', fallback='')

        # Connect to the Scrapy PostgreSQL database
        conn = psycopg2.connect(service='scrapy_db')
        cur = conn.cursor()

        # Fetch all hotels from Scrapy database
        cur.execute("SELECT * FROM hotels")
        hotels = cur.fetchall()

        django_media_root = settings.MEDIA_ROOT

        with transaction.atomic():
            for hotel in hotels:
                self.process_hotel(hotel, scrapy_image_dir, django_media_root)

        cur.close()
        conn.close()

        self.stdout.write(self.style.SUCCESS('Successfully migrated data from Scrapy to Django'))

    def process_hotel(self, hotel, scrapy_image_dir, django_media_root):
        hotel_id, name, description, lat, lon, rating, amenities_str, images_str, address, city_name = hotel

        # Create or get the city location
        city, _ = Location.objects.get_or_create(
            name=city_name,
            type='city',
            defaults={'latitude': lat, 'longitude': lon}
        )

        # Create the property, using hotel_id as the primary key
        property_obj, _ = Property.objects.update_or_create(
            property_id=hotel_id,
            defaults={'title': name, 'description': description}
        )
        property_obj.locations.add(city)

        # Add amenities
        if amenities_str:
            self.add_amenities(property_obj, amenities_str)

        # Add images
        if images_str:
            self.add_images(property_obj, images_str, scrapy_image_dir, django_media_root)

    def add_amenities(self, property_obj, amenities_str):
        amenities = [a.strip() for a in amenities_str.split(',') if a.strip()]
        for amenity_name in amenities:
            amenity, _ = Amenity.objects.get_or_create(name=amenity_name)
            property_obj.amenities.add(amenity)

    def add_images(self, property_obj, images_str, scrapy_image_dir, django_media_root):
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
                Image.objects.get_or_create(property=property_obj, image=rel_path)
            else:
                self.stdout.write(self.style.WARNING(f'Image not found: {source_path}'))
