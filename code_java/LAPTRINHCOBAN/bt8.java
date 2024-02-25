import java.util.Scanner;
public class bt8 {
    public static void main(String[] args){
Scanner sc = new Scanner(System.in);
System.out.println("\t\t\t\t---------- ax + b = 0 ----------\t\t\t\t\"");
System.out.print("a= ");
float a = sc.nextFloat();
System.out.print("b= ");
float b = sc.nextFloat();
if(a == 0){
    if(b != 0){
    System.out.print("phuong trinh vo nghiem!");
}
if(b == 0){
    System.out.print("phuong trinh co vo so nghiem");
}
}
else{
System.out.print("phuong trinh co ghiemm la: "+(-b/a));    
}
    }
}
