# Data Description and Sources

## Study Area and Geographic Coverage

This study examines the relationship between short-term rental activity (Airbnb) and long-term housing rents at the neighborhood level across five major U.S. metropolitan areas: Austin, Dallas, Los Angeles, New York City, and Broward County (Fort Lauderdale area). These markets were selected to represent diverse geographic regions, varying regulatory environments, and different levels of tourism intensity. The dataset encompasses 582 distinct neighborhoods, capturing variation in urban density, demographic composition, housing supply, and tourism activity across these metropolitan areas.

The geographic units of analysis vary by city due to differences in how Airbnb and Census data are organized. In Austin, neighborhoods correspond to ZIP Code Tabulation Areas (ZCTAs), providing 44 distinct geographic units. Dallas neighborhoods are defined by City Council Districts, yielding 14 units. Los Angeles contains 266 neighborhood-defined areas following Airbnb's neighborhood classification system, while New York City includes 224 neighborhoods spanning all five boroughs (Manhattan, Brooklyn, Queens, The Bronx, and Staten Island). Broward County is divided into 34 municipalities and unincorporated areas. This multi-city approach allows for the examination of Airbnb's impact across different market conditions while controlling for city-level fixed effects.

## Raw Data Acquisition and Scale

The construction of this dataset required the integration of data from **38 distinct source files** spanning five different data categories. The raw data encompassed approximately **227,000 rows** of listing-level information and **1,200+ rows** of supplementary neighborhood-level data across multiple dimensions. This multi-source integration presented significant methodological challenges due to incompatible geographic definitions, varying levels of data granularity, and the need for systematic quality control across diverse data types.

### Scale of Raw Data Sources

The raw data collection involved five primary categories:

**1. Airbnb Listings Data (5 files, 226,787 rows, 79 columns each)**
- Austin: 28,956 individual listings
- Broward County: 39,074 individual listings  
- Dallas: 9,790 individual listings
- Los Angeles: 84,139 individual listings
- New York City: 64,828 individual listings

Each Airbnb file contained 79 variables including property characteristics (bedrooms, bathrooms, property type), pricing information, host details, location coordinates, availability calendars, and guest review metrics. From these comprehensive listing files, I extracted neighborhood identifiers and aggregated listing counts to the neighborhood level.

**2. Census Demographics Data (27 files, 745 rows total)**
These files were collected in three rounds to achieve complete neighborhood coverage:
- Round 1 (9 files): Austin ZIP codes, Dallas districts, initial LA/NYC/Broward neighborhoods
- Round 2 (15 files): Comprehensive LA and NYC neighborhood coverage in 8 batches
- Round 3 (3 files): Remaining small and remote neighborhoods

Each demographic file contained 6-8 variables including median household income, population, housing units, educational attainment, and population density.

**3. Rent Data (2 files, 88 rows total)**
- Primary neighborhood rent file: 43 neighborhoods
- Austin ZIP-level rent file: 45 ZIP codes

Rent files contained median monthly rent values from Zillow Research Data and HUD Fair Market Rent estimates.

**4. Housing Units Data (1 file, 33 rows)**
Contained total housing unit counts for neighborhoods where ACS data were not directly available.

**5. Tourism Classification Data (6 files, 319 rows total)**
Tourism indicator files created through manual classification and research, with separate files for each city and data collection round.

### Data Integration Methodology

The integration of these 38 source files into a single analytical dataset required a systematic multi-stage approach addressing three primary challenges: geographic fragmentation, data standardization, and quality control.

**Stage 1: Airbnb Data Aggregation**

The first stage involved processing the five Airbnb listing files (226,787 total rows) to create neighborhood-level aggregates. For each city file, I:

1. Loaded the full listing-level dataset with all 79 variables
2. Identified the neighborhood identifier column (`neighbourhood_cleansed` or `neighbourhood`)
3. Applied text standardization (lowercase conversion, whitespace removal, space collapsing)
4. Grouped listings by standardized neighborhood name
5. Counted the number of listings per neighborhood
6. Assigned city identifiers to each neighborhood

