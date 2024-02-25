
#include <iostream>
#include <math.h>
using namespace std;
bool kiemtrasonguyento(int n){ // ham kiem tra so nguyen to
	for(int j=2;j<n;j++){
		if(n<=1)
		return false;
		if(n%j==0)
		return false;
	}
	return true;
}

int xacdinhsonguyento(int n){ // b) ham xac dinh so nguyen to thu n
	int i, count = 0;
for( i=2;count <= n ;i++){
		if(kiemtrasonguyento(i) == true){
		count++;
		}
		if(kiemtrasonguyento(i) == false)
		continue;
		if(count == n){
		return i;
			break;
	}} 
 return i;
}
  int demsonguyento(int n){ // a) ham dem so nguyen to
  	int dem = 0;
  	for (int i = 2; i <= n; i++){
  		if(kiemtrasonguyento(i) == true) dem++;
  } return dem;
  }
  
   int nnearest(int n){ // c) ham tim so nguyen to gan n nhat
  	int i, j, kc1, kc2;
  	if (n <= 1){
  		cout << "so nguyen to gan " << n << " nhat la: " << 2 << "\n";
	  }
	  else{
	for (i = n; i >= 2; i--){
		if (kiemtrasonguyento(i) == true ) break;		
	}
	for ( j = n+1; j <= pow(10,4); j++){
		if (kiemtrasonguyento(j) == true) break;
	}
	kc1 = n - i;
	kc2 = j - n;
	if (kc1 > kc2) cout << "so nguyen to gan " << n << " nhat la: " << j << "\n";
	if (kc1 < kc2) cout << "so nguyen to gan " << n << " nhat la: " << i << "\n";
	if (kc1 == kc2) cout << "so nguyen to gan " << n << " nhat la: " << i << " va " << j << "\n";
}
}
   
   int nfirst(int n){ // d) ham xuat cac so nguyen to dau tien 
   	int dem = 1, i = 2;
   	while (dem <= n){
   		if (kiemtrasonguyento (i) == true)
	 { cout << i <<" ";
	 dem++;
	 } i++;
	   }}

   
   
  int main () {
  	int n;
  	cout << "n= "; cin >> n;
  	cout << "cau a: \n";
  	cout << "so luong so nguyen to nho hon hoac bang " << n << " la: " << demsonguyento(n) << "\n";
  	cout << "cau b: \n";
  	cout << "so nguyen to thu " << n << " la: " << xacdinhsonguyento(n) << "\n";
  	cout << "cau c: \n";
  	nnearest(n);
  	cout << "cau d: \n";
  	 nfirst(n);
  	return 0;
  }
