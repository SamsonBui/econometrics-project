#!/usr/bin/env python3
"""
Neighborhood-Level Airbnb Data Integration Script
==================================================
This script integrates Airbnb listings data with demographic, rent, housing,
and tourism data to create a complete neighborhood-level dataset for econometric analysis.

Combines functionality from all data collection rounds into a single script.

Author: Econometrics Project
Date: 2025-11-15
"""

import pandas as pd
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')


def standardize_text(text):
    """
    Standardize text: lowercase, strip whitespace, collapse multiple spaces.
    
    Parameters:
    -----------
    text : str
        Input text to standardize
        
    Returns:
    --------
    str
        Standardized text
    """
    if pd.isna(text):
        return text
    text = str(text).lower().strip()
    while '  ' in text:
        text = text.replace('  ', ' ')
    return text


def load_and_process_airbnb_file(file_path, city_name):
    """
    Load a single Airbnb listings file and count listings per neighborhood.
    
    Parameters:
    -----------
    file_path : str
        Path to Airbnb CSV file
    city_name : str
        Name of the city
        
    Returns:
    --------
    pd.DataFrame
        DataFrame with columns: city, neighborhood, airbnb_count
    """
    print(f"\nProcessing: {city_name}")
    print(f"   File: {Path(file_path).name}")
    
    df = pd.read_csv(file_path, low_memory=False)
    print(f"   + Loaded {len(df):,} listings")
    
    # Detect neighborhood column
    if 'neighbourhood_cleansed' in df.columns:
        neighborhood_col = 'neighbourhood_cleansed'
    elif 'neighbourhood' in df.columns:
        neighborhood_col = 'neighbourhood'
    else:
        raise ValueError(f"No neighborhood column found in {file_path}")
    
    print(f"   + Using column: {neighborhood_col}")
    
    # Extract neighborhood and standardize
    df_clean = df[[neighborhood_col]].copy()
    df_clean.columns = ['neighborhood']
    df_clean['neighborhood'] = df_clean['neighborhood'].apply(standardize_text)
    
    # Remove missing neighborhoods
    df_clean = df_clean.dropna(subset=['neighborhood'])
    
    # Count listings per neighborhood
    neighborhood_counts = df_clean.groupby('neighborhood').size().reset_index(name='airbnb_count')
    
    # Add city column
    neighborhood_counts['city'] = standardize_text(city_name)
    
    # Reorder columns
    neighborhood_counts = neighborhood_counts[['city', 'neighborhood', 'airbnb_count']]
    
    print(f"   + Found {len(neighborhood_counts)} unique neighborhoods")
    print(f"   + Total listings: {neighborhood_counts['airbnb_count'].sum():,}")
    
    return neighborhood_counts


def load_all_airbnb_data(airbnb_files):
    """
    Load and process all Airbnb listing files.
    
    Parameters:
    -----------
    airbnb_files : dict
        Dictionary mapping city names to file paths
        
    Returns:
    --------
    pd.DataFrame
        Combined neighborhood-level Airbnb data
    """
    print("\n" + "="*80)
    print("STEP 1: LOADING AIRBNB DATA (NEIGHBORHOOD LEVEL)")
    print("="*80)
    
    all_neighborhoods = []
    
    for city_name, file_path in airbnb_files.items():
        df = load_and_process_airbnb_file(file_path, city_name)
        all_neighborhoods.append(df)
    
    # Combine all neighborhoods
    airbnb_neighborhoods = pd.concat(all_neighborhoods, ignore_index=True)
    
    print("\n" + "-"*80)
    print("AIRBNB DATA SUMMARY:")
    print("-"*80)
    print(f"Total neighborhoods: {len(airbnb_neighborhoods)}")
    print(f"Total listings: {airbnb_neighborhoods['airbnb_count'].sum():,}")
    print(f"\nNeighborhoods by city:")
    city_counts = airbnb_neighborhoods.groupby('city').size()
    for city, count in city_counts.items():
        print(f"  {city:20s}: {count:3d} neighborhoods")
    
    return airbnb_neighborhoods


