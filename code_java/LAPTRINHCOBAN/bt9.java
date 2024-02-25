import java.lang.Math;
import java.util.Scanner;
public class bt9 {
    public static void main(String [] args){
    Scanner sc = new Scanner(System.in);
    System.out.println("\t\t\t\t---------- ax2 + bx + c = 0 ----------\t\t\t\t\"");
System.out.print("a= ");
double a = sc.nextDouble();
System.out.print("b= ");
double b = sc.nextDouble();
System.out.print("c= ");
double c = sc.nextDouble();
if(a == 0){
    if(b == 0){
        if(c == 0){
            System.out.print("phhuong trinh co vo so nghiem");
    }
        if(c != 0){
            System.out.print("phuong trinh vo nghiem!");
        }
    }
if(b != 0){
    System.out.print("phuong trinh co nghiem la: "+(-c/b));
}}
else{
double delta = b*b - 4*a*c;
double x1 = ((-b + Math.sqrt(delta)) / (2*a))*100/100;
double x2 = ((-b - Math.sqrt(delta)) / (2*a))*100/100;
if(delta  < 0){
    System.out.print("phuong trinh vo nghiem!");
}
if(delta == 0){
    System.out.print("phuong trinh co nghiem kep la: "+(-b/(2*a)));
}
if(delta > 0){
    System.out.print("phuong trinh co 2 ngiem la: "+x1+" "+x2);
}
}
}
}
