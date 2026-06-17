# 🎮 Dự án Cờ Caro AI (Caro AI PRO)

Chào mừng bạn đến với dự án **Caro AI PRO**! Đây là một trò chơi cờ Caro (phiên bản 4 quân liên tiếp thắng) được xây dựng bằng ngôn ngữ lập trình Python, tích hợp giao diện đồ họa đẹp mắt và động cơ trí tuệ nhân tạo (AI Engine) thông minh sử dụng thuật toán **Minimax** và **Alpha-Beta Pruning** kết hợp các kỹ thuật tối ưu hóa nâng cao trong lý thuyết trò chơi.

---

## 🌟 Tính Năng Nổi Bật

- 🎨 **Giao diện Pygame Cao Cấp (GUI)**:
  - Thiết kế hiện đại theo phong cách tối giản (Glassmorphism & Dracula Palette).
  - Tích hợp Menu lựa chọn đa dạng chế độ chơi.
  - Dashboard hiển thị thông tin trận đấu theo thời gian thực (thông số AI, thời gian trận đấu, lịch sử lượt đi).
  - Hỗ trợ đổi chế độ chơi nhanh trực tiếp từ bảng điều khiển trong game.
  - Đồ họa mượt mà, xử lý đa luồng (Multi-threading) giúp giao diện không bị giật/lag khi AI đang tính toán nước đi.
- 💻 **Giao diện Dòng lệnh (Console UI)**:
  - Giao diện text sắc nét với màu sắc ANSI sống động.
  - Phù hợp để chạy nhanh trên máy chủ hoặc thiết bị không có màn hình GUI.
- 🧠 **Trí Tuệ Nhân Tạo (AI Engine) Siêu Việt**:
  - **Minimax**: Thuật toán duyệt đệ quy cơ bản.
  - **Alpha-Beta Pruning**: Cắt tỉa nhánh cận tối ưu giúp giảm số node phải duyệt từ hàm mũ xuống còn một phần nhỏ.
  - **Zobrist Hashing & Transposition Table (Bảng chuyển vị)**: Lưu vết trạng thái bàn cờ đã được duyệt để tránh tính toán lại.
  - **Beam Search (Tìm kiếm chùm)**: Giới hạn bề rộng tìm kiếm nâng cao để kiểm soát sự bùng nổ tổ hợp trên bàn cờ kích thước lớn.
  - **Move Ordering**: Ưu tiên duyệt các nước đi gần quân cờ hiện tại và chấm điểm sơ bộ để kích hoạt cắt tỉa Alpha-Beta sớm nhất.
  - **Iterative Deepening**: Tìm kiếm sâu dần có kiểm soát thời gian thực tế, tự động dừng khi chạm ngưỡng thời gian tối đa cấu hình.
  - **Tactical Forced Moves**: Tự động chặn ngay nước đi nguy hiểm của đối thủ hoặc đi nước kết liễu trận đấu mà không cần duyệt sâu.
- 📊 **Bộ Công Cụ Benchmark & Phân Tích**:
  - Kiểm thử hiệu năng tự động qua các trạng thái bàn cờ khác nhau (Early game, Mid game, AI win, Human win, Complex).
  - Lưu kết quả benchmark ra file CSV (`nodes`, `time_ms`, `score`).
  - Notebook Jupyter (`analysis.ipynb`) trực quan hóa hiệu năng duyệt node và thời gian xử lý giữa Minimax và Alpha-Beta.

---

## ⚖️ Quy Luật Trò Chơi

Trong phiên bản này, luật chơi được thiết lập như sau:
* **Bàn cờ**: Mặc định kích thước **15x15** (GUI) hoặc **9x9** (Console / Benchmark).
* **Điều kiện chiến thắng**: Người chơi hoặc Máy tạo được một chuỗi **4 quân liên tiếp** theo hàng ngang, hàng dọc, đường chéo chính hoặc đường chéo phụ (không phân biệt chặn 2 đầu hay không).
* **Quân cờ**: Người chơi cầm quân **X** (màu Đỏ), Máy cầm quân **O** (màu Xanh). Người chơi X đi trước.

---

## 📂 Cấu Trúc Dự Án

