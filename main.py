# Dustin Mays
# CS 410 - Assignment 2: Genetic Algorithms

from PIL import Image, ImageDraw
import random
import copy
import time
import sys
import numpy as np

inputImage = sys.argv[1]
im = Image.open(inputImage)
print("Input image: ", inputImage, " -> Format: ", im.format, im.size, im.mode)

pix = im.load()
original = []
for i in range(0, im.size[1]):
    for j in range(0, im.size[0]):
        original.append(pix[j, i])

def compare_colors(color1, color2):
    total_difference = 0
    for i in range(0, 4):
        total_difference = total_difference + abs(color1[i] - color2[i])
    return total_difference

# Add a rectangle to Individual's overall image
# This was inspired heavily from: https://stackoverflow.com/a/54426778
def transp_rectangle(img, xy, **kwargs):
    transp = Image.new('RGBA', img.size, (0,0,0,0)) # temp drawing image
    draw = ImageDraw.Draw(transp, "RGBA") # create draw object on transp image
    draw.rectangle(xy, **kwargs)
    # Alpha-composite two images together
    img.paste(Image.alpha_composite(img, transp))

class Rectangle:
    def __init__(self):
        self.xy = [0,0,0,0]
        self.color = [0,0,0,0]
        self.xy[0] = random.randint(0,im.size[0])
        self.xy[1] = random.randint(0,im.size[1])
        self.xy[2] = random.randint(0,im.size[0])
        self.xy[3] = random.randint(0,im.size[1])
        self.color[0] = random.randint(0,255)
        self.color[1] = random.randint(0,255)
        self.color[2] = random.randint(0,255)
        self.color[3] = random.randint(0,200)


    def copy_from(self, other):
        self.xy = other.xy
        self.color = other.color

    # Utilized for mutations
    def change_rand_color(self):
        index = random.randint(0,2)
        self.color[index] = random.randint(0, 255)

    # Utilized for mutations
    def change_rand_xdim(self):
        index = random.randint(0,3)
        self.xy[index] = random.randint(0, im.size[0])

    # Randomize a rectangle's shape and color
    def completely_random(self):
        self.xy[0] = random.randint(0, im.size[0])
        self.xy[1] = random.randint(0, im.size[1])
        self.xy[2] = random.randint(0, im.size[0])
        self.xy[3] = random.randint(0, im.size[1])
        self.color[0] = random.randint(0, 255)
        self.color[1] = random.randint(0, 255)
        self.color[2] = random.randint(0, 255)
        self.color[3] = random.randint(0, 200)

    def swap_box(self, other):
        temp0 = self.xy[0]
        temp1 = self.xy[1]
        temp2 = self.xy[2]
        temp3 = self.xy[3]
        self.xy[0] = other.xy[0]
        self.xy[1] = other.xy[1]
        self.xy[2] = other.xy[2]
        self.xy[3] = other.xy[3]
        other.xy[0] = temp0
        other.xy[1] = temp1
        other.xy[2] = temp2
        other.xy[3] = temp3

    def swap_color(self, other):
        temp0 = self.color[0]
        temp1 = self.color[1]
        temp2 = self.color[2]
        temp3 = self.color[3]
        self.color[0] = other.color[0]
        self.color[1] = other.color[1]
        self.color[2] = other.color[2]
        self.color[3] = other.color[3]
        other.color[0] = temp0
        other.color[1] = temp1
        other.color[2] = temp2
        other.color[3] = temp3

    def scramble_color(self):
        temp0 = self.color[0]
        temp1 = self.color[1]
        temp2 = self.color[2]
        temp3 = self.color[3]
        self.color[2] = temp0
        self.color[1] = temp2
        self.color[0] = temp3
        self.color[3] = temp1

    def randomize_all_colors(self):
        self.color[0] = random.randint(0, 255)
        self.color[1] = random.randint(0, 255)
        self.color[2] = random.randint(0, 255)
        self.color[3] = random.randint(0, 200)

    def randomize_dimensions(self):
        self.xy[0] = random.randint(0, im.size[0])
        self.xy[1] = random.randint(0, im.size[1])
        self.xy[2] = random.randint(0, im.size[0])
        self.xy[3] = random.randint(0, im.size[1])

