#include<iostream>
#include <math.h>
using namespace std;
void S(int n){
	float  s= 1, f = 1;
	for (float i = 1; i < n; i++){
		f += (1/(i + 1)); // bien duoi mau so
	 s += (i+1)/f;}
	cout << "S(" << n << ")= " << s;
}

int main(){
	int n;
	cout << "so nguyen duong n: "; cin >> n;
	S(n);
	return 0;
}
