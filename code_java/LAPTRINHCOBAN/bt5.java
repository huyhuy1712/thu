import java.util.Scanner;
public class bt5 {
    public static void main(String[] args) {
    Scanner input = new Scanner(System.in);
    System.out.print("nhap n: ");
    int n = input.nextInt();
    if(n % 2 == 0) {
        System.out.print(n+" la so chan");
    }
    else{ 
        System.out.print(n+" la so le");
    }
}
}