class Individual:
    num_rectangles = 60

    # default constructor: assigns values randomly
    def __init__(self):
        self.rectangles = []
        for i in range(self.num_rectangles):
            self.rectangles.append(Rectangle()) # Creates random rectangles for initial individuals
        self.eval_fitness()

    # Recreate image from rectangles
    def regenerate_image(self):
        self.image = Image.new("RGBA", (im.size[0], im.size[1]), (255, 255, 255, 70))
        for r in self.rectangles:
            transp_rectangle(self.image, r.xy, fill=(r.color[0],r.color[1],r.color[2],r.color[3]))

    def output_individual(self, path):
        self.image.save(path)

    # mutation runner
    # mutate_dice => dictates whether a mutation occurs based on rate
    # Potential mutations: swap alleles between two, insert
    def mutate(self):
        mutatation_type = -1
        mutate_dice = random.randint(1,200)
        if mutate_dice <= 5:
            mutatation_type = random.randint(0,7)
        if mutatation_type == 0:
            self.color_swap()
        if mutatation_type == 1:
            self.color_scramble()
        if mutatation_type == 2:
            self.random_color()
        if mutatation_type == 3:
            self.random_box()
        if mutatation_type == 4:
            self.box_swap()
        if mutatation_type == 5:
            self.complete_random_mutate()
        if mutatation_type == 6:
            self.mix_rect_order()
        if mutate_dice == 20:
            self.complete_random_mutate()

    def color_swap(self):
        pair = np.random.choice(self.rectangles, size=2, replace=False)
        pair[0].swap_color(pair[1])

    def color_scramble(self):
        index = random.randint(0, self.num_rectangles - 1)
        self.rectangles[index].scramble_color()

    def random_color(self):
        i = random.randint(0, 1)
        index = random.randint(0, self.num_rectangles - 1)
        if i == 0:
            self.rectangles[index].change_rand_color()
        else:
            self.rectangles[index].randomize_all_colors()

    def random_box(self):
        index = random.randint(0, self.num_rectangles - 1)
        self.rectangles[index].randomize_dimensions()

    def box_swap(self):
        pair = np.random.choice(self.rectangles, size=2, replace=False)
        pair[0].swap_box(pair[1])

    def mix_rect_order(self):
        random.shuffle(self.rectangles)

    def complete_random_mutate(self):
        rectangle_index = random.randint(0, self.num_rectangles - 1)
        self.rectangles[rectangle_index].completely_random()

    # evaluate the fitness of an individual
    # generate an image for the individual and compare pixel-by-pixel to input
    # fitness is an int that is the sum of all pixel-color differences
    def eval_fitness(self):
        self.regenerate_image()
        testPix = self.image.load()
        testPixList = []
        for i in range(0, im.size[1]):
            for j in range(0, im.size[0]):
                testPixList.append(testPix[j, i])
        orig = original[0]
        test = testPixList[0]
        total_difference = 0
        for i in range(0, len(original)):
            orig = original[i]
            test = testPixList[i]
            total_difference = total_difference + compare_colors(orig, test)
        self.fitness = total_difference

