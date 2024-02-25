#include <bits/stdc++.h>
using namespace std;
struct SoPhuc{
	double sothuc;
	double soao;

	SoPhuc operator + (const SoPhuc other){ //dinh nghia operator trong struct
		SoPhuc tong;
		tong.sothuc = sothuc + other.sothuc; 
		tong.soao = soao + other.soao; 
		return tong;
	}
	
	SoPhuc operator - (const SoPhuc other){
		SoPhuc hieu;
		hieu.sothuc = sothuc - other.sothuc;
		hieu.soao = soao - other.soao;
		return hieu;
	}
		
	void Nhap(){
	cout << "Nhap phan thuc: "; 
	cin >> sothuc;
	cin.ignore(); // lam sach bo nho dem
	cout << "Nhap phan ao: ";
	 cin >> soao;
	 cin.ignore();
	 }	

	void Xuat(){
	cout << "so phuc: ";
	cout << sothuc << "+" << soao << "i" << "\n";
	cout << "modun: " << sqrt(pow(sothuc,2) + pow(soao,2)) << "\n";
}
};
int main(){
 SoPhuc z1, z2, tong, hieu;
 z1.Nhap();
 z1.Xuat();
 z2.Nhap();
 z2.Xuat();
 tong = z1 + z2;
 hieu = z1 - z2;
 cout << "tong 2 so phuc: " << tong.sothuc << "+" << tong.soao << "i" << "\n";
  cout << "hieu 2 so phuc: " << hieu.sothuc << "+" << hieu.soao << "i" << "\n";
}