```text
├── ai/
│   ├── __init__.py
│   ├── agent.py            # Lớp bọc (wrapper) quản lý AI Agent
│   ├── alpha_beta.py       # Công cụ AI Alpha-Beta kết hợp bảng chuyển vị & tối ưu hóa
│   ├── evaluator.py        # Hàm đánh giá trạng thái bàn cờ (Heuristics) bằng cửa sổ trượt (window size = 4)
│   └── minimax.py          # Thuật toán tìm kiếm Minimax cơ bản
├── assets/                 # Các tài nguyên hình ảnh nút bấm, quân cờ (X.png, O.png, start.png,...)
├── config/
│   └── config.json         # File cấu hình giới hạn thời gian tính toán và độ rộng chùm tìm kiếm
├── core/
│   ├── __init__.py
│   ├── board.py            # Quản lý ma trận bàn cờ, mã hóa Zobrist, luật thắng/thua, undo/make move
│   └── game_engine.py      # Điều phối trạng thái trò chơi (lượt đi, kiểm tra trạng thái chung)
├── tests/
│   └── benchmark/
│       ├── logs/           # Thư mục lưu kết quả đo hiệu năng CSV
│       ├── analysis.ipynb  # Notebook phân tích, vẽ biểu đồ so sánh hiệu năng
│       └── runner.py       # Script chạy đo đạc thời gian và số node duyệt của thuật toán
├── ui/
│   ├── __init__.py
│   ├── console_ui.py       # Giao diện điều khiển dòng lệnh
│   └── gui.py              # Giao diện đồ họa Pygame đầy đủ tính năng
├── Cờ Caro.code-workspace  # File cấu hình không gian làm việc của VS Code
├── main.py                 # File chạy chính của chương trình
└── requirements.txt        # Các thư viện phụ thuộc của dự án
```

---

## ⚙️ Hướng Dẫn Cài Đặt

### 1. Yêu Cầu Hệ Thống
* Hệ điều hành: Windows, macOS, hoặc Linux.
* Phiên bản Python khuyến nghị: **Python 3.8 đến 3.11**.

### 2. Cài Đặt Các Thư Viện Phụ Thuộc
Mở terminal tại thư mục gốc của dự án và chạy lệnh:

```bash
pip install -r requirements.txt
```

*Lưu ý: File `requirements.txt` bao gồm `pygame` cho giao diện đồ họa, và nhóm thư viện `pandas`, `matplotlib`, `seaborn`, `ipykernel` phục vụ việc hiển thị biểu đồ phân tích hiệu năng trong file `.ipynb`.*

---

## 🚀 Hướng Dẫn Sử Dụng

### 1. Khởi Chạy Giao Diện Đồ Họa (GUI)
Để trải nghiệm trò chơi ở chế độ đồ họa mượt mà nhất:

```bash
python main.py
```

**Các chế độ chơi hỗ trợ:**
* **Người vs Người (PvP)**: Chơi cờ caro truyền thống với bạn bè trên cùng máy tính.
* **Chơi với Máy (Bạn đi trước)**: Thách thức AI ở các mức độ khó khác nhau (Dễ - Trung bình - Khó). Bạn cầm quân X đi trước.
* **Chơi với Máy (Máy đi trước)**: Tương tự như trên nhưng Máy sẽ cầm quân X đi trước để tăng độ thử thách.
* **Máy vs Máy (AvA)**: Xem hai thuật toán AI tự động thi đấu với nhau để phân tích chiến thuật.

**Tùy chọn độ khó:**
* **DỄ**: Độ sâu tìm kiếm (Depth) = 2. AI phản hồi cực nhanh, phù hợp cho người mới bắt đầu.
* **TRUNG BÌNH**: Độ sâu tìm kiếm (Depth) = 3. AI cân bằng tốt giữa thời gian suy nghĩ và độ thông minh.
* **KHÓ**: Độ sâu tìm kiếm (Depth) = 5. AI suy nghĩ sâu hơn, có khả năng bẫy người chơi rất cao.

---

### 2. Khởi Chạy Kiểm Thử Hiệu Năng (Benchmark)
Bạn có thể chạy thử nghiệm đo đạc hiệu năng của AI trên các thế cờ mẫu để xuất dữ liệu so sánh bằng lệnh:

```bash
python main.py --benchmark
```

Dữ liệu kết quả sẽ được lưu tự động vào file `tests/benchmark/logs/benchmark_results.csv`.

---

### 3. Phân Tích Hiệu Năng Bằng Biểu Đồ
Để trực quan hóa các dữ liệu so sánh giữa Minimax và Alpha-Beta (số lượng node đã duyệt, thời gian chạy):
1. Đảm bảo đã chạy lệnh Benchmark ở bước trên.
2. Mở file `tests/benchmark/analysis.ipynb` bằng công cụ **Jupyter Notebook** hoặc **VS Code Jupyter Extension**.
3. Chạy toàn bộ các ô (Run All Cells) để xem biểu đồ so sánh chi tiết.