def load_supplementary_data(base_path):
    """
    Load all supplementary data files (demographics, rent, housing, tourism).
    
    Parameters:
    -----------
    base_path : str
        Base path to data directory
        
    Returns:
    --------
    tuple
        (demographics_df, rent_df, housing_df, tourism_df)
    """
    print("\n" + "="*80)
    print("STEP 2: LOADING SUPPLEMENTARY DATA")
    print("="*80)
    
    # Load demographics
    print("\nMerging: Loading demographics data...")
    demographics_path = f"{base_path}/Census Demographics/neighborhood_demographics_acs_2023.csv"
    demographics_df = pd.read_csv(demographics_path)
    demographics_df['city'] = demographics_df['city'].apply(standardize_text)
    demographics_df['neighborhood'] = demographics_df['neighborhood'].apply(standardize_text)
    print(f"   + Loaded {len(demographics_df)} demographic records")
    
    # Load rent data
    print("\nMerging: Loading rent data...")
    rent_path = f"{base_path}/Rent Data/neighborhood_median_rent_2024.csv"
    rent_df = pd.read_csv(rent_path)
    rent_df['city'] = rent_df['city'].apply(standardize_text)
    rent_df['neighborhood'] = rent_df['neighborhood'].apply(standardize_text)
    print(f"   + Loaded {len(rent_df)} rent records")
    
    # Load housing units
    print("\nMerging: Loading housing units data...")
    housing_path = f"{base_path}/Housing Units/neighborhood_housing_units.csv"
    housing_df = pd.read_csv(housing_path)
    housing_df['city'] = housing_df['city'].apply(standardize_text)
    housing_df['neighborhood'] = housing_df['neighborhood'].apply(standardize_text)
    print(f"   + Loaded {len(housing_df)} housing records")
    
    # Load tourism classification
    print("\nMerging: Loading tourism classification data...")
    tourism_path = f"{base_path}/Tourist Area Indicator/neighborhood_tourist_classification.csv"
    tourism_df = pd.read_csv(tourism_path)
    tourism_df['city'] = tourism_df['city'].apply(standardize_text)
    tourism_df['neighborhood'] = tourism_df['neighborhood'].apply(standardize_text)
    print(f"   + Loaded {len(tourism_df)} tourism records")
    
    return demographics_df, rent_df, housing_df, tourism_df


def merge_all_datasets(airbnb_df, demographics_df, rent_df, housing_df, tourism_df):
    """
    Merge all datasets at neighborhood level.
    
    Parameters:
    -----------
    airbnb_df : pd.DataFrame
        Airbnb neighborhood data
    demographics_df : pd.DataFrame
        Demographics data
    rent_df : pd.DataFrame
        Rent data
    housing_df : pd.DataFrame
        Housing units data
    tourism_df : pd.DataFrame
        Tourism data
        
    Returns:
    --------
    pd.DataFrame
        Merged neighborhood-level dataset
    """
    print("\n" + "="*80)
    print("STEP 3: MERGING ALL DATASETS")
    print("="*80)
    
    # Start with Airbnb data
    merged = airbnb_df.copy()
    print(f"\n+ Starting with Airbnb data: {len(merged)} neighborhoods")
    
    # Merge demographics
    print(f"\nMerging: Merging demographics...")
    merged = merged.merge(
        demographics_df, 
        on=['city', 'neighborhood'], 
        how='left'
    )
    matched = merged['median_household_income'].notna().sum()
    print(f"   + Matched: {matched}/{len(merged)} neighborhoods")
    
    # Merge rent
    print(f"\nMerging: Merging rent data...")
    merged = merged.merge(
        rent_df, 
        on=['city', 'neighborhood'], 
        how='left',
        suffixes=('', '_rent')
    )
    # Use rent file data if both exist
    if 'median_rent_rent' in merged.columns:
        merged['median_rent'] = merged['median_rent_rent'].fillna(merged.get('median_rent', np.nan))
        merged = merged.drop(columns=['median_rent_rent'])
    matched = merged['median_rent'].notna().sum()
    print(f"   + Matched: {matched}/{len(merged)} neighborhoods")
    
    # Merge housing units
    print(f"\nMerging: Merging housing units...")
    merged = merged.merge(
        housing_df, 
        on=['city', 'neighborhood'], 
        how='left',
        suffixes=('', '_housing')
    )
    # Use housing file data if both exist
    if 'housing_units_housing' in merged.columns:
        merged['housing_units'] = merged['housing_units_housing'].fillna(merged.get('housing_units', np.nan))
        merged = merged.drop(columns=['housing_units_housing'])
    matched = merged['housing_units'].notna().sum()
    print(f"   + Matched: {matched}/{len(merged)} neighborhoods")
    
    # Merge tourism
    print(f"\nMerging: Merging tourism data...")
    merged = merged.merge(
        tourism_df, 
        on=['city', 'neighborhood'], 
        how='left',
        suffixes=('', '_tourism')
    )
    # Use tourism file data if both exist
    if 'tourist_area_tourism' in merged.columns:
        merged['tourist_area'] = merged['tourist_area_tourism'].fillna(merged.get('tourist_area', np.nan))
        merged = merged.drop(columns=['tourist_area_tourism'])
    matched = merged['tourist_area'].notna().sum()
    print(f"   + Matched: {matched}/{len(merged)} neighborhoods")
    
    print(f"\n+ Final merged dataset: {len(merged)} neighborhoods")
    
    return merged