class Population:
    num_individuals = 16 # Keep Even

    # Default, randomize constructor for population
    # Runs once and generates num_individuals with random blocks of random size, position, and color
    # Also runs functions to determine relative fitness of each individual for mating purposes
    def __init__(self):
        self.temp_weights = []
        self.weights = []
        self.individuals = []

        for i in range(0, 1000):
            self.individuals.append(Individual())
        self.individuals.sort(key=lambda x: x.fitness)
        for i in range(0, 1000 - self.num_individuals):
            self.individuals.pop()
        for i in self.individuals:
            self.temp_weights.append(i.fitness)
        self.invert_weights(self.num_individuals)

        if len(self.weights) != len(self.individuals):
            print("Weight count does NOT equal individual count")

    def best_fitness(self):
        best_performance = self.individuals[0].fitness
        number = len(self.individuals)
        for i in range(1, number):
            if self.individuals[i].fitness < best_performance:
                best_performance = self.individuals[i].fitness
        return best_performance

    def top_performer(self):
        self.individuals.sort(key=lambda x: x.fitness)
        return self.individuals[0]

    # remove lowest ~20% of individuals prior to mating
    def cull_herd(self):
        cull_weights = [0.2, 0.6, 0.2]
        temp = [4, 5, 6]
        prob = np.random.choice(temp, p=cull_weights)
        amount_to_cull = int(1/prob * self.num_individuals)
        self.individuals.sort(key=lambda x: x.fitness)
        for i in range(0, amount_to_cull): # cull worst ~1/5
            self.individuals.pop()
        self.adjust_weights(len(self.individuals))

    # adjust relative weighting of each individual's fitness
    # weights used for cross-over
    def adjust_weights(self, pop_size):
        self.temp_weights.clear()
        self.weights.clear()
        for i in range(0, pop_size):
            self.temp_weights.append(self.individuals[i].fitness)
        self.invert_weights(pop_size)

    def invert_weights(self, pop_size):
        sum_of_weights = 0
        for w in range(0, pop_size):
            self.weights.append(1 / self.temp_weights[w])
            sum_of_weights = sum_of_weights + self.weights[w]
        for w in range(0, pop_size):
            self.weights[w] = self.weights[w] / sum_of_weights

    # Using random index, swap mated pairs rectangles
    # Then call mutate function
    # Evaluate population fitness and remove/cull lowest performing 20%
    def cross_over(self):
        mated_pairs = self.generate_mates()
        # Run a mate/swap function for each pair
        # Create a temporary list of these new individuals
        # Overwrite individuals[] with temp list when loop is completed
        temp_individuals = []
        for pair in mated_pairs:
            num_rect = pair[0].num_rectangles
            index = random.randint(1, num_rect - 1)
            temp0 = copy.deepcopy(pair[0])
            temp1 = copy.deepcopy(pair[1])
            for i in range(0, index):
                temp0.rectangles[i].copy_from(pair[1].rectangles[i])
            for i in range(index, num_rect):
                temp1.rectangles[i].copy_from(pair[0].rectangles[i])
            pair[0] = temp1
            pair[1] = temp0
            temp_individuals.append(pair[0])
            temp_individuals.append(pair[1])
        self.individuals.clear()
        self.individuals = temp_individuals
        for i in self.individuals:
            i.mutate()
            i.eval_fitness()
        self.cull_herd()


    # generates a list of paired individuals for mating/cross-over
    # pairs are weighted for best fitness
    # so individuals with lowest(best) fitness value may cross-over more than once
    def generate_mates(self):
        mated_pairs = []
        pair_count = int(self.num_individuals / 2)
        for i in range(0, pair_count):
            mated_pairs.append(np.random.choice(self.individuals, size=2, replace=False, p=self.weights))
        if len(mated_pairs) != int(self.num_individuals / 2):
            print("Num of Individuals * 1/2 does NOT match Mated Pair count")
        return mated_pairs

def run_test():
    pop = Population()
    print("Fitness of Best of First Cohort: ", pop.best_fitness())
    top = pop.top_performer()
    start = time.time()
    for i in range(0, 250001):  # should run for 2-4 hours depending on image's size
        if i % 100 == 0:
            print("Cross-Over: ", i)
        pop.cross_over()
        if i == 1000:
            print("Time for 1000 Cross-overs: ", time.time() - start)
            top = pop.top_performer()
            print("Best individual's fitness @ 1000 Cross-overs: ", top.fitness)
            top.output_individual("test1000.png")
        if i == 5000:
            print("Time for 5000 Cross-overs: ", time.time() - start)
            top = pop.top_performer()
            print("Best individual's fitness @ 5000 Cross-overs: ", top.fitness)
            top.output_individual("test5000.png")
        if i == 10000:
            print("Time for 10000 Cross-overs: ", time.time() - start)
            top = pop.top_performer()
            print("Best individual's fitness @ 10000 Cross-overs: ", top.fitness)
            top.output_individual("test10000.png")
        if i == 20000:
            print("Time for 20000 Cross-overs: ", time.time() - start)
            top = pop.top_performer()
            print("Best individual's fitness @ 20000 Cross-overs: ", top.fitness)
            top.output_individual("test20000.png")
        if i == 50000:
            print("Time for 50000 Cross-overs: ", time.time() - start)
            top = pop.top_performer()
            print("Best individual's fitness @ 50000 Cross-overs: ", top.fitness)
            top.output_individual("test50000.png")
        if i == 100000:
            print("Time for 100000 Cross-overs: ", time.time() - start)
            top = pop.top_performer()
            print("Best individual's fitness @ 100000 Cross-overs: ", top.fitness)
            top.output_individual("test100000.png")
        if i == 200000:
            print("Time for 200000 Cross-overs: ", time.time() - start)
            top = pop.top_performer()
            print("Best individual's fitness @ 200000 Cross-overs: ", top.fitness)
            top.output_individual("test200000.png")
        if i == 250000:
            print("Time for 250000 Cross-overs: ", time.time() - start)
            top = pop.top_performer()
            print("Best individual's fitness @ 250000 Cross-overs: ", top.fitness)
            top.output_individual("test250000.png")
run_test()