---

## 🔍 Chi Tiết Thuật Toán & Tối Ưu Hóa AI

### 1. Hàm Đánh Giá Trạng Thái (Evaluation Heuristics)
Do bàn cờ Caro có kích thước lớn, AI không thể duyệt đến khi kết thúc trò chơi. Vì vậy, hàm đánh giá tại `ai/evaluator.py` đóng vai trò chấm điểm cho các trạng thái trung gian.
Hàm sử dụng kỹ thuật **Cửa sổ trượt kích thước 4** (Sliding Window of size 4) để quét qua tất cả các hàng ngang, dọc và 2 hướng chéo:
- 4 quân của mình: **+100,000 điểm** (Thắng chắc chắn)
- 3 quân của mình + 1 ô trống: **+1,000 điểm**
- 2 quân của mình + 2 ô trống: **+100 điểm**
- 1 quân của mình + 3 ô trống: **+10 điểm**
- Các điểm số tương tự nhưng mang giá trị âm (-) đối với quân của đối thủ để thực hiện chiến thuật phòng thủ.

### 2. Cơ Chế Cắt Tỉa Alpha-Beta (Alpha-Beta Pruning)
Giảm đáng kể không gian trạng thái cần tìm kiếm bằng cách bỏ qua các nhánh chắc chắn không mang lại kết quả tốt hơn nước đi tốt nhất hiện tại.
* **Alpha**: Điểm tối thiểu người chơi tối đa hóa (Maximizing Player - AI) chắc chắn đạt được.
* **Beta**: Điểm tối đa người chơi tối thiểu hóa (Minimizing Player - Con người) có thể giới hạn cho đối thủ.

### 3. Bảng Chuyển Vị (Transposition Table) & Mã Hóa Zobrist
Một trong những điểm yếu của tìm kiếm cây là việc tính toán lại nhiều lần cùng một trạng thái bàn cờ nhưng được hình thành từ các thứ tự đi khác nhau (Hiện tượng trùng lặp vị trí).
* **Mã hóa Zobrist**: Tạo ra một giá trị mã băm (64-bit integer hash key) duy nhất cho mỗi trạng thái bàn cờ bằng cách thực hiện phép toán XOR giữa các số ngẫu nhiên được định sẵn. Phép XOR này có thể được cập nhật liên tục cực nhanh sau mỗi nước đi (`make_move` và `undo_move`) mà không cần quét lại toàn bàn cờ.
* **Transposition Table**: Lưu trữ điểm số và nước đi tốt nhất của trạng thái bàn cờ đã được tính toán. Nếu gặp lại trạng thái đó tại cùng độ sâu hoặc sâu hơn, AI sẽ trả về kết quả ngay lập tức thay vì đi vào đệ quy tìm kiếm lại.

### 4. Giới Hạn Bề Rộng (Beam Search)
Hệ số nhánh của bàn cờ Caro 15x15 ban đầu là 225 và giảm dần. Để giảm thiểu thời gian suy nghĩ ở các độ sâu lớn, động cơ sử dụng **Beam Search** bằng cách chỉ lấy ra top `beam_width_root` các nước đi triển vọng nhất ở nút gốc và `beam_width_inner` ở các nút bên trong để đưa vào duyệt đệ quy sâu. Các tham số này được định nghĩa tại `config/config.json`.

---

## 🛠️ Cấu Hình Hệ Thống (`config/config.json`)

Bạn có thể chỉnh sửa các tham số của thuật toán AI trực tiếp trong file cấu hình `config/config.json`:

```json
{
  "time_limit": 1.5,
  "beam_width_root": 15,
  "beam_width_inner": 10
}
```

* `time_limit`: Thời gian tối đa (tính bằng giây) cho phép AI suy nghĩ một nước đi. Nếu quá thời gian này, thuật toán tìm kiếm sâu dần (Iterative Deepening) sẽ lập tức trả về nước đi tốt nhất tìm được ở độ sâu trước đó.
* `beam_width_root`: Số nước đi tiềm năng tối đa được xem xét tại vị trí gốc.
* `beam_width_inner`: Số nước đi tiềm năng tối đa được xem xét tại các vị trí đệ quy bên trong.

Chúc bạn có những trải nghiệm thú vị với trò chơi **Caro AI PRO**! 🚀
