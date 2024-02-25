
#include <iostream>
#include <math.h>
using namespace std;
int main(){
 int a, b,c,max, min;
 cout<< "a= "; cin>> a;
  cout<< "b= "; cin>> b;
   cout<< "c="; cin>> c;
   max = a;
   if( b>max) max=b;
   if( c>max) max=c;
	
   min=a;
      if( b<min) min=b;
   if( c<min) min=c;
	cout <<"max= "<<max<<endl;
	cout << "min= "<<min<<endl;
	return 0;
}
