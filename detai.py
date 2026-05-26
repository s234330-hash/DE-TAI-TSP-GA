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

            total += distances[
                self.Genes[i]
            ][
                self.Genes[i + 1]
            ]

        total += distances[
            self.Genes[-1]
        ][
            self.Genes[0]
        ]

        return total

    def cross_over(self, partner, split_point, distances):

        child = self.Genes[:split_point]

        for gene in partner.Genes:

            if gene not in child:
                child.append(gene)

        return DNA(child, distances)


class GA:

    def __init__(self,
                 n_cities,
                 n_population,
                 mutation_rate):

        self.NCities = n_cities
        self.NPopulation = n_population
        self.MutationRate = mutation_rate

        self.Cities = []
        self.Population = []

        self._distances = []

        self._rnd = random.Random()

    # =========================
    # NHẬP THÀNH PHỐ THỦ CÔNG
    # =========================
    def init_cities_manual(self):

        print("\n=== NHẬP TỌA ĐỘ THÀNH PHỐ ===\n")

        for i in range(self.NCities):

            x = int(input(f"Nhập X thành phố {i}: "))
            y = int(input(f"Nhập Y thành phố {i}: "))

            self.Cities.append(City(x, y))

        self._create_distance_matrix()

    # =========================
    # RANDOM THÀNH PHỐ
    # =========================
    def init_cities_random(self, width, height):

        for _ in range(self.NCities):

            x = self._rnd.randint(0, width)
            y = self._rnd.randint(0, height)

            self.Cities.append(City(x, y))

        self._create_distance_matrix()

    # =========================
    # TẠO MA TRẬN KHOẢNG CÁCH
    # =========================
    def _create_distance_matrix(self):

        self._distances = [

            [0 for _ in range(self.NCities)]

            for _ in range(self.NCities)
        ]

        for i in range(self.NCities):

            for j in range(self.NCities):

                dx = self.Cities[i].X - self.Cities[j].X
                dy = self.Cities[i].Y - self.Cities[j].Y

                self._distances[i][j] = math.sqrt(
                    dx * dx + dy * dy
                )

    # =========================
    # KHỞI TẠO POPULATION
    # =========================
    def init_population(self):

        for _ in range(self.NPopulation):

            genes = list(range(self.NCities))

            self._rnd.shuffle(genes)

            dna = DNA(
                genes,
                self._distances
            )

            self.Population.append(dna)

    # =========================
    # TÌM DNA TỐT NHẤT
    # =========================
    def _get_best_dna(self):

        best = self.Population[0]

        for dna in self.Population:

            if dna.SumDistances < best.SumDistances:
                best = dna

        return best

    # =========================
    # TẠO MATING POOL
    # =========================
    def _create_mating_pool(self):

        pool = []

        best = self._get_best_dna()

        for i in range(len(self.Population)):

            fitness = int(
                math.floor(
                    best.SumDistances * 100 /
                    self.Population[i].SumDistances
                )
            )

            fitness = max(1, fitness)

            for _ in range(fitness):
                pool.append(i)

        return pool

    # =========================
    # MUTATION
    # =========================
    def _mutate(self, dna):

        if self._rnd.random() < self.MutationRate:

            i1 = self._rnd.randint(
                0,
                len(dna.Genes) - 1
            )

            i2 = i1

            while i2 == i1:

                i2 = self._rnd.randint(
                    0,
                    len(dna.Genes) - 1
                )

            dna.Genes[i1], dna.Genes[i2] = (
                dna.Genes[i2],
                dna.Genes[i1]
            )

            dna.SumDistances = dna.calculate_distance(
                self._distances
            )

    # =========================
    # EVOLUTION 1 LẦN
    # =========================
    def _evol_once(self):

        pool = self._create_mating_pool()

        best = self._get_best_dna()

        # GIỮ ELITE
        self.Population[0] = DNA(
            best.Genes[:],
            self._distances
        )

        for i in range(1, len(self.Population)):

            p1 = self.Population[
                pool[
                    self._rnd.randint(
                        0,
                        len(pool) - 1
                    )
                ]
            ]

            p2 = self.Population[
                pool[
                    self._rnd.randint(
                        0,
                        len(pool) - 1
                    )
                ]
            ]

            split_point = self._rnd.randint(
                1,
                len(self.Cities) - 1
            )

            child = p1.cross_over(
                p2,
                split_point,
                self._distances
            )

            self._mutate(child)

            self.Population[i] = child

    # =========================
    # EVOLUTION
    # =========================
    def evolution(self, generations):

        for i in range(generations):

            self._evol_once()

            if (i + 1) % 50 == 0:

                best = self._get_best_dna()

                print(
                    f"Generation {i+1} "
                    f"- Best Distance: "
                    f"{best.SumDistances:.2f}"
                )

        return self._get_best_dna()


# ===================================
# MAIN
# ===================================
if __name__ == "__main__":

    print("=== GENETIC ALGORITHM CHO TSP ===\n")

    N_CITIES = int(
        input("Nhập số thành phố: ")
    )

    N_POPULATION = int(
        input("Nhập kích thước dân số: ")
    )

    MUTATION_RATE = float(
        input("Nhập tỉ lệ đột biến: ")
    )

    GENERATIONS = int(
        input("Nhập số thế hệ tiến hóa: ")
    )

    print("\n1. Random thành phố")
    print("2. Nhập thủ công")

    mode = int(
        input("\nChọn chế độ: ")
    )

    ga = GA(
        N_CITIES,
        N_POPULATION,
        MUTATION_RATE
    )

    # =========================
    # RANDOM MODE
    # =========================
    if mode == 1:

        WIDTH = int(
            input("Nhập chiều rộng: ")
        )

        HEIGHT = int(
            input("Nhập chiều cao: ")
        )

        ga.init_cities_random(
            WIDTH,
            HEIGHT
        )

    # =========================
    # MANUAL MODE
    # =========================
    else:

        ga.init_cities_manual()

    ga.init_population()

    print("\nĐang chạy Genetic Algorithm...\n")

    best = ga.evolution(GENERATIONS)

    print("\n=== KẾT QUẢ ===")

    print(
        f"Khoảng cách tốt nhất: "
        f"{best.SumDistances:.2f}"
    )

    print(
        f"Lộ trình tốt nhất: "
        f"{best.Genes}"
    )

    print("\n=== TỌA ĐỘ THÀNH PHỐ ===")

    for i, city in enumerate(ga.Cities):

        print(
            f"City {i}: "
            f"({city.X}, {city.Y})"
        )