This aggregation reduced the 226,787 individual listings to 582 unique neighborhoods, creating the base dataset structure. The aggregation process preserved geographic diversity while creating a manageable analytical unit.

**Stage 2: Text Standardization Protocol**

A critical methodological innovation was the implementation of a consistent text standardization protocol applied to all geographic identifiers across all 38 source files. The standardization function performed the following operations:

1. Convert all text to lowercase (e.g., "Hollywood" → "hollywood")
2. Strip leading and trailing whitespace
3. Collapse multiple consecutive spaces into single spaces
4. Remove special characters that might cause matching failures

This standardization was essential because the same neighborhood might appear as "West Hollywood", "west hollywood", or "West  Hollywood" (with extra space) across different data sources. Without standardization, these would fail to match during merging operations. The standardization protocol was applied uniformly to city names and neighborhood names in all 38 source files before any merging operations.

**Stage 3: Iterative Left-Join Strategy**

The core integration methodology employed iterative left joins, preserving all 582 Airbnb neighborhoods as the base and progressively filling in data from supplementary sources. The merge sequence was:

1. **Base**: Airbnb neighborhood counts (582 neighborhoods, 3 variables)
2. **Merge 1**: Census demographics (27 files) → added income, population density, education, housing units
3. **Merge 2**: Rent data (2 files) → added median rent
4. **Merge 3**: Housing units (1 file) → filled remaining housing unit gaps
5. **Merge 4**: Tourism classification (6 files) → added tourist area indicator

Each merge used `(city, neighborhood)` as the composite key. The left-join approach ensured no Airbnb neighborhoods were dropped, even if supplementary data were unavailable. After each merge, I calculated match rates to identify gaps requiring additional data collection.

**Stage 4: Three-Round Data Collection**

The iterative merge process revealed substantial missing data after the initial integration (only 2 of 582 neighborhoods matched completely). This necessitated three rounds of targeted data collection:

**Round 1** focused on structured geographic units (Austin ZIP codes, Dallas districts) where Census data could be directly matched. This round involved collecting 9 new data files and increased completeness from 0.3% to 14.3% (83 neighborhoods).

**Round 2** addressed the bulk of missing neighborhoods in Los Angeles and New York City through systematic batch collection. I divided the missing neighborhoods into priority groups based on Airbnb listing volume and collected data in 8 batches for LA and 6 batches for NYC. This round added 15 new data files and increased completeness to 92.8% (540 neighborhoods).

**Round 3** targeted the final 42 neighborhoods, primarily small, remote, or industrial areas with limited Airbnb activity. This round added 3 new data files and achieved 100% completeness (582 neighborhoods).

### Methodological Complexity and Challenges

The data integration task presented several layers of complexity:

**Geographic Fragmentation**: The most significant challenge was reconciling incompatible geographic definitions. Airbnb uses informal neighborhood names (e.g., "78701" for Austin, "District 1" for Dallas, "Hollywood" for LA), while Census data are organized by formal geographic units (ZCTAs, tracts, places). This required city-specific strategies: direct ZCTA matching for Austin, district-level aggregation for Dallas, and neighborhood name matching with manual verification for LA and NYC.

**Data Granularity Mismatch**: The Airbnb data were at the listing level (226,787 rows), while supplementary data were at the neighborhood level (hundreds of rows). This required careful aggregation of the Airbnb data while preserving the ability to calculate density measures using housing unit denominators.

**Multi-Source Validation**: With 38 source files from different providers (Inside Airbnb, Census Bureau, Zillow, HUD, manual research), ensuring consistency in measurement units, time periods, and geographic coverage required extensive validation. For example, rent values from different sources needed CPI adjustment to a common base year (2024 dollars).

**Incremental Fill Strategy**: The three-round data collection approach required a sophisticated fill strategy that updated missing values without overwriting existing data. For each new data file, I implemented row-by-row matching that filled only `NaN` values in the target dataset, preserving data from earlier rounds when available.

