#include <iostream>
#include <math.h>
#include <string>
using namespace std;
 void xdngay(int d, int m, int y){ // a)ham xd ngay truoc va sau
	if ( m == 1 ||  m == 3 ||  m == 5 ||  m == 7 ||  m == 8 ||  m == 10 ||  m == 12 ){ // cac thang co 31 ngay
		if (d >= 2 && d <= 30) {
			cout << " ngay ke truoc " << d << "/" << m <<"/" << y << " la: " << d-1 << "/" << m << "/" << y <<"\n";
			cout << " ngay ke sau " << d << "/" << m <<"/" << y << " la: " << d+1 << "/" << m << "/" <<  y <<"\n";
		}
		if (d == 31 && ( m == 1 ||  m == 3 ||  m == 5 ||  m == 7 ||  m == 8 ||  m == 10)) { // chuyen thang
			cout << " ngay ke truoc " << d << "/" << m <<"/" << y << " la: " << d-1 << "/" << m << "/" <<  y <<"\n";
			cout << " ngay ke sau " << d << "/" << m <<"/" << y << " la: " << 1 << "/" << m+1 << "/" <<  y <<"\n";
		}
		if (d == 1 &&  (  m == 3 ||  m == 5 ||  m == 7 ||  m == 10)){
			cout << " ngay ke truoc " << d << "/" << m <<"/" << y << " la: " << 30 << "/" << m-1 << "/" <<  y <<"\n";
			cout << " ngay ke sau " << d << "/" << m <<"/" << y << " la: " << d+1 << "/" << m << "/" <<  y <<"\n";}
	 if( d == 1 && m == 8 ){
		cout << " ngay ke truoc " << d << "/" << m <<"/" << y << " la: " << 31 << "/" << m-1 << "/" <<  y <<"\n";
		cout << " ngay ke sau " << d << "/" << m <<"/" << y << " la: " << d+1 << "/" << m << "/" <<  y <<"\n";	
	}
		}	
	if (d == 31 && m == 12) { // chuyen nam
			cout << " ngay ke truoc " << d << "/" << m <<"/" << y << " la: " << d-1 << "/" << m << "/" <<  y <<"\n";
			cout << " ngay ke sau " << d << "/" << m <<"/" << y << " la: " << 1 << "/" << 1 << "/" <<  y+1 <<"\n";
		}
			if (d == 1 && m == 1) {
			cout << " ngay ke truoc " << d << "/" << m <<"/" << y << " la: " << 31 << "/" << 12 << "/" <<  y-1 <<"\n";
			cout << " ngay ke sau " << d << "/" << m <<"/" << y << " la: " << d+1 << "/" << m << "/" <<  y <<"\n";
		}

	if ( m == 4 ||  m == 6 ||  m == 9 ||  m == 11 ){ // cac thang co 30 ngay
		if (d >= 2 && d <= 29) {
			cout << " ngay ke truoc " << d << "/" << m <<"/" << y << " la: " << d-1 << "/" << m << "/" << y <<"\n";
			cout << " ngay ke sau " << d << "/" << m <<"/" << y << " la: " << d+1 << "/" << m << "/" <<  y <<"\n";
		}
		if (d == 30) {
			cout << " ngay ke truoc " << d << "/" << m <<"/" << y << " la: " << d-1 << "/" << m << "/" <<  y <<"\n";
			cout << " ngay ke sau " << d << "/" << m <<"/" << y << " la: " << 1 << "/" << m+1 << "/" <<  y <<"\n";
		}
		if (d == 1 ) {
			cout << " ngay ke truoc " << d << "/" << m <<"/" << y << " la: " << 31 << "/" << m-1 << "/" <<  y <<"\n";
			cout << " ngay ke sau " << d << "/" << m <<"/" << y << " la: " << d+1 << "/" << m << "/" <<  y <<"\n";
		}		
}
	
	if (m == 2){ // thang co 28 day
	if ( d >= 2 && d <= 27){
			cout << " ngay ke truoc " << d << "/" << m <<"/" << y << " la: " << d-1 << "/" << m << "/" << y <<"\n";
			cout << " ngay ke sau " << d << "/" << m <<"/" << y << " la: " << d+1 << "/" << m << "/" <<  y <<"\n";
	}
	if (d == 1){
 	cout << " ngay ke truoc " << d << "/" << m <<"/" << y << " la: " << 31 << "/" << 1 << "/" << y <<"\n";
			cout << " ngay ke sau " << d << "/" << m <<"/" << y << " la: " << 2 << "/" << m << "/" <<  y <<"\n";
	}
		if (d == 28){
 	cout << " ngay ke truoc " << d << "/" << m <<"/" << y << " la: " << d-1 << "/" << m << "/" << y <<"\n";
			cout << " ngay ke sau " << d << "/" << m <<"/" << y << " la: " << 1 << "/" << m+1 << "/" <<  y <<"\n";
	}
}
	}
	
	void demngay(int d, int m, int y){ // b)ham dem ngay
		int i, sd, songay = 0, deltasd, s;
		if (m == 1){
		int sn = d - 1;
		s = 365 * (y-1) + sn;
		cout << "so ngay giua 1/1/1 den " << d << "/" << m << "/" << y << " la: " << s << "\n"; 
		}
		else {
		for (int i = 1; i < m; i++){	
	if ( i == 1 || i == 3 ||  i == 5 ||  i == 7 ||  i == 8 ||  i == 10 ||  i == 12 ){ sd = 31;
	// cac thang co 31 ngay 
	}
		if (  i == 4 ||  i == 6 ||  i == 9 ||  i == 11 ){ sd = 30;
		} // cac thang co 30 ngay
		if (i == 2){ sd = 28;
		} // thang co 28 ngay
	songay += sd;  // so ngay tu ngay dau tien toi ngay cuoi cung giua 2 thang
	} deltasd = songay + d; // so ngay con lai	
	
	s = 365 * (y-1) + deltasd; // so ngay trong cac nam
	cout << "so ngay giua 1/1/1 den " << d << "/" << m << "/" << y << " la: " << s << "\n"; 
}
}

