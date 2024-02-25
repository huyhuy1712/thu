import java.util.Scanner;
public class cau1 {
    public static int Max(int[] a ){
        int max = a[0];
        for(int i = 0; i < 10; i++){
        if(max <= a[i]) max = a[i];}
        return max;
    }
    public static int Min(int[] a ){
        int min = a[0];
        for(int i = 0; i < 10; i++){
        if(min >= a[i]) min = a[i];}
        return min;
    }
    public static void add(int[] a, int index,int k){
        int[] c = new int[11];
        for(int i = 0; i < index-1; i++){
            c[i] = a[i];
        }
        c[index-1] = k;
for(int i = index-1; i < 10; i++){
    c[i+1] = a[i];
    }
    for(int i = 0; i < 11; i++){
    System.out.print(c[i] + " ");
}
}
public static void delete(int[] a, int index){
    int[] d = new int[9];
    for(int i = 0; i < index-1; i++){
        d[i] = a[i];
    }
    for(int i = index-1; i < 9; i++){
        d[i] = a[i+1];
}
for(int i = 0; i < 9; i++){
System.out.print(d[i]+" ");
}
}
    public static void main(String[] args) {
Scanner sc = new Scanner(System.in);
    int[] a = new int[10];
    int[] b = new int[10];
    for(int i = 0; i < 10; i++){
    System.out.print("a[" + i + "] = ");
         a[i] = sc.nextInt();
         b[i] = a[i];
    }
    for(int i = 0; i < 10; i++){
    System.out.print(a[i]+" ");}
        int m = Max(a);
        int max2 = a[0];
        for(int i = 0; i < 10; i++){
            if(max2 <= a[i] && a[i] != m) max2 = a[i];}
            System.out.println("\nmax cua mang = " + m);
            System.out.print("max nhi cua mang = " + max2);
            for(int i = 0; i < 9; i++){
                for(int j = i+1;j < 10;j++){
        if (a[i] >= a[j]) {
    int temp = a[i];
    a[i] = a[j];
    a[j] = temp;}
    }
        }
        System.out.println("\nmang tang dan: ");
        for(int i = 0; i < 10; i++){
            System.out.print(a[i]+" ");
        }  
        for(int i = 0; i < 9; i++){
            for(int j = i+1;j < 10;j++){
    if (a[i] <= a[j]) {
int temp = a[i];
a[i] = a[j];
a[j] = temp;}
}
    }
        System.out.println("\nmang giam dan: ");
        for(int i = 0; i < 10; i++){
            System.out.print(a[i]+" ");
        } 
        System.out.print("\n nhap phan tu can them: ");
        int k = sc.nextInt();
        System.out.print("nhap vi tri them: ");
        int index = sc.nextInt();
        add(b,index,k);
        System.out.print("\nnhap vi tri can xoa: ");
        int index2 = sc.nextInt();
        delete( b, index2);
        int s = 0;
        for(int i = 0; i < 10; i++){
            int t = b[i];
            while(b[i]>10){
                b[i] /= 10;
            }
            if(b[i] % 2 != 0) {s+=t;
        } b[i] = t; 
        }
        System.out.println("\ntong cac so co chu so dau le la: "+s);
        int min2 = b[0];
        int n = Min(b);
        for(int i = 0; i < 10; i++){
            if(min2 >= b[i] && b[i]!= n) min2 = b[i];
        }
        System.out.println("gia tri nho thu hai cua mang la: "+min2);
        System.out.print("nhap x: ");
        int x = sc.nextInt();
        int x1 = x /10, x2 = x % 10;
        int count = 0;
        int count1 = 0;
        for(int i = 0; i < 10; i++){
            int g = b[i];
            while(b[i] > 0){
                int t = b[i] % 10;
                if(t == x1) {count++;}
                if(t == x2) {count1++;}
                b[i] /= 10;
            } b[i] = g;
        if(count != 0 && count1 != 0){
            System.out.print(b[i]+" ");
        }
        count = 0; count1 = 0;
    }
    for(int i = 0; i < 9; i++){
        for(int j = i+1;j < 10;j++){
            if(b[i] % 2 == 0 && b[j] % 2 == 0){
                if(b[i] >= b[j]){
                    int temp = b[i];
                    b[i] = b[j];
                    b[j] = temp;
            }
            }
    }
    }
    System.out.println("\n day cac so chan tang: ");
    for(int i = 0; i < 10; i++){
    System.out.print(b[i]+" ");
    }
}
}



