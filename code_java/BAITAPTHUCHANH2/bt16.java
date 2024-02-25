public class bt16 {
    public static void main(String[] args) {
        int n = 4; // Số phần tử trong dãy số cần tính toán
        int x0 = 1; // Giá trị của X0
        int x1 = 1; // Giá trị của X1
        int xn = recursiveSequence(n, x0, x1); // Tính giá trị của Xn bằng đệ qui
        System.out.println("Giá trị của Xn là: " + xn);
    }

    public static int recursiveSequence(int n, int x0, int x1) {
        if (n == 0) {
            return x0; // Kết thúc đệ qui khi n = 0, trả về giá trị của X0
        } else if (n == 1) {
            return x1; // Kết thúc đệ qui khi n = 1, trả về giá trị của X1
        } else {
            return n * x0 + (n - 1) * x1 + recursiveSequence(n - 1, x1, x0); // Tính giá trị của Xn bằng công thức đã cho
        }
    }
}