void doiamlich(int y){ // c)
 	 string can, chi;
 	int socuoi = y % 10;
 	if (socuoi == 1) can = "TAN";
 	if (socuoi == 2) can = "NHAM";
 	if (socuoi == 3) can = "QUY";
 	if (socuoi == 4) can = "GiAP";
 	if (socuoi == 5) can = "AT";
 	if (socuoi == 6) can = "BINH";
 	if (socuoi == 7) can = "DINH";
 	if (socuoi == 8) can = "MAU";
 	if (socuoi == 9) can = "KI";
 	if (socuoi == 0) can = "CANH";
	 int sothu2 = y % 100;
	 int n = sothu2 % 12;
	 if ( y>=1900 && y <= 1999){
	 	if(n == 1) chi = "SUU";
	 	if(n == 2) chi = "DAN";
	 	if(n == 3) chi = "MEO";
	 	if(n == 4) chi = "THIN";
	 	if(n == 5) chi = "TY";
	 	if(n == 6) chi = "NGO";
	 	if(n == 7) chi = "MUI";
	 	if(n == 8) chi = "THAN";
	 	if(n == 9) chi = "DAU";
	 	if(n == 10) chi = "TUAT";
	 	if(n == 11) chi = "HOI";
	 	if(n == 0) chi = "TYS";
	 }
	 if(y >= 2000){
	 	 if(n == 1) chi = "TY";
	 	if(n == 2) chi = "NGO";
	 	if(n == 3) chi = "MUI";
	 	if(n == 4) chi = "THAN";
	 	if(n == 5) chi = "DAU";
	 	if(n == 6) chi = "TUAT";
	 	if(n == 7) chi = "HOI";
	 	if(n == 8) chi = "TYS";
	 	if(n == 9) chi = "SUU";
	 	if(n == 10) chi = "DAN";
	 	if(n == 11) chi = "MEO";
	 	if(n == 0) chi = "THIN";		
	 }
	 cout << "nam " << can << " " << chi << " = " << y << "\n";
 }
	

int main(){
	int d, m, y, nam;
	cout << "d: "; cin >> d;
	cout << "m: "; cin >> m;
	cout << "y: "; cin >> y;
	cout << d << "/" << m << "/" << y << "\n";
	if (d <= 0 || d >= 32 || m <= 0 || m >= 13 || y <= 0){
		cout << " ngay thang nam khong hop le! \n";
	}
	else{
	cout << "cau a: \n";
	xdngay(d,m,y);
	cout << "cau b: \n";
	demngay(d, m, y);
	cout << "cau c,d: \n";
	cout << "nam(>=1000)= "; cin >> nam;
	if (nam <1000) cout << "nam truoc cong nguyen \n";
	if (nam>=1000 && nam < 1900) cout << "khong co nam am lich \n";
	if (nam>=10000) cout << "nam qua lon \n";
	else doiamlich(nam);
	}
	return 0;
}
