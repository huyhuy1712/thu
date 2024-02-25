import java.util.Scanner;
public class codenam2 {
public static void main(String[] args){
    Scanner sc = new Scanner(System.in);
    System.out.println("nhap ho&ten: ");
    String name = sc.nextLine();
    System.out.println("Hello + "+ name);
    System.out.println("nhap a: ");
    int a = sc.nextInt();
     System.out.println("nhap b: ");
     int b = sc.nextInt();
      System.out.println("nhap c: ");
    int c = sc.nextInt();
    System.out.println(a+" "+b+" "+c);
    System.out.println("tong: "+(a+b+c) + "\n" + "tich: " + (a*b*c));

}
}
