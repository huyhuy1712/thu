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
