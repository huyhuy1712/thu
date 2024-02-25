import java.util.Scanner;
public class bt2 {
    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        System.out.print("nhap a: ");
        int a = input.nextInt();
        System.out.print("nhap b: ");
        int b = input.nextInt();
        System.out.println("tong 2 so "+ a +" va "+ b+" la: "+ (a+b));
        System.out.println("hieu 2 so "+ a +" va "+ b+" la: "+ (a-b));
        System.out.println("thuong 2 so "+ a +" va "+ b+" la: "+ (a*b));
        System.out.print("tich 2 so "+ a +" va "+ b+" la: "+ (a/b));
}
}
