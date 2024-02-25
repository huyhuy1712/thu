import java.util.Scanner;
import java.lang.Math;
public class bt19 {
    public static boolean checkscp(int n)
{
for(int i= 2; i < n; i++)
    if(i == Math.sqrt(n)) return true;
return false;
}
public static void main(String[] args) {
    Scanner sc = new Scanner(System.in);
    System.out.print("nhap n: ");
    int n = sc.nextInt();
    while(!checkscp(n)){
    System.out.print(n+" khong phai la so chinh phuong moi nhap lai\n");
    System.out.println("nhap n: ");
    n = sc.nextInt();
    }

System.out.print(n+" la so chinh phuong");
}
}
