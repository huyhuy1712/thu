#include <iostream>
#include <math.h>
using namespace std;
 float S(int n, int h ){
  int x[n];
  int y[h];
  int i, j;
  float s = 0;
  for ( i = 0 ; i <= n; i++){
  cout << " x(" << i+1 << ")= "; cin >> x[i];
}
for ( j = 0 ; j <= h; j++){
cout << " y(" << j+1 << ")= "; cin >> y[j];
}
for (i = 0; i <= n; i++){
for (j = 0 ; j <= n ; j++){
	float t = (x[i+1] - x[i])*(y[j+1] + y[j])/2;
	s += t; 
}} return abs(s);
} 

int main(){
	int n, y;
	cout << "n = y = "; cin >> n;
	y = n;
	cout << "dien tich da giac P la: " << S(n,y);
	return 0;
}
 
