#include <iostream>
#include<math.h>
using namespace std;
int main(){
float xA, yA, xB, yB, xC, yC, xG, yG;
nhaplaidulieu:
cout<<"toa do A: \n";
cout <<"xA= "; cin >> xA;
cout <<"yA= "; cin >> yA;
cout<<"toa do B: \n";
cout <<"xB= "; cin >> xB;
cout <<"yB= "; cin >> yB;
cout<<"toa do C: \n";
cout <<"xC= "; cin >> xC;
cout <<"yC= "; cin >> yC;
float xAB = xB - xA ;
float yAB = yB - yA ;
float yAC = yC - yA ;
float xAC = xC - xA ;
if(xAB*yAC == xAC*yAB){ cout<<" 3 diem thang hang! \n";
goto nhaplaidulieu;}
else{ 
	float	AB = sqrt( ( (xB-xA) * (xB-xA) ) + ( (yB-yA) * (yB-yA) ) );
	float 	AC= sqrt( ( (xC-xA) * (xC-xA) ) + ( (yC-yA) * (yC-yA) ) );
	float 	BC = sqrt( ( (xC-xB) * (xC-xB) ) + ( (yC-yB) * (yC-yB) ) );
	float cv = AB + AC + BC ;
	float q= ( AB + AC + BC ) / 2 ;
	float dt = sqrt(q * (q-AB) * (q-AC) * (q-BC) ) ;
 xG= ( xA + xB + xC ) / 3 ;
	yG = ( yA + yB + yC ) / 3 ;
	cout << " trong tam tam giac ABC la: G("<< xG <<";"<< yG <<")"<< endl;
	cout<< " chu vi tam giac ABC la: "<< round(cv * 100) / 100 << endl;
	cout << "dien tich tam giac ABC la: "<< round(dt * 100) / 100 << endl;
}
	return 0;
}

