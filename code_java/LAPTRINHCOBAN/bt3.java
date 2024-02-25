import java.util.Scanner;

import javax.print.event.PrintEvent;
public class bt3 {
    public static void main(String[] args){
        Scanner input = new Scanner(System.in);
        System.out.print("nhap ho ten: ");
String hoten = input.nextLine();
System.out.print("nhap que quan: ");
String quequan = input.nextLine();
System.out.print("nhap diem toan: ");
float t = input.nextFloat();
System.out.print("nhap diem ly: ");
float l = input.nextFloat();
System.out.print("nhap diem hoa: ");
float h = input.nextFloat();
System.out.println(hoten);
System.out.println(quequan);
System.out.println("diem toan: " + t);
System.out.println("diem ly: " + l);
System.out.println("diem hoa : " + h);
System.out.print("diem trung binh cua em "+hoten+" la: "+(((t+l+h)/3)*100/100));
    }
}
