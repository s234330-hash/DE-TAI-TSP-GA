# DE-TAI-TSP-GA

## 1. Giới thiệu đề tài

Traveling Salesman Problem (TSP) là một bài toán tối ưu nổi tiếng trong lĩnh vực Trí tuệ nhân tạo và Khoa học máy tính.

Bài toán yêu cầu:
- Một người bán hàng phải đi qua tất cả các thành phố đúng một lần
- Sau đó quay lại thành phố xuất phát
- Tổng quãng đường phải là ngắn nhất

Do số lượng trường hợp tăng rất nhanh khi số thành phố lớn, việc tìm lời giải tối ưu bằng brute force sẽ tốn rất nhiều thời gian.

Trong project này, thuật toán Genetic Algorithm (GA) được sử dụng để tìm nghiệm gần tối ưu cho bài toán TSP.

---

# 2. Mục tiêu đề tài

- Tìm đường đi ngắn nhất giữa các thành phố
- Áp dụng thuật toán Genetic Algorithm
- Hiểu cơ chế:
  - Selection
  - Crossover
  - Mutation
- Mô phỏng quá trình tiến hóa trong AI

---

# 3. Công nghệ sử dụng

- Python
- Genetic Algorithm
- Math Library
- Random Library

---

# 4. Phương pháp thực hiện

## 4.1 Khởi tạo thành phố

Các thành phố được sinh ngẫu nhiên trên mặt phẳng tọa độ 2D.

Mỗi thành phố gồm:
- Tọa độ X
- Tọa độ Y

Ví dụ:

```python
class City:
    def __init__(self, x, y):
        self.X = x
        self.Y = y
```

---

## 4.2 Biểu diễn cá thể (DNA)

Mỗi cá thể đại diện cho một lộ trình đi qua các thành phố.

Ví dụ:

```bash
[3, 1, 8, 7, 10]
```

---

## 4.3 Hàm thích nghi (Fitness Function)

Độ thích nghi được đánh giá bằng:
- Tổng khoảng cách của toàn bộ lộ trình

Khoảng cách càng nhỏ:
- cá thể càng tốt

Công thức khoảng cách Euclid:

d = √((x2 - x1)^2 + (y2 - y1)^2)

---

## 4.4 Selection

Thuật toán chọn các cá thể tốt hơn để sinh ra thế hệ mới.

Các cá thể có khoảng cách ngắn:
- có xác suất được chọn cao hơn

---

## 4.5 Crossover

Hai cá thể cha mẹ được kết hợp để tạo ra cá thể con.

Ví dụ:

Parent 1:
```bash
[1,2,3,4,5]
```

Parent 2:
```bash
[3,5,1,2,4]
```

Child:
```bash
[1,2,3,5,4]
```

---

## 4.6 Mutation

Mutation giúp:
- tránh rơi vào local optimum
- tăng tính đa dạng quần thể

Phương pháp mutation:
- hoán đổi vị trí ngẫu nhiên giữa 2 thành phố

---

## 4.7 Evolution

Quần thể sẽ:
- Selection
- Crossover
- Mutation

qua nhiều thế hệ để tìm lời giải tốt hơn.

---

# 5. Kết quả chương trình

Sau nhiều thế hệ tiến hóa:
- thuật toán tìm được lộ trình tối ưu gần đúng
- tổng khoảng cách giảm đáng kể

Ví dụ kết quả:

```bash
Khoảng cách tốt nhất: 2777.54
Lộ trình: [3, 1, 8, 7, 10, 5, 4, ...]
```

---

# 6. Ưu điểm

- Tìm nghiệm nhanh
- Hiệu quả với bài toán lớn
- Dễ mở rộng

---

# 7. Nhược điểm

- Không đảm bảo nghiệm tối ưu tuyệt đối
- Phụ thuộc:
  - mutation rate
  - population size
  - số generation

---

# 8. Kết luận

Project đã áp dụng thành công Genetic Algorithm để giải bài toán Traveling Salesman Problem.

Thuật toán cho kết quả tốt trong thời gian ngắn và thể hiện rõ nguyên lý tiến hóa trong AI.

---

# 9. Cách chạy chương trình

```bash
python ga_tsp.py
```

---

# 10. GitHub Repository

https://github.com/s234330-hash/DE-TAI-TSP-GA
