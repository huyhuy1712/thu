import java.lang.Math;

import java.util.Scanner;
public class bt13 {
    public static int gt(int n){
        if(n==0 || n==1) return 1;
        else return n * gt(n-1);
}
public static void main(String[] args) {
Scanner sc = new Scanner(System.in);
System.out.print("nhap n: ");
int n = sc.nextInt();
double s = 2021;
for(int i=2;i<=n;i++){
    s+= (Math.pow(-1,i)/gt(i));
}
System.out.print("cau a: \n s= " + s);
System.out.print("\n nhap x: ");
int x = sc.nextInt();
float sum1 = 0;
for(int i= 1; i <= n; i++){
    sum1 += (Math.pow(x,i)/gt(x+i));
}
System.out.print("cau b: \n s= "+sum1);
}
}
