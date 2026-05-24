import random
import math


class City:
    def __init__(self, x, y):
        self.X = x
        self.Y = y


class DNA:
    def __init__(self, genes, distances):
        self.Genes = genes[:]
        self.SumDistances = self.calculate_distance(distances)

    def calculate_distance(self, distances):
        total = 0

        for i in range(len(self.Genes) - 1):
            total += distances[self.Genes[i]][self.Genes[i + 1]]

        total += distances[self.Genes[-1]][self.Genes[0]]

        return total

    def cross_over(self, partner, split_point, distances):
        child = self.Genes[:split_point]

        for gene in partner.Genes:
            if gene not in child:
                child.append(gene)

        return DNA(child, distances)


class GA:
    def __init__(self, n_cities, n_population, mutation_rate):

        self.NCities = n_cities
        self.NPopulation = n_population
        self.MutationRate = mutation_rate

        self.Cities = []
        self.Population = []

        self._distances = []
        self._rnd = random.Random()

    def init_cities(self, width, height):

        for _ in range(self.NCities):

            x = self._rnd.randint(0, width)
            y = self._rnd.randint(0, height)

            self.Cities.append(City(x, y))

        self._create_distance_matrix()

    def _create_distance_matrix(self):

        self._distances = [
            [0 for _ in range(self.NCities)]
            for _ in range(self.NCities)
        ]

        for i in range(self.NCities):
            for j in range(self.NCities):

                dx = self.Cities[i].X - self.Cities[j].X
                dy = self.Cities[i].Y - self.Cities[j].Y

                self._distances[i][j] = math.sqrt(dx * dx + dy * dy)

    def init_population(self):

        for _ in range(self.NPopulation):

            genes = list(range(self.NCities))

            self._rnd.shuffle(genes)

            dna = DNA(genes, self._distances)

            self.Population.append(dna)

    def _get_best_dna(self):

        best = self.Population[0]

        for dna in self.Population:

            if dna.SumDistances < best.SumDistances:
                best = dna

        return best

    def _create_mating_pool(self):

        f_proportion = []

        best_dna = self._get_best_dna()

        for i in range(len(self.Population)):

            p = int(
                math.floor(
                    best_dna.SumDistances
                    * 100.0 /
                    self.Population[i].SumDistances
                )
            )

            p = max(1, p)

            for _ in range(p):
                f_proportion.append(i)

        return f_proportion

    def _mutate(self, dna):

        for i in range(len(dna.Genes)):

            r = self._rnd.random()

            if r < self.MutationRate:

                i1 = self._rnd.randint(0, len(self.Cities) - 1)

                i2 = self._rnd.randint(0, len(self.Cities) - 1)

                dna.Genes[i1], dna.Genes[i2] = (
                    dna.Genes[i2],
                    dna.Genes[i1]
                )

        dna.SumDistances = dna.calculate_distance(self._distances)

    def _evol_once(self):

        pool = self._create_mating_pool()

        self.Population[0] = self._get_best_dna()

        for i in range(1, len(self.Population)):

            p1 = self.Population[
                pool[self._rnd.randint(0, len(pool) - 1)]
            ]

            p2 = self.Population[
                pool[self._rnd.randint(0, len(pool) - 1)]
            ]

            split_point = self._rnd.randint(
                1,
                len(self.Cities) - 1
            )

            new_dna = p1.cross_over(
                p2,
                split_point,
                self._distances
            )

            self._mutate(new_dna)

            self.Population[i] = new_dna

    def evolution(self, times):

        for _ in range(times):
            self._evol_once()

        dna = self._get_best_dna()

        print(f"Evolution {times}: {dna.Genes}")

        return dna


if __name__ == "__main__":

    N_CITIES = 20
    N_POPULATION = 100
    MUTATION_RATE = 0.01

    WIDTH = 800
    HEIGHT = 600

    GENERATIONS = 500

    ga = GA(
        N_CITIES,
        N_POPULATION,
        MUTATION_RATE
    )

    ga.init_cities(WIDTH, HEIGHT)

    ga.init_population()

    print(f"Chạy Genetic Algorithm cho TSP với {N_CITIES} thành phố...")

    best = ga.evolution(GENERATIONS)

    print(f"Khoảng cách tốt nhất: {best.SumDistances}")

    print(f"Lộ trình: {best.Genes}")
