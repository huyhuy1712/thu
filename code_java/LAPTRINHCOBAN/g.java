import java.util.Scanner;

public class g {
    public static int Fibo(int n){
        if(n == 1 || n == 2) return 1;
        else return Fibo(n-1) + Fibo(n-2);
    }

    public static boolean checkFibo(int x){
        if(x <= 0) return false;
        int fibo = 1, prevFibo = 1;
        while(fibo < x){
            int temp = fibo;
            fibo = fibo + prevFibo;
            prevFibo = temp;
        }
        if(fibo == x) return true;
        else return false;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.print("nhap n: ");
        int n = sc.nextInt();
        System.out.print("cau a: "+Fibo(n)+ "\n");

        System.out.print("nhap x: ");
        int x = sc.nextInt();
        System.out.print("cau b: \n");
        if(checkFibo(x)){
            System.out.print(x+" la so Fibonacci");
        } else {
            System.out.print(x+" khong la so Fibonacci");
        }
    }
}