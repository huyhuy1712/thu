import java.util.Scanner;
public class bt10 {
    public static boolean checksnt(int n){
        if(n<2)return false;
        for(int i=2;i<=n/2;i++)
        if(n%i==0)return false;
        return true;
    }
    public static void main(String[] args) {
        Scanner sc= new Scanner(System.in);
        System.out.print("nhap n: ");
      int n = sc.nextInt();
        if(checksnt(n))  System.out.print(n+ " la so nguyen to");
        
        else{
            System.out.print(n+ " khong la so nguyen to");
        }
    }
}
