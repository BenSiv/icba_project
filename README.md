# icba_project
Predicting milk attributes as a factor of cattle feed

![Israeli Cattle Breeders Association](docs/ICBA_logo.png)

## Summary
This is a dataset of a single dairy farm in israel. There are two tables, the first is the feed data per group of cows in a daily time series in the years 2005-2022. The second table is the lab results of the milk analysis for the dairy cows in a monthly time series.

## Importat notes
- The groups are not static, cows can pass between them in cycles of milking and period of dryness.
- Not all groups gives milk, so it would be wise to omit non-relevane groups.
- The lab results are messured monthly, and the feed is daily, so parhapse we need only the few days prior to the sample taking. We can eather do a mean of few days prior, or seperating them so the model could learn the important period to effect each attribute of the sample quality. It is reasonable to assume that different attributes changes in different rates from the feed to the milk.
- Allthough the main focus is to increase the milk quality, the milk quantity also needs to be taken into account. We want the milk quantity to increase or at least be stable.
- Environment temprature is a big factor on the quantity of milk given. So, it might be wise to import weather data to try and explain some of the variability.
- Feed categories alone are not a coherent thing, so breaking apart the categories into rough nutrient measurement can be helpfull for the model to reason and infere from it.

## Data Dictionary

### Feed data
- **Date**: Date daily
- **Group**: Categorical nominal, cattle group
- **Group_name**: Categorical nominal, cattle group name
- **Feed_num**: Categorical nominal, number of feed in a day, usualy 2
- **Feed_ID**: Categorical nominal, feed type ID
- **Feed_name**: Categorical nominal, feed type name
- **Quantity**: Numerical continuouse, quantity of feed type
- **Units**: Categorical nominal, units of the quantity column
- **Num_of_cows**: Numerical descrete, number of cows in the group

### Lab results
- **Date**: Date montly
- **Group**: Categorical nominal, cattle group
- **Milk**: Numerical continuouse, Average milk quantity in kg per day
- **Fat**: Numerical continuouse, Percent of fat in the milk
- **Protein**: Numerical continuouse, Percent of protein in the milk
- **Lactose**: Numerical continuouse, Percent of lactose in the milk
- **Somatic_cells**: Numerical descrete, count of somatic cells in a ml of milk.

## Modeling results
The most favorable outcomes were achieved using a random forest model when I utilized nutritional data for each day of the week leading up to the test.

In the enclosed images, you can observe predictions for each of the milk-related metrics. The section before the green dashed line represents the data used for training, while the portion after that line pertains to the test data.

Significantly, there is a pronounced issue of "overfitting," indicating that the model lacks generality, and this has a detrimental impact on the accuracy of predictions for the test data.

![Fat content](docs/figures/week_before/random_forest/Fat.png)
![Protein content](docs/figures/week_before/random_forest/Protein.png)
![Lactose content](docs/figures/week_before/random_forest/Lactose.png)
