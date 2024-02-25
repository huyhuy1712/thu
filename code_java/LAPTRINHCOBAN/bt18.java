    
import java.util.Scanner;
public class bt18 {
    public static int Fibo(int n){
        if(n == 1 || n == 2) return 1;
        else return Fibo(n-1)+Fibo(n-2);
    }

public static boolean checkfubo(int x){
    int fubo = 1 ;
    int prevfubo = 1;
    while(fubo < x){
        int temp = fubo;
        fubo = fubo + prevfubo;
        prevfubo = temp;}
        if(fubo == x) return true;
        return false;
}
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.print("nhap n: ");
        int n = sc.nextInt();
        System.out.print("cau a: "+Fibo(n)+ "\n");
        System.out.print("cau b: ");
        System.out.print("nhap x: ");
        int x  = sc.nextInt();
        if(checkfubo(x)){
        System.out.print(x+" la so fubonaci\n");}
        else{System.out.print(x+" khong la so fubonaci\n");}

        System.out.print("cau c: ");
        for(int i = 1; i <= n; i++){
            System.out.print(Fibo(i)+" ");
        }
        System.out.print("\nnhap m: ");
        int m = sc.nextInt();
        int s = 0;
        System.out.print(" cau d: ");
        for(int i = 1; i < 100; i++){
            if(Fibo(i) > m) break;
            s += Fibo(i);
        }
        System.out.print(s);
}
}
