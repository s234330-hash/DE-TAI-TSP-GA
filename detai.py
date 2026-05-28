import random
import math
import matplotlib
matplotlib.use('TkAgg')   # dùng TkAgg để hiện cửa sổ; đổi thành 'Agg' nếu chỉ muốn lưu file
import matplotlib.pyplot as plt


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
    # EVOLUTION + GHI LỊCH SỬ
    # =========================
    def evolution(self, generations):

        history = []
        for i in range(generations):

            self._evol_once()

            best = self._get_best_dna()
            history.append(best.SumDistances)

            if (i + 1) % 50 == 0:

                print(
                    f"Generation {i+1} "
                    f"- Best Distance: "
                    f"{best.SumDistances:.2f}"
                )

        return self._get_best_dna(), history


# ===================================
# VẼ KẾT QUẢ
# ===================================
def plot_result(ga, best, history, generations):

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.patch.set_facecolor('#0f1117')

    # ---------- Panel trái: lộ trình ----------
    ax1 = axes[0]
    ax1.set_facecolor('#0f1117')
    ax1.set_title(
        f'Generation: {generations} | Distance: {best.SumDistances:.2f}',
        color='white', fontsize=13, pad=10
    )

    xs = [ga.Cities[i].X for i in best.Genes]
    ys = [ga.Cities[i].Y for i in best.Genes]
    xs.append(xs[0])
    ys.append(ys[0])

    ax1.plot(xs, ys, color='#4fc3f7', linewidth=2, zorder=1)
    ax1.scatter(
        [c.X for c in ga.Cities],
        [c.Y for c in ga.Cities],
        color='#ff7043', s=60, zorder=3,
        edgecolors='white', linewidths=0.8
    )

    for i, city in enumerate(ga.Cities):
        ax1.annotate(
            str(i), (city.X, city.Y),
            textcoords='offset points', xytext=(5, 5),
            color='#cfd8dc', fontsize=8
        )

    ax1.tick_params(colors='#607d8b')
    for spine in ax1.spines.values():
        spine.set_edgecolor('#37474f')
    ax1.xaxis.label.set_color('#90a4ae')
    ax1.yaxis.label.set_color('#90a4ae')

    # ---------- Panel phải: biểu đồ hội tụ ----------
    ax2 = axes[1]
    ax2.set_facecolor('#0f1117')
    ax2.set_title(
        'Khoảng cách tốt nhất theo thế hệ',
        color='white', fontsize=13, pad=10
    )
    ax2.plot(history, color='#66bb6a', linewidth=1.5)
    ax2.fill_between(range(len(history)), history, alpha=0.15, color='#66bb6a')
    ax2.set_xlabel('Thế hệ', color='#90a4ae')
    ax2.set_ylabel('Khoảng cách', color='#90a4ae')
    ax2.tick_params(colors='#607d8b')
    for spine in ax2.spines.values():
        spine.set_edgecolor('#37474f')

    plt.tight_layout(pad=2)
    plt.show()


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
        input("Nhập tỉ lệ đột biến (vd: 0.03): ")
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

    best, history = ga.evolution(GENERATIONS)

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

    # =========================
    # HIỆN HÌNH
    # =========================
    plot_result(ga, best, history, GENERATIONS)