def compute_derived_variables(df):
    """
    Compute derived analysis variables.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Merged dataset
        
    Returns:
    --------
    pd.DataFrame
        Dataset with computed variables
    """
    print("\n" + "="*80)
    print("STEP 4: COMPUTING DERIVED VARIABLES")
    print("="*80)
    
    df = df.copy()
    
    # Compute airbnb_density
    print("\nComputing: airbnb_density = airbnb_count / housing_units")
    df['airbnb_density'] = np.where(
        df['housing_units'].notna() & (df['housing_units'] > 0),
        df['airbnb_count'] / df['housing_units'],
        np.nan
    )
    valid = df['airbnb_density'].notna().sum()
    print(f"   + Valid values: {valid}/{len(df)}")
    
    # Compute log_rent
    print("\nComputing: log_rent = log(median_rent)")
    df['log_rent'] = np.where(
        df['median_rent'].notna() & (df['median_rent'] > 0),
        np.log(df['median_rent']),
        np.nan
    )
    valid = df['log_rent'].notna().sum()
    print(f"   + Valid values: {valid}/{len(df)}")
    
    # Compute log_income
    print("\nComputing: log_income = log(median_household_income)")
    df['log_income'] = np.where(
        df['median_household_income'].notna() & (df['median_household_income'] > 0),
        np.log(df['median_household_income']),
        np.nan
    )
    valid = df['log_income'].notna().sum()
    print(f"   + Valid values: {valid}/{len(df)}")
    
    # Compute log_airbnb_density
    print("\nComputing: log_airbnb_density = log(airbnb_density)")
    df['log_airbnb_density'] = np.where(
        df['airbnb_density'].notna() & (df['airbnb_density'] > 0),
        np.log(df['airbnb_density']),
        np.nan
    )
    valid = df['log_airbnb_density'].notna().sum()
    print(f"   + Valid values: {valid}/{len(df)}")
    
    return df


def create_final_dataset(df):
    """
    Select final columns and prepare for export.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Dataset with all variables
        
    Returns:
    --------
    pd.DataFrame
        Final dataset with selected columns
    """
    print("\n" + "="*80)
    print("STEP 5: CREATING FINAL DATASET")
    print("="*80)
    
    # Define final column order
    final_columns = [
        'city',
        'neighborhood',
        'median_rent',
        'airbnb_count',
        'housing_units',
        'airbnb_density',
        'median_household_income',
        'population_density',
        'pct_college',
        'tourist_area',
        'log_rent',
        'log_income',
        'log_airbnb_density'
    ]
    
    # Select only columns that exist
    available_columns = [col for col in final_columns if col in df.columns]
    df_final = df[available_columns].copy()
    
    print(f"\n+ Final dataset shape: {len(df_final)} neighborhoods × {len(df_final.columns)} variables")
    
    return df_final


def print_data_quality_report(df):
    """
    Print comprehensive data quality report.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Final dataset
    """
    print("\n" + "="*80)
    print("DATA QUALITY REPORT")
    print("="*80)
    
    # Basic info
    print(f"\nMerging: DATASET DIMENSIONS")
    print("-"*80)
    print(f"Neighborhoods: {len(df)}")
    print(f"Variables: {len(df.columns)}")
    print(f"Total data points: {len(df) * len(df.columns)}")
    
    # Complete neighborhoods
    complete = df.dropna(subset=['median_rent', 'housing_units', 'median_household_income'])
    print(f"\nMerging: COMPLETE NEIGHBORHOODS")
    print("-"*80)
    print(f"Neighborhoods with core variables: {len(complete)} ({len(complete)/len(df)*100:.1f}%)")
    
    # Neighborhoods per city
    print(f"\nMerging: NEIGHBORHOODS BY CITY")
    print("-"*80)
    city_counts = df.groupby('city').size().sort_values(ascending=False)
    for city, count in city_counts.items():
        complete_city = df[df['city'] == city].dropna(subset=['median_rent', 'housing_units', 'median_household_income']).shape[0]
        pct = (complete_city / count * 100) if count > 0 else 0
        print(f"  {city.title():20s}: {count:3d} total, {complete_city:3d} complete ({pct:.1f}%)")
    
    # Missing values
    print(f"\nMerging: MISSING VALUES")
    print("-"*80)
    missing = df.isnull().sum()
    missing_pct = (missing / len(df) * 100).round(1)
    
    for col in df.columns:
        miss_count = missing[col]
        miss_pct = missing_pct[col]
        status = "+" if miss_count == 0 else ("WARNING: " if miss_pct < 50 else "ERROR:")
        print(f"  {status} {col:30s}: {miss_count:4d} missing ({miss_pct:5.1f}%)")
    
    total_missing = missing.sum()
    total_cells = len(df) * len(df.columns)
    total_pct = (total_missing / total_cells * 100).round(1)
    print(f"\n  Total missing: {total_missing:,} / {total_cells:,} ({total_pct}%)")
    
    # Summary statistics
    print(f"\nMerging: SUMMARY STATISTICS")
    print("-"*80)
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    summary = df[numeric_cols].describe().round(2)
    print(summary.to_string())


