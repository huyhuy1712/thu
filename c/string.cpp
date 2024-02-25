#include <stdio.h>
#include <string.h>
using namespace std;
	void uber(char string[]){   //ham doi tat ca ki tu trong chuoi thanh in hoa giong ham strupr(string)
		int length = strlen(string);
	for(int i = 0; i < length; i++){
		if(string[i] >= 'a' && string[i] <= 'z'){
			string[i] = string[i] - 32;
		}
	}
	} 
	
	void lower(char str[]){     // ham thay doi tu chu thuong sang chu in hoa giong ham strlwr(string)
	int length = strlen(str);
	for(int i = 0; i < length; i++){
		if(str[i] >= 65 &&  str[i] <= 90){
			str[i] = str[i] + 32;
		}
	} 
	}

	void proper(char str[]){  // ham doi cac ki tu dau tien cua moi tu sang in hoa
	if(str[0] >= 'a' && str[0] <= 'z'){
		str[0] -= 32;
	for(int i = 0; i < strlen(str); i++){
		if(str[i] == ' '){
			if(str[i+1] >= 'a' && str[i+1] <= 'z'){
				str[i+1] -= 32;
			}
			else continue;
		}
	}	
	}
}
	
	void xoa(char*s, int pos){
		int length = strlen(s);
		for(int i = pos; i < length; i++){
			s[i] = s[i+1];
		}
		length--;
	} 
	
	void standard(char *str){  // ham dinh chuan chuoi 
		int length = strlen(str);
		 if(str[0] == ' '){
			xoa(str,0);
		}
	if(str[length-1] == ' '){
		xoa(str,length-1);
	}
		for(int i = 1; i < length-1; i++){
		if(str[i] == ' ' && str[i+1] == ' '){
		xoa(str,i);
		i--;
		}	
}
}
		
void xoakt(char *s){   // ham xoa tat ca khoang trang
	int length = strlen(s);
	for(int i = 0; i < length; i++){
		if(s[i] == ' '){
		xoa(s,i);
		i--;
		}
	}
}

void xuattu(char* s, int k){  // ham xuat 1 tu cua chuoi tai vi tri tu thu k dau tien
	for(int i = k; s[i] != ' '; i++){
		printf("%c",s[i]); 
	}
}

	void tumax(char* s){ //tim tu co do dai lon nhat
	char *word = strtok(s," ");
	char *word_max = word;
	int length_max = strlen(word);
	while(word != NULL){
	word = strtok(NULL," ");
	if(word != NULL){
	int length = strlen(word);
	if(length >= length_max){
		length_max = length;
		word_max = word;
	}	
	}
}
	printf("%stu dai nhat chuoi la: ",word_max);
}

void xuattaivitri(char* s,int pos,int n) {// Trích ra n ký t? d?u tiên/cu?i cùng/b?t d?u tai vi tri pos
	for(int i = pos; i <= n; i++){
		printf("%c",s[i]);
	}
}

void demtu(char *s){ /// so so luong tu co trong chuoi
	int count = 0;
	int length = strlen(s);
	for(int i = 0; i < length; i++){
		if(s[i] == ' '){
			count++;
		}
		}
	printf("so tu cua chuoi la: %d\n",count+1);
	for(int i = 0; i < length; i++){
		if(s[i] != ' '){
			printf("%c",s[i]);
	}
	else{
		printf("\n");
	}
}
}
	int main(){
 	char str[50];
 	printf("nhap chuoi: ");
 	gets(str);
 	xoakt(str);
 	puts(str);
}
