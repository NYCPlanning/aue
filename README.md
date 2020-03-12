# Proximity Analysis

This repo contains code for identifying the best- and worst-case scenarios for the spatial distribution of any proximity-restricted establishment type in NYC. The input data for this analysis is a subset of PLUTO lots where establishments could appear in the future. Whether or not an establishment is "allowed" can depend on several proximity restrictions. There are restrictions on the minimum allowable distance between one type of establishment and another (i.e. a city may regulate the commercial uses that can exist close to schools or houses of worship), as well as the distance *between* establishments of a given type. The purpose of these restrictions is to avoid the formation of a "district." This analysis deals with the second type of restriction. As currently configured this repo explores a restriction in which a single shop cannot exist within 500ft of another shop. Given this restriction, some arrangements of establishmets will allow for more total establishments than others. Placing an establishment on a lot that is within 500ft of numerous other potential establishment lots eliminates those neighboring lots as possibilities for the "next" establishment siting.

# Background

## Usage

Run `./aue.sh` from the home directory. Results are found in the `output` directory. Each row of the output file contains the BBLs for a single solution. The number of columns is the total number of possible establishments. These counts are also output to the terminal.

## Overview of Results

Using the methodology outlined below, we have identified a best-case scenario of **339** lots that could feasibly have proximity-restricted establishments, given a 500ft restriction. The worst-case scenario, meaning the case where establishments are arranged in a way that limits the addition of new establishments, is **333** lots. Note that these numbers are the maximum number of *possible* establishments. In reality, not all lots are currently vaccant or suitable for future shops.


## Methodology

We approached this problem by creating a matrix of possible co-existing establishments -- lots that can simultaneaously have establishments because they are further than 500ft apart. Simplifying the distance calculations to a binary flag makes our calculations much easier. 

### Data loading and preparation

**Input data**:

The input data for this analysis is the subset of MapPLUTO lots that meet the criteria, buffered to 500ft. See the image below for an example of what this data looks like.

![input-data](https://github.com/NYCPlanning/aue/blob/master/readme-images/input-data.png "Buffered Lots")


**Creating a "possibility matrix"**: 

Using the buffers in the input data, we can create a square matrix that represents whether an establishment on one lot can coexist with an establishment on another lot. Remember that in this problem, two given establishments can only coexist if they are at least 500ft away from eachother. If this is the case, the value in the possibility matrix is 1. If the two establishments are within 500ft, the value is 0. The diagonals are null.

Note that this matrix is always square. To create this matrix, we test whether a lot's 500ft buffer intersects with the geometry of another lot,
then pivot the pair-wise intersection data. Below is a simple example of a lot arrangement and how the resulting possibility matrix would look.

![example](https://github.com/NYCPlanning/aue/blob/master/readme-images/example.png "Simple example")

|**Lot Index**|**0**|**1**|**2**|**3**|
|---|---|---|---|---|
|**0**| - | 0 | 1 | 1 |
|**1**| 0 | - | 0 | 1 |
|**2**| 1 | 0 | - | 1 |
|**3**| 1 | 1 | 1 | - |

### Using the possibility matrix to identify a single solution

To explain the algorithm in this repo, let's refer to the example above.

The first step is to assign an establishment to a lot. We can think of this as the "seed".
For simplicity, we will assign this to the first indexed lot, lot 0.

We can now refer to the possibility matrix to determine where we can place the next establishment. Specifically,
we can extract the top row of the matrix, which describes which lots can have establishments if there is an establishment on lot 0:

|**0**|**1**|**2**|**3**|
|---|---|---|---|
| - | 0 | 1 | 1 |

Zeros are lots that are unavailable for the next assignment because of proximity to an already-assigned lot. The null values are lots that we've already assigned. The next establishment must be placed on a lot with a 1. Let's assign the next establishment to the left-most available lot,
lot 2. Now, our list of lots with establishments is {0, 2}. In order to find the possibilities for the next establishment,
we have to take into account the proximity information for *both* existing establishments. We can do this by multiplying the elements
of the top row and the third row as follows:

|**0**|**1**|**2**|**3**|
|---|---|---|---|
| - * 1 = - | 0 * 0 = 0 | 1 * - = - | 1 * 1 = 1|

The only possibility for our next establishment is on lot 3. Our lot list is now {0, 2, 3}. There are no more establishments we can add to this solution.
If we were to try to add another establishment, we would have to multiply all of the rows of the possibility matrix corresponding with our current picks -- {1, 2, and 3}. This would give us:

|**0**|**1**|**2**|**3**|
|---|---|---|---|
| - * 1 * 1 = - | 0 * 0 * 1 = 0 | 1 * - * 1 = - | 1 * 1 * - = - |

There are no ones, meaning there are no lots left where we can put an establishment.

This solution looks like:

![first-solution](https://github.com/NYCPlanning/aue/blob/master/readme-images/first-solution.png "Best-case solution")

### Picking new "seeds" & how solutions relate to eachother

Of course, we know from our picture above that there is another way of picking lots to have establishments without violating the proximity rules. We could have establishments on lots 1 and 3, since they are more than 500ft apart. In order to find *all* of the possible solutions, we have to rerun the selection process from a different starting lot. Rather than picking lot 0 to have the first establishment, we will pick lot 1 to have the first.

In this case, the initial list of establishment lots is: {1}

Our possible next steps are:

|**0**|**1**|**2**|**3**|
|---|---|---|---|
| 0 | - | 0 | 1 |

We assign the next establishment to lot 3. Our list of establishments is {1, 3}. We intuitively know we're done.
Our next possible steps would be:

|**0**|**1**|**2**|**3**|
|---|---|---|---|
| 0 * 1 = 0 | - * 1 = - | 0 * 1 = 0 | 1 * - = - |

This solution looks like:

![second-solution](https://github.com/NYCPlanning/aue/blob/master/readme-images/second-solution.png "Worst-case solution")

This process gets repeated using every possible lot as a seed. Remember that the *order* of lots in a given solution 
doesn't matter. If lot 1 and 2 can both have an establishment, it doesn't matter which of these lots gets an establishment first. 
Before providing a table of results, we filter out permutations (i.e. {0, 3, 2} is not included if {0, 2, 3} is already a solution).

### Example results

In this example, we only have two possible arrangements of establishments. The best-case scenario is the one with the most possible establishments, or 3 establishments placed on lots 0, 2, and 3. The worst-case scenario has a maximum possible number of establishments of 2, placed on lots 1 and 3.

In reality, multiple arrangements yeild the same number of maximum possible establishments. The tables in the output folder contain all arrangements associated with the best- and worst-case scenarios.
