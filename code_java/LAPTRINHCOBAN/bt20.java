import java.util.Scanner;
public class bt20 {
    public static boolean checksnt(int n){
        if(n < 2) return false;
        for(int i = 2; i < n/2; i++) 
        if(n%i == 0) return false;
return true;
    }
    public static void dem(int n){
        int t = n;
        int count = 0;
        while(n != 0){
        n /= 10;
        count++;
        }
        System.out.print(t+" co "+count+" chu so");
    }
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.print("nhap n: ");
        int n = sc.nextInt();
        int t = n;
        for(int i = 2;i<=n;i++){
            if(checksnt(i)){
                while(n%i == 0){
                    System.out.print(i+" ");
                    n /= i ;
                }
            }
        }
        System.out.print("\n");
        dem(t);
    }
}
