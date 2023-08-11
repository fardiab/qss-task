from django.shortcuts import render
import pandas as pd
from django.http import JsonResponse
from csv import DictReader 
from django.db import transaction
import os
from .models import Sect, SubSect, Indica, Country

def all(request):
    # data = pd.read_csv('data/KPI tracking - KPIs from theglobaleconomy.csv')
    data = pd.read_csv('data/updated_searchart_data.csv')





    # subsectors = data[['Sector', 'Subsector']].drop_duplicates()

    # # Create and save instances of SubSect model for each subsector
    # for _, row in subsectors.iterrows():
    #     sector_name = row['Sector']
    #     subsector_name = row['Subsector']

    #     # Get the corresponding Sect instance
    #     sector = Sect.objects.get(sector=sector_name)

    #     # Create and save the SubSect instance with the related sector
    #     subsect = SubSect.objects.create(sector=sector, subsector=subsector_name)
    #     subsect.save()



    # Extract unique indicators
    # indicators = data[['Sector', 'Subsector', 'Indicator']].drop_duplicates()

    # # Create and save instances of Indica model for each indicator
    # for _, row in indicators.iterrows():
    #     sector_name = row['Sector']
    #     subsector_name = row['Subsector']
    #     indicator_name = row['Indicator']

    #     # Get the corresponding SubSect instance
    #     subsect = SubSect.objects.get(sector__sector=sector_name, subsector=subsector_name)

    #     # Create and save the Indica instance with the related subsector and indicator names
    #     indica = Indica.objects.create(subsector=subsect, indicator=indicator_name)
    #     indica.save()




    # Extract unique sectors
    # amounts = data['Sector'].unique()
    
    # # Create and save instances of Sect model for each sector
    # for sector in amounts:
    #     date = Sect.objects.create(sector=sector)
    #     date.save()




    # csv_file_path = 'data/updated_searchart_data.csv'
    # batch_size = 5000  # Define the batch size according to your needs

    # with pd.read_csv(csv_file_path, chunksize=batch_size) as reader:
    #     year_instances = []
    #     for chunk in reader:
    #         for _, row in chunk.iterrows():
    #             indicator_name = row['Indicator']
    #             country_name = row['Country']
    #             country_code2 = row['Country_code_2']
    #             country_code = row['Country_code']
    #             rank = row['Rank']
    #             amount = row['Amount']
    #             year = row['Year']
    
    #             # Get the corresponding Country instance
    #             indicator = Indica.objects.get(indicator=indicator_name) if indicator_name else None
    
    #             # Create the Year instance with the related indicator and year value
    #             year_instance = Country(indicator=indicator, year=year, rank=rank, amount=amount, country=country_name, country_code=country_code, country_code2=country_code2)
    #             year_instances.append(year_instance)
    
    #         # Bulk create Year instances for each chunk
    #         Country.objects.bulk_create(year_instances)
    #         year_instances = []  # Reset the list for the next chunk



    # subsectors = data[['Subsector', "Indicator", "Description"]].drop_duplicates()

    # for _, row in subsectors.iterrows():
    #     subsector_name = row['Subsector'].strip()  # Remove leading/trailing whitespaces if needed
    #     content = row['Description']
    #     indicator_name = row['Indicator']

    #     try:
    #         subsect = SubSect.objects.get(subsector=subsector_name)
    #     except SubSect.DoesNotExist:
    #         print(f"Subsector '{subsector_name}' does not exist in the database.")
    #         continue

    #     # Use bulk_create to insert the data into the Indica model in one query
    #     indica = Indica.objects.create(subsector=subsect, indicator=indicator_name, content=content)
    #     indica.save()


    # description_csv_file = 'data/KPI tracking - KPIs from theglobaleconomy.csv'
    # data = pd.read_csv('data/MergedDataset.csv')
    # content_data = pd.read_csv('data/KPI tracking - KPIs from theglobaleconomy.csv', usecols=['Description', 'Indicator'])
    # content_data['Indicator'] = content_data['Indicator'].str.replace(",", "")

    # # Update descriptions for existing indicators in the Indica model
    # for _, row in content_data.iterrows():
    #     indicator_name = row['Indicator']
    #     description = row['Description']

    #     if indicator_name == "Other":
    #         continue

    #     try:
    #         indica = Indica.objects.get(indicator=indicator_name)
    #         indica.content = description
    #         indica.save()
    #         print(f"Indicator '{indicator_name}' updated successfully.")
    #     except Indica.DoesNotExist:
    #         print(f"Indicator '{indicator_name}' does not exist in the database.")
    #         continue



    # indicators_without_description = Indica.objects.filter(content__isnull=True)
    # indicator_with_description = Indica.objects.filter(content__isnull=False)

    # # Print the names of indicators without descriptions
    # for indicator in indicators_without_description:
    #     print({"Not full of ":  indicator})

    # for indicator in indicator_with_description:
    #     print({"full of ": indicator})

    # sectors = Sect.objects.all()

    # for sector in sectors:
    #     # Assuming the sector name is used as the filename for the corresponding image
    #     filename = sector.sector + ".jpeg"  # Replace '.jpg' with the actual image extension

    #     # Assuming your images are stored in a directory named 'sector_images' within the 'media' folder
    #     image_path = f'images\{filename}'

    #     if os.path.exists(image_path):
    #         # Open the image file and associate it with the sector
    #         with open(image_path, 'rb') as image_file:
    #             sector.image.save(filename, image_file, save=True)

    #         print(f"Image associated with sector: {sector.sector}")
    #     else:
    #         print(f"Image not found for sector: {sector.sector}")

    return render(request, 'first_page.html')
    




