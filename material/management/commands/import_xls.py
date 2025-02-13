import pandas as pd
from django.core.management.base import BaseCommand
from ...models import MainCategory, SubCategory

class Command(BaseCommand):
    help = 'Import data from an .xlsx file into the database'

    def handle(self, *args, **kwargs):
        # Path to your .xls file
        file_path = 'D:\Downloads\Processed_LINE_BLANKS.xlsx'

        # Read the .xls file
        df = pd.read_excel(file_path)

        # Iterate over the rows and insert data into the database
        for index, row in df.iterrows():
            main_category_name = row['Material_Type']  # Replace with actual column name from your file
            subcategory_product = row['PRODUCT']  # Replace with actual column name
            subcategory_type = row['TYPE']  # Replace with actual column name
            subcategory_size = row['SIZE']  # Replace with actual column name
            subcategory_class = row['CLASS']  # Replace with actual column name
            subcategory_face_type = row['FACE TYPE']  # Replace with actual column name

            # Check if the MainCategory exists, otherwise create it
            main_category, created = MainCategory.objects.get_or_create(name=main_category_name)

            # Create the SubCategory
            SubCategory.objects.create(
                main_category=main_category,
                product=subcategory_product,
                type=subcategory_type,
                size=subcategory_size,
                class_field=subcategory_class,
                face_type=subcategory_face_type
            )

        self.stdout.write(self.style.SUCCESS('Data imported successfully!'))
