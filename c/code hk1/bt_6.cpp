#include <iostream>
#include <math.h>
#include <cstdlib>
using namespace std;
int main() {
 cout << "cau a: \n" ;
 int n, max;
	cout << "n= "; cin >> n;
	int a[n];
	a[0] = max;
	for (int i = 0; i < n; i++){
		a[i] = rand(); 
		cout << a[i] << " ";
	}
	cout << endl;
	for (int i = 0; i < n;i++) {
		if (a[i] > max) { max = a[i]; }
	}
		cout << "max = " << max << endl;

	cout << "cau b: \n";
	int s = 0;
		for (int i = 0; i < n; i++) {
	 s = s + a[i];
}
	cout << "tong cua day so là: " << s << endl;

	cout << "cau c: \n";
	int k, e = 0;
	cout << "k= "; cin >> k;
	for (int i = 0; i < n; i++){
		if(a[i] == k) e++;
		}
			cout << "so phan tu bang k la: " << e << endl;

			cout << "cau d: \n";
				for (int i = 0; i < n - 1; i++){
				for (int j = i + 1 ;j < n; j++) {
			 if(a[i] > a[j]) {
			int k = a[i] ;
			   a[i] = a[j];
			   a[j] = k;
				}}}
				for(int i = 0; i < n; i++)
					cout << a[i] << " ";
	return 0;
}
