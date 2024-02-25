import java.util.Scanner;

public class bt17 {
    public static void main(String[] args) {
    Scanner sc  = new Scanner(System.in);
    System.out.print("nhap a: ");
    int a = sc.nextInt(); 
    System.out.print("nhap b: ");   
    int b = sc.nextInt();    
    int t = a;
    int h = b;
    int UCLN;
    if(a == b) UCLN = a;
    while(a!= b){
        if(a > b) a -= b;
       if(b > a) b -= a;
    }
    UCLN = a;
    int BCNN = (t*h) / UCLN;
    System.out.println("UCLN cua 2 so "+t+" va "+h+" la "+UCLN);
    System.out.println("BCNN cua 2 so "+t+" va "+h+" la "+BCNN);
}
}
