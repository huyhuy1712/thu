#include <stdio.h>
#include <iostream>
#include <math.h>
using namespace std;
int main(){
int m,n;
int a[100][100];
cin >> m;
cin >> n;
	for (int i = 0; i < m; i++) {
		for (int j = 0; j < n; j++) {
		cin >> a[i][j];
		}
		}
			for (int i = 0; i < m; i++) {
		for (int j = 0; j < n; j++) {
		cout << a[i][j] << " ";
			} cout << endl;
	}
	int t = m * n;
	int kc;
	int min2 = abs(a[0][0]-a[0][1]);
 	for(int i = 0; i<t-1;t++){
	 for (int j = i + 1; j < t; j++) {
		  kc = abs(a[i / n][i % n] - a[j / n][j % n]);
		 if (min2 >= kc) {
		 min2 = kc;} else continue;
}
}	
cout << "haha";
}
