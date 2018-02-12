from Individual import *
import random
import functools
import math


class NSGA_problem(object):
        def __init__(self, scenario):
            self.scenario = scenario
            self.max_objectives = [None, None]
            self.min_objectives = [None, None]
            self.problem_type = None
            f = open('input.txt', 'r')
            gene_s = f.readlines()
            self.gene = [int(g) for g in gene_s]

        def __dominates(self, individual2, individual1):
            worse_than_other = self.f1(individual1) <= self.f1(individual2) and self.f2(individual1) <= self.f2(
                individual2)
            return worse_than_other

        def generateIndividual(self):
            individual = Individual()
            individual.features = [i for i in self.gene]
            individual.dominates = functools.partial(self.__dominates, individual1=individual)
            self.calculate_objectives(individual)
            return individual

        def calculate_objectives(self, individual):
            individual.objectives = []
            individual.objectives.append(self.f1(individual))
            individual.objectives.append(self.f2(individual))
            for i in range(2):
                if self.min_objectives[i] is None or individual.objectives[i] < self.min_objectives[i]:
                    self.min_objectives[i] = individual.objectives[i]
                if self.max_objectives[i] is None or individual.objectives[i] > self.max_objectives[i]:
                    self.max_objectives[i] = individual.objectives[i]
            # print individual.objectives[0], individual.objectives[1]

        def f1(self, individual):
            return 1*sum(individual.features)+len(individual.features)-individual.features.count(0)

        def f2(self, individual):
            flows = self.scenario.track_list
            success = 0
            super_chargers_slots = [[l for l in individual.features] for i in xrange(48)]
            for f in flows:
                super_slot = f.time_slot-1
                for l in f.feasible_super_locations:
                    if super_chargers_slots[super_slot][l] > 0:
                        super_chargers_slots[super_slot][l] -= 1
                        success += 1
                        break
            return len(flows)-success