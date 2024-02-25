import java.util.Scanner;
public class bt6 {
    public static void main(String[] args) {
Scanner sc = new Scanner(System.in);
System.out.print("nhap ngay: ");
int ngay = sc.nextInt();
System.out.print("nhap thang: ");
int thang = sc.nextInt();
System.out.print("nhap nam: ");
int nam = sc.nextInt();
if(thang < 3){
    thang = thang + 12;
    nam = nam - 1;
}
int n = (ngay+(2*thang)+(3*(thang+1))/5 + nam + (nam / 4)) % 7;
if (n == 0) {
    System.out.print(ngay+"/"+thang+"/"+nam+" la ngay chu nhat");
}
if (n == 1) {
    System.out.print(ngay+"/"+thang+"/"+nam+" la ngay thu hai");
}
if (n == 2) {
    System.out.print(ngay+"/"+thang+"/"+nam+" la ngay thu ba");
}
if (n == 3) {
    System.out.print(ngay+"/"+thang+"/"+nam+" la ngay thu tu");
}
if (n == 4) {
    System.out.print(ngay+"/"+thang+"/"+nam+" la ngay thu nam");
}
if (n == 5) {
    System.out.print(ngay+"/"+thang+"/"+nam+" la ngay thu sau");
}
if (n == 6) {
    System.out.print(ngay+"/"+thang+"/"+nam+" la ngay thu bay");
}
}
}