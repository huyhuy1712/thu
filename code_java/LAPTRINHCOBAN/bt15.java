import java.util.Scanner;
public class bt15 {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.print("nhap a: ");
        int a = sc.nextInt();
        System.out.print("nhap b: ");
        int b = sc.nextInt();
        System.out.print("nhap c: ");
        int c = sc.nextInt();
        System.out.print("nhap d: ");
        int d = sc.nextInt();
        int max = a;
        if(max <= b) max = b;
        if(max <= c) max = c;
        if(max <= d) max = d;
        int min = a;
        if(min >= b) min = b;
        if(min >= c) min = c;
        if(min >= d) min = d;
        System.out.println("max= "+max);
        System.out.print("min= "+min);
}
}
