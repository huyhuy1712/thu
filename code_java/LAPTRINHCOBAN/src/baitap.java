import java.util.Scanner;
public class baitap {
    public static void main(String[] args){
        
Scanner input = new Scanner(System.in);
System.out.println("nhap so phan tu: ");
int n = input.nextInt();
int arr[]= new int[n];
        for(int i=0; i<n; i++){
            System.out.print("arr["+ i + "]= ");
            arr[i] = input.nextInt();
       }
        for(int i=0; i<n; i++){
            System.out.print(arr[i] + " ");
        } 
        System.out.println("");
    int max  =arr[0];
    for(int i=0;i<arr.length;i++){
        if(max <= arr[i]){
            max = arr[i];
            
    } 
}
System.out.println("max = " + max);
for(int i = 0; i < n; i++){
    if(max <= arr[i]){
System.out.println("index = " + i);}
}
System.out.print("nhap k: ");
int k = input.nextInt();
int arr2[] = new int[n+1];
int arr3[] = new int[n+1];
for(int i=0;i<n;i++){
    arr2[i] = arr[i];
}
arr2[n] = k;
arr = arr2;
for(int i=0;i<arr.length;i++){
    System.out.print(arr[i] + " ");
}
System.out.print("index = ");
int index = input.nextInt();
System.out.print("m= ");
int m = input.nextInt();
for(int i = 0; i < index; i++){
    arr3[i] = arr[i];

}
arr3[index] = m;
for(int i=index+1;i<=n;i++) {
    arr3[i] = arr[i-1];
}
for(int i=0;i<arr.length;i++){
    System.out.print(arr3[i] + " ");
}
}
}
