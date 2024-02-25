#include <iostream>
#include <math.h>
using namespace std;
void kiemtrasohoanchinh(long int n){ // ham kiem tra so hoan chinh 
	int s = 0;
	for (int i = 1 ; i < n; i++){
		if (n % i == 0){
			s += i; 
		}}
		if ( s == n && n != 0){cout << n <<" la so hoan chinh \n";} 
else { cout << n << " khong la so hoan chinh \n";}
}
	void kiemtrasochinhphuong(int n){ // ham kiem tra so chinh phuong  
	int dem = 0; 
	for (int i = 1 ; i < n; i++){
	if (sqrt(n) / i == 1 ) dem ++;	
	}
	if (dem == 0) { cout << n << " khong phai la so chinh phuong \n"; 
	}
	else { cout << n << " la so chinh phuong \n"; 
	}}
	
	void kiemtrasonguyento (int n){ // ham kiem tra so nguyen to 
	int dem = 0 ; 
	for (int i = n-1; i>=2; i--){
		if (n % i == 0) dem++ ; 	
	} 
	if (dem == 0 && n != 0 && n!= 1){ cout << n << " la so nguyen to \n";
	} 
	  else {cout << n << " khong phai la so nguyen to \n";
	} 
	} 

 kiemtrasoarmstrong(int n){ // ham kiem tra so armstrong
	int dem = 0, i = n, so, armstrong = 0;
	while (n != 0){ // dem so
		n /= 10;
		dem ++;
	} n = i; // tra gia tri n ve lai ban dau
	while ( n != 0){
		so = n % 10; // lay so cuoi
		armstrong += pow(so,dem);
		n /= 10; // bo so cuoi cua n 
	} n =  i;
	if (n != armstrong || n < 10){cout << n << " khong phai la so armstrong \n";
 } else {cout << n << " la so armstrong \n";
	}
}

	void songuoc(int n){ // ham tim so nguoc
	int sodoi = 0, so, i = n;
		while (n != 0){
			so = n % 10;
			sodoi = (sodoi * 10) + so;
			n /= 10;
		} n = i;
		cout << "so viet nguoc cua " << n << " la: " << sodoi;
	} 
	
	 void sodoixung(int n){
	 		int sodoi = 0, so, i = n;
		while (n != 0){
			so = n % 10;
			sodoi = (sodoi * 10) + so;
			n /= 10;
		} n = i;
	 	if (n == sodoi){
	 		cout << n << " la so doi xung \n";
		 } else { cout << n << " khong phai la so doi xung \n";
		 }
	 }

int main (){ 
int n, t; 
	cout << "n= "; cin >> n;
	cout << "cau a: \n"; 
	kiemtrasohoanchinh(n);
	cout << "cau b: \n";
	kiemtrasochinhphuong(n); 
	cout << "cau c: \n";
	kiemtrasonguyento(n); 
	cout << "cau d: \n";
	kiemtrasoarmstrong(n);
	cout << " cau e: \n";
	sodoixung(n);
	cout << " cau f: \n";
	songuoc(n);
	return 0; 	
} 
