#include <iostream>
#include <math.h>
using namespace std;
int S(int n, float x){
float t = 0;
float s = 0;
for(float i = 1; i <= n; i++){
	t += (1/i);
	s += ( pow(-1,i-1)*(pow(x,i)/t)); 

} cout << "S(" << n << "," << x <<")= " << s;
}

int main (){
	float n, x;
	nhaplai:
  cout << "n= "; cin >> n;
  cout << " x= "; cin >> x;
  if (n < 1) goto nhaplai;
  else { S(n, x);
  }
  return 0;
}
