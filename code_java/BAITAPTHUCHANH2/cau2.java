// import java.util.Scanner;

// import javax.sound.sampled.SourceDataLine;
// public class cau2 {
    
//     public static void main(String[] args) {
//         Scanner sc = new Scanner(System.in);
//         System.out.print("nhap so dong: ");
//         int m = sc.nextInt();
//         System.out.print("nhap so cot: ");
//         int n = sc.nextInt();
//         int [][] a = new int [m][n];
//         int [][] b = new int [m][n];
//         for(int i = 0; i < m ; i++){
//             for(int j = 0; j < n ; j++){
//                 System.out.print("a[" + i + "][" + j + "]= ");
//                 a[i][j] = sc.nextInt();
//             }
//         }
//         for(int i = 0; i < m ; i++){
//             for(int j = 0; j < n ; j++){
//         System.out.print(a[i][j]+" ");
//     } System.out.print("\n");
//     }
//     for(int i = 0; i < m ; i++){
//         for(int j = 0; j < n ; j++){
//             b[i][j] = a[i][j];
//         }
//     }
//     int t = m*n;
//     for(int i  = 0; i < t-1; i++){
//         for(int j = i+1; j < t; j++){
//             if(a[i/n][i%n] >= a[j/n][j%n]){
//                 int temp = a[i/n][i%n];
//                 a[i/n][i%n] = a[j/n][j%n];
//                 a[j/n][j%n] = temp;
//             }
//     }
// }
// System.out.println("mang tang dan theo hang: ");
// for(int i = 0; i < m ; i++){
//     for(int j = 0; j < n ; j++){
//         System.out.print(a[i][j]+" ");
//     }
//     System.out.print("\n");
// }
// for(int i = 0; i < t-1 ; i++){
//     for(int j = i+1; j < t; j++){
//         if(a[i%m][i/m] <= a[j%m][j/m]){
//         int temp = a[i%m][i/m];
//         a[i%m][i/m] = a[j%m][j/m];
//         a[j%m][j/m] = temp;            
//     }
// }
// }
// System.out.println("mang giam dan theo cot: ");
// for(int i = 0; i < m ; i++){
//     for(int j = 0; j < n ; j++){
//         System.out.print(a[i][j]+" ");
//     }
//     System.out.print("\n");
// }
// System.out.println("min = "+a[m-1][n-1]);
// System.out.println("max = "+a[0][0]);

// int max = b[0][0], index = 0, index1 = 0;
// for(int i = 0; i < m ; i++){
//     for(int j = 0; j < n; j++){
//         if(b[i][j] >= max){
//             max = b[i][j];
//             index = i;
//             index1 = j;
//         }
//     }
// }
// System.out.println("vi tri chua max la: " + index + " " + index1);

// int min = b[0][0], index2 = 0, index3 = 0;
// for(int i = 0; i < m ; i++){
//     for(int j = 0; j < n; j++){
//         if(b[i][j] <= max){
//             max = b[i][j];
//             index2 = i;
//             index3 = j;
//         }
//     }
// }
// System.out.println("vi tri chua min la: " + index2 + " " + index3);
// }
// }
