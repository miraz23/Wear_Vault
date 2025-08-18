from django.core.management.base import BaseCommand
from django.conf import settings
from shop.models import product
import os


class Command(BaseCommand):
    help = 'Migrate existing local product images to Cloudinary'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be migrated without actually doing it',
        )

    def handle(self, *args, **options):
        if not hasattr(settings, 'CLOUDINARY_STORAGE'):
            self.stdout.write(
                self.style.ERROR('Cloudinary is not configured. Please set up your .env file first.')
            )
            return

        products = product.objects.all()
        self.stdout.write(f'Found {products.count()} products to process')

        for prod in products:
            self.stdout.write(f'Processing product: {prod.product_name}')
            
            # Check each image field
            local_images_found = False
            for field_name in ['product_image_1', 'product_image_2', 'product_image_3', 'product_image_4', 'product_image_5']:
                image_field = getattr(prod, field_name)
                
                if image_field and hasattr(image_field, 'url'):
                    # Check if it's a local file
                    if image_field.url.startswith('/media/') or image_field.url.startswith('/images/'):
                        self.stdout.write(f'  - {field_name}: Local file found')
                        local_images_found = True
                    else:
                        self.stdout.write(f'  - {field_name}: Already on Cloudinary')
                else:
                    self.stdout.write(f'  - {field_name}: No image')
            
            if local_images_found and not options['dry_run']:
                try:
                    # Simply re-save the product to trigger Cloudinary upload
                    prod.save()
                    self.stdout.write(f'  ✓ Product re-saved to trigger Cloudinary upload')
                except Exception as e:
                    self.stdout.write(f'  ✗ Error saving product: {str(e)}')
            
            self.stdout.write('')

        if options['dry_run']:
            self.stdout.write(
                self.style.WARNING('Dry run completed. Use --dry-run=False to actually migrate images.')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS('Migration completed successfully!')
            ) 