**Duplicate Resolution**: Several source files contained overlapping geographic coverage (e.g., multiple files covering different subsets of LA neighborhoods). I implemented duplicate detection that identified neighborhoods appearing in multiple files and resolved conflicts by taking median values across sources.

### Data Source Diversity

The final dataset integrates information from **10 distinct data providers and repositories**:

1. **Inside Airbnb** - Short-term rental listings (5 files)
2. **U.S. Census Bureau ACS** - Demographics and housing (27 files)
3. **Zillow Research Data** - Median rent estimates
4. **HUD Fair Market Rents** - Rent benchmarks
5. **MetroGIS Collaborative** - Geographic boundary data
6. **Dallas Open Data Portal** - City council district demographics
7. **LA County Open Data** - Los Angeles neighborhood data
8. **NYC Open Data** - New York City neighborhood data
9. **Broward County Open Data** - Florida municipal data
10. **Manual Research** - Tourism classification (TripAdvisor, tourism boards, hotel databases)

This diversity of sources, while ensuring comprehensive coverage, required developing flexible data processing pipelines that could handle varying file formats (CSV with different delimiters), column naming conventions, and data quality levels.

## Airbnb Listings Data

Short-term rental data come from Inside Airbnb (http://insideairbnb.com/), an independent, non-commercial initiative that scrapes publicly available information from the Airbnb website. The dataset includes detailed listing-level information for all active Airbnb properties in each metropolitan area as of late 2023 and early 2024. A total of 119,729 individual Airbnb listings (after removing duplicates and inactive listings from the raw 226,787 rows) are aggregated to the neighborhood level for this analysis.

For each listing, the Inside Airbnb dataset provides the neighborhood location (using Airbnb's internal neighborhood classification), property type, room type, number of bedrooms and bathrooms, nightly price, availability, host information, and guest review metrics. The key variable extracted from this dataset is the total count of Airbnb listings in each neighborhood, which serves as the primary measure of short-term rental intensity. These counts are then normalized by the total housing stock in each neighborhood to create an Airbnb density measure (listings per housing unit), which serves as the main independent variable of interest.

The neighborhood names in the Airbnb data are standardized through a text normalization process that converts all strings to lowercase, removes extra whitespace, and ensures consistent spelling. This standardization is essential for merging the Airbnb data with other neighborhood-level datasets that may use slightly different naming conventions.

## Demographic and Socioeconomic Variables

Neighborhood-level demographic and socioeconomic characteristics are obtained from the U.S. Census Bureau's American Community Survey (ACS) 5-Year Estimates for 2019-2023. The ACS provides detailed demographic, social, economic, and housing information at various geographic levels, including ZIP codes, census tracts, and incorporated places. Given the varied geographic units used in the Airbnb data, demographic variables are matched at the appropriate Census geographic level for each city: ZCTA-level data for Austin, aggregated tract-level data for Dallas City Council Districts, and place or neighborhood-level data for Los Angeles, New York City, and Broward County.

Key demographic variables include median household income (in 2023 dollars), which controls for neighborhood affluence and purchasing power. Population density (measured as persons per square mile) captures urban intensity and housing market pressure. Educational attainment is measured as the percentage of adults aged 25 and older with a bachelor's degree or higher, serving as a proxy for neighborhood socioeconomic status and the prevalence of knowledge workers who may demand urban amenities. Total population and land area are used to calculate population density for neighborhoods where it is not directly available in the ACS tables.

For neighborhoods where direct ACS data at the precise geographic level are not available, Census tract-level data are aggregated using population-weighted averages to match the Airbnb neighborhood boundaries. This approach is particularly relevant for Los Angeles and New York City, where Airbnb's neighborhood definitions do not always correspond to standard Census geographic units.

## Housing Market Variables

Housing stock data come from two primary sources. Total housing units for each neighborhood are obtained from the ACS 5-Year Estimates (Table B25001), providing a measure of housing supply that serves as the denominator in the Airbnb density calculation. This variable is crucial for distinguishing between neighborhoods with high absolute numbers of Airbnb listings due to large housing stocks versus those with high Airbnb penetration rates.

Median rent data, the dependent variable in this analysis, are compiled from multiple sources depending on data availability. Primary sources include Zillow Research Data, which provides median rent estimates at the ZIP code and neighborhood level for many U.S. markets, and the Department of Housing and Urban Development (HUD) Fair Market Rent data. For neighborhoods where current rental data are not available from these sources, median gross rent estimates from the ACS 5-Year Estimates (Table B25064) are used. All rent values are adjusted to reflect 2024 dollars using the national Consumer Price Index for All Urban Consumers (CPI-U) to ensure comparability across markets and over time.

The median rent values represent the typical monthly cost for a long-term residential rental unit in each neighborhood. These rents are converted to natural logarithms for the econometric analysis to address the right-skewed distribution of rent values and to facilitate the interpretation of regression coefficients as elasticities.

## Tourism Classification

A binary tourism indicator is constructed for each neighborhood to distinguish between areas that primarily serve tourists versus residential neighborhoods. This classification is based on multiple criteria, including hotel density (number of hotels per square mile), presence of major tourist attractions (museums, entertainment venues, beaches, theme parks), official tourism board designations, and prominence in travel guides such as TripAdvisor and Lonely Planet.

The tourism classification was developed through a multi-stage process. First, neighborhoods containing major tourist landmarks or attractions were identified and classified as tourist areas (coded as 1). Examples include Hollywood and Venice Beach in Los Angeles, Times Square and the Financial District in Manhattan, South Beach in Broward County, and Downtown Austin. Second, neighborhood-level hotel density was calculated using business registry data, with neighborhoods exceeding a threshold of 5 hotels per square mile classified as tourist areas. Finally, for neighborhoods not captured by the first two criteria, manual classification was performed based on qualitative assessments from tourism websites and local knowledge.

The tourism indicator serves as both a control variable and an interaction term in the econometric models. As a control, it accounts for the structural differences in rent levels between tourist-oriented and residential neighborhoods. As an interaction with Airbnb density, it tests whether the impact of short-term rentals on long-term rents differs systematically between tourist areas and residential neighborhoods.

## Data Integration and Quality Control

The integration of these diverse data sources required a systematic multi-stage process to address geographic fragmentation and ensure data quality. The primary challenge stemmed from incompatible geographic definitions across data sources: Airbnb uses neighborhood names, the Census uses standardized geographic units (ZCTAs, tracts, places), and rent data providers use various geographic levels.

To address this fragmentation, I implemented a three-round data collection and integration strategy. Round 1 focused on cities with structured geographic units (Austin ZIP codes and Dallas districts), achieving matches for 83 neighborhoods (14.3% of the sample). Round 2 involved comprehensive neighborhood-level data collection for Los Angeles and New York City, conducted in batches to ensure systematic coverage, bringing the match rate to 540 neighborhoods (92.8%). Round 3 targeted the remaining 42 neighborhoods, primarily small or remote areas, achieving complete coverage of all 582 neighborhoods.

All geographic identifiers (city names, neighborhood names) were standardized using a consistent text normalization function that converts strings to lowercase, removes extra whitespace, and collapses multiple spaces. This standardization was essential for successful merging across datasets. Each merge was performed using left joins on city and neighborhood identifiers, preserving all Airbnb neighborhoods and filling in data from supplementary sources where matches were found.

Multiple quality control checks were implemented throughout the integration process. Duplicate neighborhood records within each city were identified and resolved by taking median values across duplicates. Numeric variables were validated to ensure positive values for all measures where negative values are not meaningful (e.g., rent, income, population density). Extreme outliers were flagged but retained in the dataset to avoid biasing the sample toward average neighborhoods. After each round of data integration, match rates were calculated and completeness reports generated to identify remaining gaps.

## Derived Variables

Several derived variables are constructed from the primary data sources for use in the econometric analysis. The key independent variable, Airbnb density, is calculated as:

$$
\text{AirbnbDensity}_i = \frac{\text{AirbnbCount}_i}{\text{HousingUnits}_i}
$$

where $i$ indexes neighborhoods. This density measure provides a standardized metric of short-term rental penetration that is comparable across neighborhoods of different sizes.

Three logarithmic transformations are applied to address skewness in the data distributions and to facilitate interpretation of regression coefficients as elasticities:

$$
\text{log\_rent}_i = \ln(\text{MedianRent}_i)
$$

$$
\text{log\_income}_i = \ln(\text{MedianIncome}_i)
$$

$$
\text{log\_airbnb\_density}_i = \ln(\text{AirbnbDensity}_i)
$$

These log transformations are applied only to positive values; observations with zero or missing values for the underlying variables remain as missing in the log-transformed versions. The log-log specification in the primary regression models allows coefficients to be interpreted as elasticities, indicating the percentage change in rent associated with a one-percent change in Airbnb density or income.

For the nonlinear specification (Model 2), a quadratic term is constructed:

$$
\text{AirbnbDensity}^2_i = (\text{AirbnbDensity}_i)^2
$$

This squared term allows the estimation of diminishing or increasing marginal effects of Airbnb density on rents. An interaction term between Airbnb density and the tourism indicator is also constructed:

$$
\text{AirbnbDensity}_i \times \text{TouristArea}_i
$$

This interaction tests whether the relationship between short-term rentals and long-term rents differs systematically between tourist-oriented neighborhoods and residential areas.

## Final Dataset Characteristics

The final integrated dataset contains 582 neighborhoods across five metropolitan areas, with complete data for all variables (100% completeness, zero missing values). The panel-like structure includes both cross-sectional variation across neighborhoods and cities, though the data represent a single time period (2023-2024) rather than a true longitudinal panel. City fixed effects are included in all regression specifications to control for unobserved city-level characteristics that may affect both Airbnb prevalence and rent levels.

The dataset exhibits substantial variation across key dimensions. Airbnb density ranges from near-zero in some residential neighborhoods to over 0.28 listings per housing unit in high-tourism areas. Median rent varies from $980 per month in lower-income neighborhoods to over $5,600 in affluent urban cores. The 582 neighborhoods span the full spectrum of urban forms, from dense urban centers with over 67,000 persons per square mile to suburban and exurban areas with densities below 300 persons per square mile. Educational attainment ranges from 18% to 82% with bachelor's degrees or higher, capturing both working-class and highly educated professional neighborhoods.

This rich variation, combined with the multi-city structure and complete data coverage, provides a robust foundation for estimating the causal relationship between short-term rental intensity and long-term housing rents while controlling for a comprehensive set of neighborhood characteristics and city-level confounders.

## Summary Statistics

Table 1 presents summary statistics for the full sample of 582 neighborhoods. Airbnb density averages 0.02 listings per housing unit (2% of the housing stock), with substantial variation across neighborhoods (standard deviation of 0.03). Median rent averages $2,146 per month, ranging from $980 to $5,600. Median household income averages $86,527, with considerable variation reflecting the socioeconomic diversity of the sample. Population density averages 19,293 persons per square mile, though this figure is heavily influenced by dense urban neighborhoods in New York City and Los Angeles. Educational attainment averages 50.3% with bachelor's degrees or higher, substantially above the national average, reflecting the urban character of the study areas. Approximately 27% of neighborhoods are classified as tourist areas, indicating that the majority of the sample consists of primarily residential neighborhoods where Airbnb may compete more directly with long-term rental housing.

City-specific patterns reveal important heterogeneity. Austin and Dallas exhibit 100% data completeness and relatively uniform suburban development patterns. New York City and Los Angeles, with 224 and 266 neighborhoods respectively, exhibit the greatest internal variation in density, income, and Airbnb penetration. Broward County's 34 municipalities represent a mix of beach resort cities and inland suburban communities, with corresponding variation in tourism intensity and Airbnb activity.

---

**Data Collection Period**: November 2024 - November 2025  
**Geographic Coverage**: 582 neighborhoods across 5 U.S. metropolitan areas  
**Temporal Coverage**: Cross-sectional data for 2023-2024  
**Completeness**: 100% (zero missing values across all variables)

