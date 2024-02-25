import java.util.Scanner;
public class bt4 {
    public static void main(String[] args){
        Scanner input = new Scanner(System.in);
System.out.print("nhap ban kinh hinh tron: ");
        float r = input.nextFloat();
    System.out.println("chu vi hinh tron: "+(2*3.14*r) *100/100);
System.out.println("dien tich hinh tron: "+r*r*3.14);
    }
}
