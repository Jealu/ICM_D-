"""NSGA-II related functions"""

import functools
from Population import *
import random


class NSGA2Utils(object):

    def __init__(self, problem, num_of_individuals, mutation_strength=0.2, num_of_genes_to_mutate=5,
                 num_of_tour_particips=2):

        self.problem = problem
        self.num_of_individuals = num_of_individuals
        self.mutation_strength = mutation_strength
        self.number_of_genes_to_mutate = num_of_genes_to_mutate
        self.num_of_tour_particips = num_of_tour_particips

    def fast_nondominated_sort(self, population):
        population.fronts.append([])
        for individual in population:
            individual.domination_count = 0
            individual.dominated_solutions = set()

            for other_individual in population:
                if individual.dominates(other_individual):
                    individual.dominated_solutions.add(other_individual)
                elif other_individual.dominates(individual):
                    individual.domination_count += 1
            if individual.domination_count == 0:
                population.fronts[0].append(individual)
                individual.rank = 0
        i = 0
        while len(population.fronts[i]) > 0:
            temp = []
            for individual in population.fronts[i]:
                for other_individual in individual.dominated_solutions:
                    other_individual.domination_count -= 1
                    if other_individual.domination_count == 0:
                        other_individual.rank = i + 1
                        temp.append(other_individual)
            i = i + 1
            population.fronts.append(temp)

    def __sort_objective(self, val1, val2, m):
        return cmp(val1.objectives[m], val2.objectives[m])

    def calculate_crowding_distance(self, front):
        if len(front) > 0:
            solutions_num = len(front)
            for individual in front:
                individual.crowding_distance = 0

            for m in range(len(front[0].objectives)):
                front = sorted(front, cmp=functools.partial(self.__sort_objective, m=m))
                front[0].crowding_distance = self.problem.max_objectives[m]
                front[solutions_num - 1].crowding_distance = self.problem.max_objectives[m]
                for index, value in enumerate(front[1:solutions_num - 1]):
                    front[index].crowding_distance = (front[index + 1].crowding_distance - front[
                        index - 1].crowding_distance) / (1+self.problem.max_objectives[m] - self.problem.min_objectives[
                        m])

    def crowding_operator(self, individual, other_individual):
        if (individual.rank < other_individual.rank) or \
                ((individual.rank == other_individual.rank) and (
                        individual.crowding_distance > other_individual.crowding_distance)):
            return 1
        else:
            return -1

    def create_initial_population(self):
        population = Population()
        for _ in range(self.num_of_individuals):
            individual = self.problem.generateIndividual()
            self.problem.calculate_objectives(individual)
            population.population.append(individual)
        return population

    def create_children(self, population):
        children = []
        while len(children) < len(population):
            participants = []
            for p in population:
                exist = False
                for pp in participants:
                    if p.features == pp.features:
                        exist = True
                        break
                if not exist:
                    participants.append(p)
            parent1 = self.__tournament(participants)
            parent2 = self.__tournament(participants)
            child1, child2 = self.__crossover(parent1, parent2)
            self.mutate(child1)
            self.mutate(child2)
            self.problem.calculate_objectives(child1)
            self.problem.calculate_objectives(child2)
            children.append(child1)
            children.append(child2)

        return children

    def __crossover(self, individual1, individual2):
        child1 = self.problem.generateIndividual()
        child2 = self.problem.generateIndividual()
        bloxk_index = [0, 94, 155, 250, 294, 385, 424, 660, 788, 868]
        swap_block = random.sample([0,1,2,3,4,5,6,7,8], 1)
        swap_index = [bloxk_index[swap_block[0]], bloxk_index[swap_block[0]+1]]
        child1.features = [gene for gene in individual1.features]
        child1.features[swap_index[0]:swap_index[1]] = [gene for gene in individual2.features[swap_index[0]:swap_index[1]]]
        child2.features = [gene for gene in individual2.features]
        child2.features[swap_index[0]:swap_index[1]] = [gene for gene in individual1.features[swap_index[0]:swap_index[1]]]
        return child1, child2

    def mutate(self, child):
        genes_to_mutate = random.sample(range(0, len(child.features)), 120)
        for gene in genes_to_mutate:
            if child.features[gene] > 0:
                if random.random()>0.5:
                    child.features[gene] += 1
                else:
                    child.features[gene] -= 1
            else:
                if random.random()>0.85:
                    child.features[gene] += 1
        genes_to_mutate = random.sample(range(0, len(child.features)-1), 80)
        for gene in genes_to_mutate:
            if child.features[gene] > 0 and child.features[gene+1]>0:
                if random.random()>0.5:
                    child.features[gene]+= 1
                    child.features[gene + 1] -= 1
                else:
                    child.features[gene] -= 1
                    child.features[gene + 1] += 1

    def __tournament(self, population):
        # participants = random.sample(population, self.num_of_tour_particips)
        # best = None
        # for participant in participants:
        #     if best is None or self.crowding_operator(participant, best) == 1:
        #         best = participant
        # return best
        if len(population) == 1:
            return population[0]
        participants = random.sample(population, self.num_of_tour_particips)
        if participants[0].dominates(participants[1]):
            return participants[0]
        return participants[1]
