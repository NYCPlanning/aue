# Adult Use Establishments Proximity Analysis

This repo contains code for identifying the best- and worst-case scenarios for the spatial distribution of Adult Use Establishments in NYC, given the restriction that no establishment be within 500ft of another establishment.

## Background

## Usage

Run `./aue.sh` from the home directory. Results are found in the `output` directory. Each row contains the BBLs for a single solution. The number of columns is the total number of possible establishments. These counts are also output to the terminal.

## Overview of Results

Using the methodology outlined below, we have identified a best-case scenario of **208** lots that could feasibly have Adult Use Establishments, given the distance restrictions. The worst-case scenario, meaning the case where establishments are arranged in a way that limits the addition of new establishments, is **203** lots. Note that these numbers are the maximum *possible* establishments. In reality, not all lots are currently vaccant.

These numbers are dependent on the input data, however, and there is ongoing work vetting the input lots as realistic locations for an establishment (i.e. there is sufficient street-frontage and access). In the future, this workflow can be re-run with refined input data to improve the estimate of best- and worst-case scenarios, simply by modifying the path for the input buffered lots.

# Methodology

We approached this problem by creating a matrix of possible co-existing establishments. Simplifying the distance calculations to a binary flag makes our calculations much easier. 

### Data loading and preparation

**Input data**:

The input data for this analysis is a shapefile of lots, buffered to 500ft. See the image below for an example of what this kind of data looks like.

![input-data](https://github.com/NYCPlanning/aue/blob/master/input-data.png "Buffered Lots")


**Creating a "possibility matrix"**: 

Using the buffers in the input data, we can create a square matrix that represents whether an establishment on one lot can coexist with an establishment on another lot. If two establishments can exist together, the value is 1. If they cannot, the value is 0. The diagonals are null.

Note that this matrix is always square, and is always symetrical. To create this matrix, we test whether or not two buffers intersect using postgres,
then pivot the pair-wise intersection data using python. Below is a simple example of a lot arrangement and how the resulting possibility matrix would look.

![example](https://github.com/NYCPlanning/aue/blob/master/example.png "Simple example")

| |**0**|**1**|**2**|**3**|
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
we can extract the 0th row of the matrix:

|**0**|**1**|**2**|**3**|
|---|---|---|---|
| - | 0 | 1 | 1 |

Zeros are lots that are unavailable for the next assignment because of proximity to an already-assigned lot. The null values are lots that we've already assigned. The next establishment must be placed on a lot with a 1. Let's assign the next establishment to the first available lot,
lot 2. Now, our list of lots with establishments is {0, 2}. In order to find the possibilities for the next establishment,
we have to take into account the proximity information for *both* existing establishments. We can do this by multiplying the elements
of the 0th row and the 2nd row as follows:

|**0**|**1**|**2**|**3**|
|---|---|---|---|
| - * 1 = - | 0 * 0 = 0 | 1 * - = - | 1 * 1 = 1|

The only possibility for our next establishment is on lot 3. Our lot list is now {0, 2, 3}. There are no more establishments we can add to this solution.
If we were to find the possibilities for the next lot, we would get the following:

|**0**|**1**|**2**|**3**|
|---|---|---|---|
| - * 1 * 1 = - | 0 * 0 * 1 = 0 | 1 * - * 1 = - | 1 * 1 * - = - |

There are no ones, so we are done.

This solution looks like:

![first-solution](https://github.com/NYCPlanning/aue/blob/master/first-solution.png "Best-case solution")

### Picking new "seeds" & how solutions relate to eachother

Of course, we know from our picture above that there is another solution. Instead, we could have establishments on lots 1 and 3. We would find this solution by rerunning the process with a different seed.

If we instead seed an establishment at lot 1, the initial list of establishment lots is: {1}

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

![second-solution](https://github.com/NYCPlanning/aue/blob/master/second-solution.png "Worst-case solution")

This process gets repeated for all seeds. Note that this will duplicate solutions, since the *order* in which we assign establishments to lots 
doesn't matter. Before providing a table of results, we filter out permutations (i.e. {0, 3, 2} is not included if {0, 2, 3} is already a solution).

### Example results

In this example, we only have two possible arrangements of establishments. The best-case scenario is the one with the most possible establishments, or 3 establishments placed on lots 0, 2, and 3. The worst-case scenario has a maximum possible number of establishments of 2, placed on lots 1 and 3.

In reality, multiple arrangements yeild the same number of maximum possible establishments. The tables in the output folder contain all arrangements associated with the best- and worst-case scenarios.