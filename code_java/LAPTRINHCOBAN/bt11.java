import java.util.Scanner;
public class bt11{
public static boolean checksnt(int n){
    if(n < 2) return false;
        for(int i = 2; i < n/2; i++)
         if(n%i == 0) return false;
            return true;
    
}
public static void main(String[] args) {
    Scanner sc = new Scanner(System.in);
    System.out.print("nhap n: ");
    int n = sc.nextInt();
    int s3 = 0;
    System.out.print("cau a: ");
    for(int i = 1; i <= n; i++){
            System.out.print(i+" ");
            s3 += i;
}
    System.out.print("\n s= "+s3);

    System.out.print("\n cau b: ");
    int s1 = 0;
    for(int i = 2; i <= n; i++){
        if(i%2 == 0){
        System.out.print(i+" ");
            s1 += i;}}
            System.out.print("\n s= "+s1);
            System.out.print("\n cau c: ");
            int s2 = 0;
            for(int i = 2; i <= n; i++){
              if(i%2 != 0){
             System.out.print(i+" ");
            s2 += i;}}
             System.out.print("\n s= "+s2);
    System.out.print("\ncau d: ");
    int s = 0;
    for(int i = 2; i <= n; i++){
        if(checksnt(i)){
            System.out.print(i+" ");
            s += i;
}
    }
    System.out.print("\n s= "+s);
    System.out.print("\n cau e: ");
    int c = 0;
for(int i = 2; i < 10000000; i++){
    if(checksnt(i)) {c++;
    System.out.print(i+" ");}
    if(c == n) break;
}
}}