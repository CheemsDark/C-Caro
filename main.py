import sys
import tests.benchmark.runner

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--benchmark":
        tests.benchmark.runner.run_benchmark()
        return

    try:
        from ui.gui import PygameUI
        gui = PygameUI(size=15)
        gui.start()
    except ImportError:
        print("Lỗi: Bạn cần cài đặt thư viện pygame để dùng giao diện đồ họa.")
        print("Vui lòng chạy lệnh: pip install pygame")

if __name__ == "__main__":
    main()
