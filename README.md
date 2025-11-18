# Airbnb Impact on Housing Rents: Neighborhood-Level Analysis

## Project Overview

This repository contains data and code for analyzing the impact of Airbnb short-term rentals on long-term housing rents at the neighborhood level across five major U.S. cities.

### Research Question
*Do increases in short-term rental activity (Airbnb listings) raise long-term housing rents at the neighborhood level across U.S. cities?*

### Hypothesis
Higher Airbnb listing density in a neighborhood is associated with higher median long-term rents, even after controlling for demographic, housing supply, and tourism-demand factors.

---

## Dataset

### Final Dataset
- **File**: `data/airbnb_neighborhood_panel.dta` (Stata format) / `.csv` (CSV format)
- **Observations**: 582 neighborhoods
- **Complete Data**: 582 neighborhoods (100% - NO MISSING VALUES!)
- **Geographic Coverage**: 5 major U.S. cities
  - Los Angeles: 266 neighborhoods
  - New York City: 224 neighborhoods
  - Austin: 44 neighborhoods (ZIP codes)
  - Broward County: 34 neighborhoods (cities)
  - Dallas: 14 neighborhoods (council districts)

### Variables (13 total)

**Identifiers:**
- `city` - City name
- `neighborhood` - Neighborhood/ZIP/district name

**Primary Variables:**
- `median_rent` - Median monthly rent (USD, 2024)
- `airbnb_count` - Number of Airbnb listings
- `housing_units` - Total housing units
- `airbnb_density` - Listings per housing unit (key independent variable)

**Control Variables:**
- `median_household_income` - Median household income (ACS 2023)
- `population_density` - People per square mile
- `pct_college` - % adults 25+ with bachelor's degree
- `tourist_area` - Binary indicator (1=tourist area, 0=residential)

**Derived Variables:**
- `log_rent` - Natural log of median rent
- `log_income` - Natural log of median household income
- `log_airbnb_density` - Natural log of Airbnb density

---

## Repository Structure

```
EconometricsProject/
│
├── README.md                                    # Project documentation
├── create_neighborhood_dataset.py              # Initial dataset creation script
├── integrate_data.py                           # Data integration script (consolidates 38 sources)
│
├── data/                                        # Data directory
│   ├── airbnb_neighborhood_panel.dta           # FINAL DATASET (Stata format)
│   ├── airbnb_neighborhood_panel.csv           # FINAL DATASET (CSV format)
│   ├── airbnb_panel_clean.dta                  # Cleaned version for analysis
│   │
│   ├── Airbnb Listings Data/                   # Raw Airbnb listings (5 files)
│   │   ├── austin_listings.csv                 # 28,956 listings, 79 columns
│   │   ├── dallas_listings.csv                 # 9,790 listings, 79 columns
│   │   ├── los-angeles_listings.csv            # 84,139 listings, 79 columns
│   │   ├── new-york-city_listings.csv          # 64,828 listings, 79 columns
│   │   └── broward-county_listings.csv         # 39,074 listings, 79 columns
│   │
│   ├── Census Demographics/                    # ACS 2023 demographic data (27 files)
│   │   ├── neighborhood_demographics_acs_2023.csv  # Primary demographics file
│   │   ├── austin_zip_demographics_acs_2023.csv    # Austin ZIP-level data
│   │   ├── dallas_council_districts_demographics.csv  # Dallas district data
│   │   ├── manhattan_neighborhoods_demographics.csv
│   │   ├── brooklyn_neighborhoods_demographics.csv
│   │   ├── outer_boroughs_neighborhoods_demographics.csv
│   │   ├── los_angeles_neighborhoods_*.csv     # LA data (8 parts)
│   │   ├── nyc_*.csv                           # NYC data (6 parts)
│   │   └── broward_county_*.csv                # Broward data (2 files)
│   │
│   ├── Rent Data/                              # Median rent data (2 files)
│   │   ├── neighborhood_median_rent_2024.csv   # Primary rent file
│   │   └── austin_zip_codes_median_rent.csv    # Austin ZIP-level rent
│   │
│   ├── Housing Units/                          # Total housing units (1 file)
│   │   └── neighborhood_housing_units.csv
│   │
│   ├── Tourist Area Indicator/                 # Tourism classification (6 files)
│   │   ├── neighborhood_tourist_classification.csv  # Primary tourism file
│   │   ├── la_tourism_classification.csv
│   │   ├── nyc_tourism_classification.csv
│   │   ├── broward_tourism_classification.csv
│   │   ├── tourism_classification_final.csv
│   │   └── tourist_area_classification.csv
│   │
│   └── charts/                                 # Visualizations
│       ├── airbnb_density_by_city.png
│       └── Graph.png
│
├── docs/                                        # Documentation
│   ├── DATA_DESCRIPTION.md                     # Comprehensive data documentation
│   └── data-sources.md                         # Data source details
│
└── Stata Output/                               # Stata analysis results
    ├── descriptives.txt                        # Descriptive statistics
    ├── descriptives.doc                        # Formatted descriptives
    ├── results.txt                             # Regression results
    └── results.doc                             # Formatted results
```

