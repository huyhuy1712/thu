import java.util.Scanner;
public class bt14 {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.print("nhap n: ");
        int n = sc.nextInt();
        int s = 0;
        if(n%2==0){
            for(int i=2;i<=n;i++){
                if(i%2==0) s+=i;
            }}
        else{
            for(int i=1;i<=n;i++){
                if(i%2!=0) s+=i;
        }
        }  
        System.out.print("S("+n+")= "+s);
    }
}