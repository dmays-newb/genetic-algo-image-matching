# Genetic Algorithm Assignement: Matching Pictures with Rectangles
Dustin Mays
Fall 2021
CS 480

## Running the Program

### Prerequisites

This is a python script requiring two modules: pil and numpy.
- [Installing Numpy](https://data-flair.training/blogs/install-numpy/)
- [Installing PIL](https://wp.stolaf.edu/it/installing-pil-pillow-cimage-on-windows-and-mac/)

### Procedure for Running

- cd into the root directory of the assignment submission: "/cs480_genetic_dmays"
- Choose a picture to use in this directory or add your own.
- Run the command: `python main.py test-image-1.png`
  - This will run with my first test image, but you can replace `test-image-1.png` with whatever picture you prefer
  - I haven't experimented formats other than PNG so I cannot ensure that it will work for all picture formats.

### Expected Output

- You should first see output related to the input's format
- You will then see the fitness score for the first cohort's fittest individual
- After this you will receive up to 7 reports depending on how long you would like the software to run
  - Each report is provided as a command-line output and contains: 
    - The number of cross-over cycles (mating cycles) completed
    - The time elapsed since the start of the program
    - The fitness value of the fittest individual of the cohort at the current cross-over cycle
  - One of these command-line reports will arrive at this interval of cross-overs
    - 1000, 5000, 10000, 20000, 50000, 100000, 200000
- Along with each command-line report, the program will save a corresponding picture within the assignment directory
  - Each picture will be named: `test<cyclecount>.png`
- For smaller pictures (15x15 - 30x30),  you can get to 10,000 cycles and three output pictures with 10-12 minutes
  - The highest cross-over cycle counts can take a couple to several hours to complete
- To end the program, either wait for it to complete (not recommended) or stop it with Ctrl+C after your desired cycle-count

## Code Commentary

I tried to name my variables, classes, and functions in a way to provide clarity without needing additional commentary. However, I have provided comments at key areas to explain functionality and purpose.

### Reference

I paraphrased code found on-line for my function transp_rectangle() on line 29. You can find the original code at: https://stackoverflow.com/a/54426778

## My Test Images

You can find the final images for each of my four test images in the folder Final-Report-Images. Each folder should contain several images. The first one to notice is "target.png"; this is the original input image which the program is trying to mimic. The rest are incremental images produced during the program's operation. These images are named "test<number_of_cross-over_cycles>.png". The worst mimic should be test1000.png and the best should be the one with the highest number of cycles. Due to time limitations, I did not run my program up to the max of 200,000 cycles for each picture, but I should have a good representation of improvement with increasing cycles for each test image.

## Basic Algorithm Description

At the start of the program, I generate num_individuals of individuals for the population. Each individual is comprised of num_rectangles of rectangles, and each of these rectangles has randomly generated dimensions, locations, colors, and opacity. The fitness of each of these is computed by comparing each individual's image (a compilation of its rectangles) is compared to the input image. The fitness is the total difference of RGB for each pixel.

Once the original cohort is created and fitness scores are set. The population's fitness scores are used to create a list of inverted-weights. This is then used for cross-overs to determine the probability that an individual will reproduce. The fittest (lowest fitness score) individuals are more likely to join in mated pairs for during cross-over. Immediately prior to cross-over, the least fit 20% are culled from the population (more explanation about this in the analysis). During cross-over, a random index is selected and then the pair of individuals swap rectangles along this index.

The new individuals resulting from the cross-over are then mutated at a rate of 0.03 or 3 out of a hundred. After this and prior to the next cycle of cross-overs, weights are recalculated based on the new individual's fitness scores. 

You will find additional description of my algorithm's components in the analysis section.

## Analysis

You can see the raw data for my analysis in the file a2-data.xlsx.

### Individual Count and Number of Rectangles

Late in the development of my program, I had the idea to start with many more random individuals in the initial cohort and then remove all of the least fit until the population size is the number that I desired for the cycles of cross-over. This allows for much greater population diversity at the onset of the program but does not have a significant performance impact. I wish I would have thought of this ealier as it significantly improves quality.

I decided on a population size of 20 individuals and 80 rectangles for each individual. This seemed to return a good balance of performance and quality. I was surprised during my testing that halving the population size from 40 to 20 didn't have as significant of an impact on quality as I would have anticipated but cut processing time in half. At a certain point, reducing the individual count is counter productive and best fitness scores can actually worsen with more time. I believe that unhelpful mutations and mating pairs can have a greater negative impact if there is not a bigger population to absorb and overwhelm them.

Reducing the rectangle count per individual can have a significant impact on performance. Halving the rectangle count from 100 to 50 cut the program's run time by 1/3 and had little impact on quality for smaller pictures. I did not experiment with pictures larger than 30x30 pixels, and I strongly suspect that the larger pictures would have required more rectangles to achieve better fitness scores at higher cross-over counts.

### Cross-Over and Culling

When I first started testing, I found that my cohorts would linger around the same average fitness regardless of the number of cross-cycles. I had used a weighted, Roullette-style methodology for creating mated pairs for cross-over which favored those with higher amounts of fitness. The problem is that I was still allowing the least fit individuals the chance to reproduce, and at the start of my program the randomly generated individuals were all fairly similar in fitness. So I introduced a 20% cull to each cohort prior to cross-over. This eliminated the least fit 20% of the individuals and dramatically improved my program. Admittedly, this 20% was an arbitrary number I chose and stuck with in order to carry out the rest of the assignment's tasks. If I had a bit more time, I would try to vary this cull percentage prior to each cross-over. Perhaps I could mimic nature and have better and worse "years" where more or less (within an acceptable range) individuals are culled.

### Mutations

During my initial testing, I only utilized 1 form of mutation. This mutation chose an individual's rectangle at random and then completely randomized that rectangle's dimensions, location, and color. The program with one mutation actually performed surprisingly well although not as well as when I introduced a full suite of mutations. The new mutations improved an individual's fitness at any given cross-over count by approximately 15%.

A very high (MR >= 0.1) rate of mutation often results in more significant improvements at the lower cross-over cycle counts, but as the population gets fitter, the higher mutation rate reduces the marginal improvement over cycles. It seems that during the start of the program when individuals have not been pressured into better fitness via selection a higher mutation rate can help some individuals get fitter more quickly. The higher rate of mutation begins to work against fitness when they begin to reduce individual fitness more often.

A very low rate (MR < 0.01) of mutation struggles to improve fitness beyond its baseline at the start of the program.

Doubling the mutation rate requires slightly more time for processing through each cycle. This results in a small time increase of approximately 0.5% for each doubling of the rate.

It seems that the ideal mutation rate falls somewhere between 0.015 and 0.05. This allows the population fitness to differentiate and improve adequately in the earlier cohorts but does not result in an excess of unhelpful, negative mutations in the later cohorts. I decided on a rate of 0.03 as it provided the best balance of performance early and late during testing.

### Diminishing marginal returns on computation

I noticed that the amount of change in fitness from one cycle to the next decreased significantly during the processing of my face image at levels above 50,000 cross-overs. I surmise that this is due to the cohort's images are getting closer to the goal and each alteration has a smaller and smaller impact to each individuals fitness score. I ran my program on an image of my face for several hours, and I imagine it would take days at its current rate to produce a substantially better picture. Perhaps a change in cross-over strategies or providing additional types of mutations would have helped at this higher level.
