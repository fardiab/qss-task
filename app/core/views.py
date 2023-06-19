from django.shortcuts import render
import pandas as pd
from django.http import JsonResponse
from csv import DictReader 
from django.db import transaction

from .models import Sect, SubSect, Indica, Country

def all(request):
    data = pd.read_csv('data/MergedDataset.csv')

    # for _, row in data.iterrows():
    #     indicator_name = row['Indicator']
    #     year_name = row['Year']

    #     # Get the corresponding Country instance
    #     indicator = Indica.objects.get(indicator=indicator_name)

    #     # Create and save the Amount instance with the related country and amount value
    #     year_name = Year.objects.create(indicator=indicator, year=year_name)
    #     year_name.save()


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


    # csv_file_path = 'data/MergedDataset.csv'
    # batch_size = 5000  # Define the batch size according to your needs

    # with pd.read_csv(csv_file_path, chunksize=batch_size) as reader:
    #     year_instances = []
    #     for chunk in reader:
    #         for _, row in chunk.iterrows():
    #             indicator_name = row['Indicator']
    #             country_name = row['Country']
    #             rank = row['Rank']
    #             amount = row['Amount']
    #             year = row['Year']
    
    #             # Get the corresponding Country instance
    #             indicator = Indica.objects.get(indicator=indicator_name) if indicator_name else None
    
    #             # Create the Year instance with the related indicator and year value
    #             year_instance = Country(indicator=indicator, year=year, rank=rank, amount=amount, country=country_name)
    #             year_instances.append(year_instance)
    
    #         # Bulk create Year instances for each chunk
    #         Country.objects.bulk_create(year_instances)
    #         year_instances = []  # Reset the list for the next chunk
    
    return render(request, 'first_page.html')
    




