#include <iostream>
#include <math.h>
using namespace std;
	int UCLN( int a, int b){
	int UCLN;
	if (a == 0 || b == 0)
	return a + b;
	while (a != b){
		if (a > b){a -= b;}
		else{b -= a;}
		}
		return a;
	}
	int main(){	
	int a, b;
	cout << "a= "; cin >> a;
	cout << "b= "; cin >> b;
	cout << "UCLN cua so a va b la: " << UCLN(a,b) << endl;
	return 0;
	}
	