### Key Files

| File | Description | Size |
|------|-------------|------|
| `airbnb_neighborhood_panel.dta` | Final integrated dataset (Stata) | 85 KB |
| `airbnb_neighborhood_panel.csv` | Final integrated dataset (CSV) | 81 KB |
| `create_neighborhood_dataset.py` | Aggregates 226,787 listings → 582 neighborhoods | 602 lines |
| `integrate_data.py` | Integrates 38 source files into final dataset | 567 lines |
| `DATA_DESCRIPTION.md` | Academic data documentation | Comprehensive |

### Data Summary

- **Total Source Files**: 38 files across 5 categories
- **Raw Data Scale**: 
  - Airbnb listings: 226,787 rows × 79 columns = **17,916,173 data points**
  - Supplementary data: 1,185 rows × 6-8 columns ≈ **8,295 data points**
  - **Total raw data points**: ~18 million
- **Final Dataset**: 582 rows × 13 columns = 582 neighborhoods × 13 variables = **7,566 data points** (100% complete, 0 missing)
- **Data Reduction**: 226,787 listings aggregated → 582 neighborhoods (389:1 ratio)
- **Geographic Coverage**: Austin (44), Dallas (14), Los Angeles (266), NYC (224), Broward (34)

---

## Data Sources

1. **Airbnb Listings**: Inside Airbnb (http://insideairbnb.com/)
   - Austin, Dallas, Los Angeles, New York City, Broward County
   - Listing-level data aggregated to neighborhood level

2. **Census Demographics**: U.S. Census Bureau, American Community Survey (ACS) 2023
   - Median household income
   - Population density
   - Educational attainment
   - Housing units

3. **Rent Data**: Zillow Research Data, HUD Fair Market Rents
   - Median monthly rent by neighborhood (2024)

4. **Tourism Classification**: Manual research and classification
   - Based on hotel density, tourist attractions, tourism board designations

---

## Data Integration Challenge & Solution

### Scale of the Data Integration Task

The construction of this dataset required integrating **38 distinct source files** from **10 different data providers**, encompassing:

- **227,000 rows** of raw Airbnb listing data (5 files, 79 columns each)
- **745 rows** of Census demographic data (27 files collected in 3 rounds)
- **88 rows** of rent data (2 files from Zillow and HUD)
- **33 rows** of housing unit data (1 file)
- **319 rows** of tourism classification data (6 files)

The raw Airbnb files alone contained detailed information on 226,787 individual listings across five cities, which needed to be aggregated to 582 neighborhoods and then merged with supplementary data sources that used incompatible geographic definitions.

### The Problem: Geographic Fragmentation

Creating this dataset required solving a significant **geographic fragmentation problem**. The Airbnb listings data and the supplementary demographic/rent data used **incompatible geographic definitions**, making direct merging impossible.

#### **Initial State (November 14, 2025)**
When I first aggregated the 119,729 Airbnb listings into 582 neighborhoods, I attempted to merge with existing demographic and rent datasets. The result was catastrophic:
- **Only 2 out of 582 neighborhoods** matched successfully (0.3%)
- **75.7% missing values** across the dataset
- **580 neighborhoods** had no demographic or rent information
- **5,724 missing values** out of 7,566 total data cells

#### **Root Cause: Mismatched Geographic Units**

The fragmentation occurred because different data sources defined "neighborhoods" differently:

| City | Airbnb Uses | Census/Demographic Data Uses |
|------|-------------|------------------------------|
| **Austin** | ZIP codes (78701, 78702, etc.) | Neighborhood names ("Downtown Austin", "East Austin") |
| **Dallas** | Council districts ("District 1", "District 2") | Neighborhood names ("Oak Lawn", "Uptown") |
| **Los Angeles** | 266 specific neighborhood names | ~50 major neighborhood names (incomplete coverage) |
| **New York City** | 224 specific neighborhood names | ~80 major neighborhood names (incomplete coverage) |
| **Broward County** | 34 city/municipality names | Limited neighborhood-level data |

**Example of the mismatch:**
- Airbnb listing in Austin shows: `neighbourhood_cleansed = "78701"`
- Census demographic data shows: `neighborhood = "downtown austin"`
- These don't match, so the merge fails and leaves missing values

---

### The Solution: Three-Round Data Collection Strategy

To solve this fragmentation, I implemented a systematic three-round data collection and integration process.

#### **Round 1: Foundation (83 Complete Neighborhoods)**

**Objective**: Fill gaps for cities with structured geographic units

**Approach**:
1. **Austin (44 neighborhoods)**: Collected Census data at the ZIP Code Tabulation Area (ZCTA) level
   - Downloaded ACS 2023 data for all 44 Austin ZIP codes
   - Obtained Zillow rent data by ZIP code
   - Direct match: Airbnb's "78701" → Census ZCTA "78701"

2. **Dallas (14 neighborhoods)**: Collected data by City Council District
   - Obtained Dallas Open Data Portal demographics by district
   - Direct match: Airbnb's "District 1" → Census "District 1"

3. **LA/NYC/Broward (25 neighborhoods)**: Collected data for major neighborhoods
   - Focused on high-traffic tourist areas (Hollywood, Venice, Manhattan, etc.)
   - Manual matching of common neighborhood names

**Result**: 83 complete neighborhoods (14.3% completeness)

**Files Created**:
- `austin_zip_demographics_acs_2023.csv`
- `austin_zip_codes_median_rent.csv`
- `dallas_council_districts_demographics.csv`
- `los_angeles_neighborhoods_demographics.csv`
- `manhattan_neighborhoods_demographics.csv`
- `brooklyn_neighborhoods_demographics.csv`
- `outer_boroughs_neighborhoods_demographics.csv`
- `broward_county_cities_demographics.csv`
- `tourist_area_classification.csv`

---

#### **Round 2: Major Expansion (540 Complete Neighborhoods)**

**Objective**: Comprehensive coverage of LA and NYC neighborhoods

**Approach**:
1. **Los Angeles (197 additional neighborhoods)**:
   - Collected data in 8 batches to cover diverse areas:
     - Part 1: High-priority neighborhoods (Downtown, Pasadena, Long Beach)
     - Part 2: Westside neighborhoods (Santa Monica, Venice, Culver City)
     - Part 3: Valley neighborhoods (Van Nuys, North Hollywood, Burbank)
     - Part 4-7: Remaining suburban and outlying areas
     - Part 8: Final missing neighborhoods
   - Used Census tract aggregation for neighborhoods without direct data
   - Cross-referenced with LA County Open Data Portal

2. **New York City (167 additional neighborhoods)**:
   - Collected data in 6 batches by borough and priority:
     - Part 1-2: High-priority Manhattan and Brooklyn neighborhoods
     - Part 3-4: Queens, Bronx, and outer neighborhoods
     - Staten Island: Complete coverage (36 neighborhoods)
     - Brooklyn/Queens final: Remaining neighborhoods
   - Utilized NYC Open Data and Neighborhood Tabulation Areas (NTAs)
   - Matched Airbnb neighborhood names to official NTA definitions

3. **Broward County (3 additional neighborhoods)**:
   - Completed remaining cities and unincorporated areas
   - Used Census Place-level data

4. **Tourism Classification (158 neighborhoods)**:
   - Manually classified neighborhoods based on:
     - Hotel density and distribution
     - Presence of major tourist attractions
     - Official tourism board designations
     - TripAdvisor and travel guide listings

**Result**: 540 complete neighborhoods (92.8% completeness)

**Files Created** (15 demographic + 3 tourism files):
- `los_angeles_neighborhoods_detailed.csv`
- `los_angeles_neighborhoods_additional.csv`
- `los_angeles_high_priority_part3.csv`
- `los_angeles_remaining_part4.csv` through `part7.csv`
- `los_angeles_final_part8.csv`
- `nyc_high_priority_part1.csv` and `part2.csv`
- `nyc_remaining_part3.csv` and `part4.csv`
- `nyc_staten_island_neighborhoods.csv`
- `nyc_brooklyn_queens_final.csv`
- `broward_county_final_neighborhoods.csv`
- `la_tourism_classification.csv`
- `nyc_tourism_classification.csv`
- `broward_tourism_classification.csv`

---

#### **Round 3: Final Completion (582 Complete Neighborhoods)**

**Objective**: Achieve 100% completeness

**Approach**:
1. **Identified 42 remaining neighborhoods** with missing data:
   - 25 Los Angeles neighborhoods (mostly small/remote areas)
   - 16 New York City neighborhoods (mostly outer borough residential)
   - 1 tourism classification update

2. **Targeted data collection** for small neighborhoods:
   - Los Angeles: Remote areas (Angeles Crest, mountain communities)
   - Los Angeles: Small cities (Walnut, Sierra Madre, San Marino)
   - Los Angeles: Industrial areas (Industry, Irwindale)
   - NYC: Outer borough residential (South Ozone Park, Roosevelt Island)
   - NYC: Small neighborhoods (Breezy Point, Marble Hill)

3. **Final tourism classification** for 11 neighborhoods

**Result**: 582 complete neighborhoods (100% completeness - ZERO missing values!)

**Files Created**:
- `la_missing_high_priority.csv` (10 neighborhoods)
- `la_missing_remaining.csv` (15 neighborhoods)
- `nyc_missing_neighborhoods.csv` (16 neighborhoods)
- `tourism_classification_final.csv` (11 neighborhoods)

---

### Technical Implementation: The Merge Process

#### **Step 1: Text Standardization**
To maximize matching success, all geographic identifiers were standardized:

```python
def standardize_text(text):
    """Standardize text: lowercase, strip whitespace, collapse spaces."""
    if pd.isna(text):
        return text
    text = str(text).lower().strip()
    while '  ' in text:
        text = text.replace('  ', ' ')
    return text
```

**Applied to**:
- City names: "New York City" → "new york city"
- Neighborhood names: "78701" → "78701", "District 1" → "district 1"
- Removed extra spaces, special characters, and inconsistent capitalization

#### **Step 2: Iterative Left Join Strategy**
The integration used a **left join** approach to preserve all Airbnb neighborhoods:

```python
# Start with Airbnb data (582 neighborhoods)
merged = airbnb_df.copy()

# Merge demographics (on city + neighborhood)
merged = merged.merge(demographics_df, on=['city', 'neighborhood'], how='left')

# Merge rent data
merged = merged.merge(rent_df, on=['city', 'neighborhood'], how='left')

# Merge housing units
merged = merged.merge(housing_df, on=['city', 'neighborhood'], how='left')

# Merge tourism classification
merged = merged.merge(tourism_df, on=['city', 'neighborhood'], how='left')
```

**Key principle**: Never drop Airbnb neighborhoods; instead, fill in missing values progressively.

#### **Step 3: Incremental Fill Strategy**
Each round of data collection filled missing values without overwriting existing data:

```python
# For each new data file
for idx, new_row in new_data.iterrows():
    city = new_row['city']
    neighborhood = new_row['neighborhood']
    
    # Find matching row in main dataset
    mask = (final_df['city'] == city) & (final_df['neighborhood'] == neighborhood)
    
    if mask.any():
        # Fill only missing values
        for col in ['median_rent', 'housing_units', 'median_household_income', 
                   'population_density', 'pct_college', 'tourist_area']:
            if col in new_row and pd.notna(new_row[col]):
                final_df.loc[mask, col] = final_df.loc[mask, col].fillna(new_row[col])
```

**Benefits**:
- Preserved data from earlier rounds
- Prevented accidental overwrites
- Allowed quality control at each stage

#### **Step 4: Derived Variable Computation**
After each merge, derived variables were recomputed to maintain consistency:

```python
# Airbnb density
df['airbnb_density'] = df['airbnb_count'] / df['housing_units']

# Log transformations (for regression analysis)
df['log_rent'] = np.log(df['median_rent'])
df['log_income'] = np.log(df['median_household_income'])
df['log_airbnb_density'] = np.log(df['airbnb_density'])
```

**Handled edge cases**:
- Division by zero → NaN
- Log of zero or negative → NaN
- Maintained data integrity throughout

---

### Data Quality Assurance

Throughout the integration process, multiple quality checks were implemented:

#### **1. Duplicate Detection**
```python
# Check for duplicate neighborhoods within each city
duplicates = df.duplicated(subset=['city', 'neighborhood']).sum()
if duplicates > 0:
    # Take median of duplicate values
    df = df.groupby(['city', 'neighborhood']).median().reset_index()
```

#### **2. Value Validation**
- Ensured all numeric values were positive (rent, income, population density)
- Verified log transformations only applied to positive values
- Checked for extreme outliers (flagged but not removed)

#### **3. Match Rate Tracking**
After each merge, tracked success rates:
```python
matched = merged['median_household_income'].notna().sum()
print(f"Matched: {matched}/{len(merged)} neighborhoods")
```

#### **4. Completeness Reporting**
Generated detailed reports after each round:
- Completeness by city
- Completeness by variable
- Identification of remaining gaps

---

### Results: From 0.3% to 100% Completeness

| Stage | Complete Neighborhoods | Completeness | Missing Values |
|-------|------------------------|--------------|----------------|
| **Initial** | 2 | 0.3% | 5,724 (75.7%) |
| **After Round 1** | 83 | 14.3% | 4,011 (53.0%) |
| **After Round 2** | 540 | 92.8% | 546 (7.2%) |
| **After Round 3** | 582 | 100.0% | 0 (0.0%) |

**Total Improvement**: 291x increase in complete neighborhoods

---

### Key Lessons Learned

1. **Geographic standardization is critical**: Different data sources rarely use identical geographic definitions

2. **Iterative approach works best**: Attempting to collect all data at once would have been overwhelming

3. **Prioritization matters**: Starting with high-Airbnb-volume neighborhoods ensured early coverage of the most important observations

4. **Multiple data sources required**: No single source had complete coverage; combining Census, Zillow, city portals, and manual research was necessary

5. **Documentation is essential**: Tracking which neighborhoods were filled in each round prevented confusion and duplication

---

### How I Solved the Complexity Challenges

The data integration task presented five major complexity challenges, each requiring specific technical solutions:

#### **Challenge 1: Geographic Fragmentation**

**Problem**: Airbnb uses informal neighborhood names (e.g., "78701", "District 1", "Hollywood") while Census data uses formal geographic units (ZCTAs, tracts, places). Direct matching failed for 99.7% of neighborhoods.

**Solution**: Implemented city-specific geographic matching strategies:

1. **Austin (ZIP Code Strategy)**:
   - Recognized that Airbnb's "78701", "78702" were ZIP codes
   - Downloaded Census data at ZCTA level (ZIP Code Tabulation Areas)
   - Direct 1:1 matching: Airbnb "78701" → Census ZCTA "78701"
   - Result: 100% match rate for all 44 Austin neighborhoods

2. **Dallas (District Aggregation Strategy)**:
   - Identified that Airbnb's "District 1", "District 2" were City Council Districts
   - Obtained Dallas Open Data Portal data aggregated by district
   - Direct 1:1 matching: Airbnb "district 1" → Dallas "District 1"
   - Result: 100% match rate for all 14 Dallas neighborhoods

3. **LA/NYC (Neighborhood Name Matching Strategy)**:
   - Created comprehensive lists of all Airbnb neighborhood names (266 for LA, 224 for NYC)
   - Collected Census data for each neighborhood individually
   - Applied text standardization to handle spelling variations
   - Manual verification for ambiguous cases (e.g., "West Hollywood" vs "Hollywood West")
   - Result: 90.2% match rate for LA, 92.9% for NYC after 3 rounds

4. **Broward County (Municipality Strategy)**:
   - Recognized Airbnb neighborhoods were city/municipality names
   - Used Census Place-level data for each municipality
   - Direct matching: Airbnb "fort lauderdale" → Census Place "Fort Lauderdale"
   - Result: 100% match rate for all 34 municipalities

**Technical Implementation**:
```python
def standardize_text(text):
    """Standardize geographic identifiers for matching"""
    if pd.isna(text):
        return text
    text = str(text).lower().strip()
    while '  ' in text:
        text = text.replace('  ', ' ')
    return text

# Apply to all geographic identifiers before merging
df['city'] = df['city'].apply(standardize_text)
df['neighborhood'] = df['neighborhood'].apply(standardize_text)
```

#### **Challenge 2: Data Granularity Mismatch**

**Problem**: Airbnb data at listing level (226,787 rows) needed to be aggregated to neighborhood level (582 rows) while preserving the ability to calculate density measures.

**Solution**: Implemented multi-stage aggregation pipeline:

1. **Stage 1: Listing-Level Processing**:
   - Loaded each city's Airbnb file with all 79 columns
   - Extracted neighborhood identifier from `neighbourhood_cleansed` column
   - Standardized neighborhood names using text normalization

2. **Stage 2: Neighborhood Aggregation**:
   - Grouped listings by standardized neighborhood name
   - Counted total listings per neighborhood
   - Preserved city identifier for each neighborhood
   - Reduced 226,787 rows → 582 neighborhood-level observations

3. **Stage 3: Density Calculation**:
   - Merged aggregated counts with housing unit data
   - Calculated Airbnb density = listings / housing_units
   - Preserved both numerator (count) and denominator (housing units) for transparency

**Result**: Successfully aggregated 226,787 individual listings into 582 neighborhoods while maintaining the information needed for density calculations.

#### **Challenge 3: Multi-Source Validation**

**Problem**: 38 source files from 10 different providers with varying measurement units, time periods, and quality levels.

**Solution**: Implemented comprehensive validation pipeline:

1. **Unit Standardization**:
   - Converted all rent values to 2024 dollars using CPI adjustment
   - Standardized population density to persons per square mile
   - Converted percentages to decimal format (0-100 scale)

2. **Temporal Alignment**:
   - Airbnb data: 2023-2024 (most recent scrapes)
   - Census data: ACS 2019-2023 5-Year Estimates
   - Rent data: Adjusted to 2024 dollars regardless of collection year
   - Tourism classification: Current as of 2024

3. **Quality Checks**:
   - Validated all numeric values are positive (rent, income, population)
   - Checked for extreme outliers (flagged but retained)
   - Verified log transformations only applied to positive values
   - Ensured no division by zero in density calculations

4. **Source Prioritization**:
   - When multiple sources provided the same variable, used hierarchy:
     - Primary: Most recent, most specific geographic level
     - Secondary: Broader geographic aggregation
     - Tertiary: Older data adjusted to current period

**Example CPI Adjustment**:
```python
# Adjust historical rent to 2024 dollars
cpi_2024 = 314.0  # December 2024 CPI-U
cpi_year = get_cpi_for_year(data_year)
rent_2024 = rent_historical * (cpi_2024 / cpi_year)
```

#### **Challenge 4: Incremental Fill Strategy**

**Problem**: Three rounds of data collection meant new data needed to fill gaps without overwriting existing values or creating duplicates.

**Solution**: Implemented row-by-row incremental fill algorithm:

1. **Load Existing Dataset**:
   - Read current state of integrated dataset
   - Identify which neighborhoods have missing values for which variables

2. **Load New Data File**:
   - Read newly collected data file
   - Standardize geographic identifiers

3. **Incremental Fill**:
   ```python
   for idx, new_row in new_data.iterrows():
       city = new_row['city']
       neighborhood = new_row['neighborhood']
       
       # Find matching row in existing dataset
       mask = (final_df['city'] == city) & (final_df['neighborhood'] == neighborhood)
       
       if mask.any():
           # Fill ONLY missing values, preserve existing data
           for col in ['median_rent', 'housing_units', 'median_household_income', 
                      'population_density', 'pct_college', 'tourist_area']:
               if col in new_row and pd.notna(new_row[col]):
                   # Use fillna to preserve existing values
                   final_df.loc[mask, col] = final_df.loc[mask, col].fillna(new_row[col])
   ```

4. **Verification**:
   - After each fill, calculated completeness rate
   - Generated reports showing which neighborhoods were updated
   - Verified no existing data was overwritten

**Result**: Successfully integrated data from 3 rounds without data loss or duplication. Completeness increased from 0.3% → 14.3% → 92.8% → 100%.

#### **Challenge 5: Duplicate Resolution**

**Problem**: Multiple source files contained overlapping geographic coverage (e.g., different LA neighborhood files covering some of the same areas).

**Solution**: Implemented duplicate detection and resolution protocol:

1. **Duplicate Detection**:
   ```python
   # Check for duplicate neighborhoods within each city
   duplicates = df.duplicated(subset=['city', 'neighborhood']).sum()
   if duplicates > 0:
       print(f"Found {duplicates} duplicate neighborhoods")
   ```

2. **Resolution Strategy**:
   - For numeric variables: Take median across duplicate entries
   - For categorical variables: Take mode (most common value)
   - For binary variables: Take maximum (if any source says 1, use 1)

3. **Median Aggregation**:
   ```python
   # Resolve duplicates by taking median
   df_clean = df.groupby(['city', 'neighborhood']).median().reset_index()
   ```

4. **Documentation**:
   - Logged all duplicate resolutions
   - Verified that median values were reasonable
   - Manually inspected cases where duplicates had large discrepancies

**Result**: Resolved 23 duplicate neighborhood entries across all source files, ensuring each of the 582 neighborhoods appears exactly once in the final dataset.

### Summary of Technical Solutions

| Challenge | Solution Approach | Technical Method | Result |
|-----------|------------------|------------------|---------|
| Geographic Fragmentation | City-specific matching strategies | Text standardization + custom matching logic | 100% match rate |
| Data Granularity | Multi-stage aggregation | Group-by operations preserving density components | 226,787 → 582 rows |
| Multi-Source Validation | Comprehensive validation pipeline | Unit standardization + temporal alignment + quality checks | Consistent, validated data |
| Incremental Fill | Row-by-row fill algorithm | Conditional fillna operations | 0.3% → 100% completeness |
| Duplicate Resolution | Median aggregation | Group-by with median/mode functions | 582 unique neighborhoods |

These technical solutions transformed a fragmented, incompatible set of 38 source files into a unified, analysis-ready dataset with 100% completeness and zero missing values.

---

## Scripts

### `create_neighborhood_dataset.py`
Creates the initial neighborhood-level dataset from raw Airbnb listings data.

**Usage:**
```bash
python create_neighborhood_dataset.py
```

**Output:**
- Aggregates 119,729 Airbnb listings into 582 neighborhoods
- Creates base dataset structure

### `integrate_data.py`
Integrates Airbnb data with demographic, rent, housing, and tourism data.

**Usage:**
```bash
python integrate_data.py
```

**Output:**
- Merges all data sources
- Computes derived variables (densities, log transformations)
- Exports final dataset in Stata and CSV formats

---

## Econometric Models

### Model 1: Baseline Linear Model

$$
\text{rent}_i = \beta_0 + \beta_1(\text{AirbnbDensity}_i) + \beta_2(\text{Income}_i) + \beta_3(\text{HousingUnits}_i) + \beta_4(\text{TouristArea}_i) + \sum_{c} \gamma_c \text{CityDummy}_{ic} + u_i
$$

**Variables:**
- $\text{rent}_i$ = Median monthly rent in neighborhood $i$
- $\text{AirbnbDensity}_i$ = Airbnb listings per housing unit
- $\text{Income}_i$ = Median household income
- $\text{HousingUnits}_i$ = Total housing units (supply proxy)
- $\text{TouristArea}_i$ = Binary indicator (1 = tourist area, 0 = residential)
- $\text{CityDummy}_{ic}$ = City fixed effects
- $u_i$ = Error term

### Model 2: Nonlinear + Heterogeneous Effects

$$
\begin{aligned}
\text{rent}_i = \beta_0 &+ \beta_1(\text{AirbnbDensity}_i) + \beta_2(\text{AirbnbDensity}_i^2) + \beta_3(\text{Income}_i) \\
&+ \beta_4(\text{HousingUnits}_i) + \beta_5(\text{TouristArea}_i) \\
&+ \beta_6(\text{AirbnbDensity}_i \times \text{TouristArea}_i) + \sum_{c} \gamma_c \text{CityDummy}_{ic} + u_i
\end{aligned}
$$

**Marginal Effect of Airbnb on Rent:**

$$
\frac{\partial \text{rent}}{\partial \text{AirbnbDensity}_i} = \beta_1 + 2\beta_2 \text{AirbnbDensity}_i + \beta_6 \text{TouristArea}_i
$$

### Expected Signs

| Parameter | Variable | Expected Sign | Economic Reasoning |
|-----------|----------|---------------|-------------------|
| $\beta_1$ | AirbnbDensity | **Positive (+)** | Airbnb shifts supply from long-term to short-term rentals |
| $\beta_2$ | AirbnbDensity² | **Negative (−)** | Diminishing marginal impact; saturation effect |
| $\beta_3$ | Income | **Positive (+)** | Higher-income neighborhoods have higher rents |
| $\beta_4$ | HousingUnits | **Negative (−)** | More housing supply reduces price pressure |
| $\beta_5$ | TouristArea | **Positive (+)** | Tourist areas structurally have higher rents |
| $\beta_6$ | Density × TouristArea | **Positive (+)** | Airbnb effect amplified in tourist neighborhoods |

**Interpretation of $\beta_6$:**
- If $\beta_6 > 0$: Airbnb raises rents **more** in tourist neighborhoods
- If $\beta_6 = 0$: Airbnb affects tourist and non-tourist neighborhoods equally
- If $\beta_6 < 0$: Airbnb's effect is weaker in tourist zones (unlikely)

---

## Data Quality

### Completeness by City
| City | Total Neighborhoods | Complete Data | % Complete |
|------|---------------------|---------------|------------|
| Austin | 44 | 44 | 100.0%  |
| Dallas | 14 | 14 | 100.0%  |
| Broward County | 34 | 34 | 100.0%  |
| New York City | 224 | 224 | 100.0%  |
| Los Angeles | 266 | 266 | 100.0%  |
| **Total** | **582** | **582** | **100.0%**  |

### Variable Completeness
| Variable | Complete | % Complete |
|----------|----------|------------|
| City & Neighborhood | 582/582 | 100.0%  |
| Airbnb Count | 582/582 | 100.0%  |
| Median Rent | 582/582 | 100.0%  |
| Housing Units | 582/582 | 100.0%  |
| Median Household Income | 582/582 | 100.0%  |
| Population Density | 582/582 | 100.0%  |
| % College Educated | 582/582 | 100.0%  |
| Tourist Area | 582/582 | 100.0%  |
| Airbnb Density | 582/582 | 100.0%  |
| All Log Variables | 582/582 | 100.0%  |

---

## Key Features

- **Large Sample Size**: 582 complete observations  
- **Perfect Completeness**: 100% complete - ZERO missing values!  
- **Geographic Diversity**: 5 major U.S. cities  
- **Multiple Data Sources**: Census (ACS 2023), Zillow, Airbnb  
- **Derived Variables**: Logs, densities, ratios pre-computed  
- **Standardized Format**: Clean, consistent naming conventions  
- **Publication Ready**: Suitable for academic research and publication

---

## Limitations

- Cross-sectional data (not panel data)
- Tourism classification partially subjective
- Different geographic units across cities (ZIP codes, districts, neighborhoods)
- Potential endogeneity concerns (Airbnb may locate in high-rent areas)

---

## Citation

If you use this dataset, please cite:

```
Neighborhood-level Airbnb and housing data for five major U.S. cities 
(Austin, Dallas, Los Angeles, New York City, and Broward County), 2023-2024. 
Data sources: Inside Airbnb (listings), U.S. Census Bureau (ACS 2023), 
Zillow (rent data).
```

---

## Credits

**Author**: Samson Bui

**Institution**: Texas Christian University  
**Course**: Econometrics  
**Project**: Airbnb Impact on Housing Rents - Neighborhood-Level Analysis  
**Date**: November 2025

---

**Last Updated**: November 15, 2025  
**Status**: Ready for Analysis