def export_dataset(df, output_base_path):
    """
    Export dataset to Stata and CSV formats.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Final dataset
    output_base_path : str
        Base path for output files (without extension)
    """
    print("\n" + "="*80)
    print("STEP 6: EXPORTING DATASET")
    print("="*80)
    
    # Export to Stata
    stata_path = f"{output_base_path}.dta"
    print(f"\nExporting: Exporting to Stata format...")
    print(f"   File: {stata_path}")
    df.to_stata(stata_path, write_index=False, version=118)
    print(f"   + Stata file created!")
    
    # Export to CSV
    csv_path = f"{output_base_path}.csv"
    print(f"\nExporting: Exporting to CSV format...")
    print(f"   File: {csv_path}")
    df.to_csv(csv_path, index=False)
    print(f"   + CSV file created!")
    
    # Print file sizes
    import os
    stata_size = os.path.getsize(stata_path) / 1024
    csv_size = os.path.getsize(csv_path) / 1024
    print(f"\nFiles: File sizes:")
    print(f"   Stata: {stata_size:.1f} KB")
    print(f"   CSV:   {csv_size:.1f} KB")


def main():
    """
    Main execution function.
    """
    print("\n" + "="*80)
    print("NEIGHBORHOOD-LEVEL AIRBNB DATASET CREATION")
    print("="*80)
    print("\nThis script creates a neighborhood-level dataset by merging:")
    print("  • Airbnb listings data")
    print("  • Census demographics (ACS 2023)")
    print("  • Median rent data (2024)")
    print("  • Housing units data")
    print("  • Tourism classification")
    
    # Define file paths
    base_path = "/Users/samsonbui/Documents/EconometricsProject/data"
    
    # Airbnb files
    airbnb_files = {
        'Austin': f"{base_path}/Airbnb Listings Data/austin_listings.csv",
        'Dallas': f"{base_path}/Airbnb Listings Data/dallas_listings.csv",
        'Los Angeles': f"{base_path}/Airbnb Listings Data/los-angeles_listings.csv",
        'New York City': f"{base_path}/Airbnb Listings Data/new-york-city_listings.csv",
        'Broward County': f"{base_path}/Airbnb Listings Data/broward-county_listings.csv",
    }
    
    # Output path
    output_base = f"{base_path}/airbnb_neighborhood_panel"
    
    try:
        # Step 1: Load Airbnb data
        airbnb_df = load_all_airbnb_data(airbnb_files)
        
        # Step 2: Load supplementary data
        demographics_df, rent_df, housing_df, tourism_df = load_supplementary_data(base_path)
        
        # Step 3: Merge all datasets
        merged_df = merge_all_datasets(airbnb_df, demographics_df, rent_df, housing_df, tourism_df)
        
        # Step 4: Compute derived variables
        computed_df = compute_derived_variables(merged_df)
        
        # Step 5: Create final dataset
        final_df = create_final_dataset(computed_df)
        
        # Print data quality report
        print_data_quality_report(final_df)
        
        # Step 6: Export
        export_dataset(final_df, output_base)
        
        # Success message
        print("\n" + "="*80)
        print("+ SUCCESS!")
        print("="*80)
        complete_count = final_df.dropna(subset=['median_rent', 'housing_units', 'median_household_income']).shape[0]
        complete_pct = (complete_count / len(final_df) * 100)
        
        print(f"\nMerging: Created neighborhood-level dataset:")
        print(f"   • {len(final_df)} neighborhoods")
        print(f"   • {len(final_df.columns)} variables")
        print(f"   • {complete_count} complete neighborhoods ({complete_pct:.1f}%)")
        print(f"   • Ready for econometric analysis")
        
        print(f"\nFiles: Output files:")
        print(f"   • {output_base}.dta")
        print(f"   • {output_base}.csv")
        
    except Exception as e:
        print("\n" + "="*80)
        print("ERROR: ERROR OCCURRED")
        print("="*80)
        print(f"\nError: {str(e)}")
        import traceback
        traceback.print_exc()
        raise


if __name__ == "__main__":
    main()

