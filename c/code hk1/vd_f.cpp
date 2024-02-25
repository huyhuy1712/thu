#include <iostream>
#include <math.h>
using namespace std;
int main(){
	 int a, b,c,max, d, max2;
 cout<< "a= "; cin>> a;
  cout<< "b= "; cin>> b;
   cout<< "c= "; cin>> c;
    cout<< "d= "; cin>> d;
    max=a;
   if(b>max) max = b;
   if(c>max) max = c;
   if(d>max) max = d;
 max2 = c;
 if (c!= max){
	if ( b!= max && b<max && b>max2 ) max2 = b;
	if ( d!=max &&  d<max && d>max2) max2 = d;
		if ( a!=max &&  a<max && a>max2) max2 = a;
			if ( c!=max &&  c<max && c>max2) max2 = c;
		}
else {
 if(b>=a && b>=d) max2 = b;
if(a>=b && a>=d) max2 = a;
if(d>=a && d>=b) max2 = d;}
   cout << "so lon thu nhi la: "<< max2;
   return 0;}
   
   
