#include<iostream>
#include<math.h>
#include <stack>
#include<cmath>
#include <string>

using namespace std;

int Priority(char c){ // H�m `priority(char c)` d�ng d? x�c d?nh d? uu ti�n c?a to�n t?:
    if(c=='^')// N?u to�n t? l� `^` th� tr? v? 5.
        return 5;
    else if(c=='*' || c=='/')// N?u to�n t? l� `*` ho?c `/` th� tr? v? 4.
        return 4; 
    else if(c=='+' || c=='-')// N?u to�n t? l� `+` ho?c `-` th� tr? v? 2.
        return 3;
    else
        return 2;// Ngu?c l?i, tr? v? 2.
}

string TrungToSangHauTo(string st){ // H�m `TrungToSangHauTo(string st)` d�ng d? chuy?n bi?u th?c trung t? sang bi?u th?c h?u t?.
    stack<char> s;// �?u ti�n, khai b�o m?t stack `s` v� m?t chu?i `res` d? luu k?t qu?.
    string res= "";
    double pi = 3.141592654;
    double e = 2.718281828;

    for(int i=0;i<st.length();i++){// Duy?t t?ng k� t? trong chu?i trung t? `st`.
        char c = st[i];
        if(isdigit(c))// N?u k� t? d� l� m?t ch? s?, th�m n� v�o chu?i h?u t? `res`.
            res += c;
        else if(c == 'p' && st.substr(i, 2) == "pi"){// X�c d?nh `pi`.
            res+= to_string(pi);// Th�m gi� tr? `pi` v�o.
            i++;// D?ch chuy?n con tr? `i` sang b�n ph?i 1 don v?
        }
        else if(c == 'e')// X�c d?nh e.
            res+= to_string(e);// Th�m gi� tr? `e` v�o.
        else if(c=='(')// N?u k� t? d� l� m?t d?u m? ngo?c `(`, th�m n� v�o stack `s`.
            s.push(c);
        else if(c==')'){// N?u k� t? d� l� m?t d?u d�ng ngo?c `)`. 
            while(!s.empty() && s.top()!='('){
                res+=s.top(); // l?y ph?n t? tr�n d?nh c?a `s` v� th�m n� v�o chu?i `postfix`, l?p l?i cho d?n khi g?p ph?i d?u m? ngo?c `(`
                s.pop();
            }
            if(!s.empty() && s.top() =='(')
                s.pop();//  Sau d� lo?i b? d?u ngo?c`(` t? stack `s`.
        }
        else{
            while(!s.empty() && Priority(c) <= Priority(s.top())){// N?u k� t? d� l� m?t to�n t?, l?y ph?n t? tr�n d?nh c?a `s`. N?u d? uu ti�n c?a to�n t? tr�n d?nh `s` l?n hon ho?c b?ng d? uu ti�n c?a to�n t? hi?n t?i. Cu?i c�ng th�m to�n t? hi?n t?i v�o `s`.
                res+= s.top();//  th� l?y ph?n t? d� ra kh?i `s` v� th�m v�o chu?i `postfix`, l?p l?i qu� tr�nh tr�n cho d?n khi `s` r?ng ho?c d? uu ti�n c?a to�n t? tr�n d?nh `s` nh? hon d? uu ti�n c?a to�n t? hi?n t?i.
                s.pop();
            }
            s.push(c);// Cu?i c�ng th�m to�n t? hi?n t?i v�o `s`.
        }
    // L?p l?i qu� tr�nh cho d?n khi duy?t h?t chu?i trung t? `st`.
    }

    while (!s.empty()) {
res += s.top();// L?y h?t c�c ph?n t? c�n l?i trong `s` ra v� th�m v�o chu?i `res`.
        s.pop();
    }

    return res;// Tr? v? chu?i h?u t? `res`.
}

double TinhGiaTriHauTo(string res){// H�m `TinhGiaTriHauTo(string postfix)` d�ng d? t�nh gi� tr? c?a bi?u th?c h?u t?.
    stack<double> s;// �?u ti�n, khai b�o m?t stack `s`.
    double pi = 3.141592654;
    double e = 2.718281828;

    for(int i=0;i<res.length();i++){// Duy?t t?ng k� t? trong chu?i h?u t? `res`.
        char c = res[i];
        if(isdigit(c))// N?u k� t? d� l� m?t ch? s?, dua n� v�o stack `s`.
            s.push(c-'0');// `c-'0'` d? bi?n d?i t? k� t? sang gi� tr? vd: '10' = 10
        else if (c == 'p'){// dua gi� tr? c?a `pi` v�o stack.
            s.push(pi);
            i += 1;
        }
        else if (c == 'e')// dua gi� tr? c?a `e` v�o stack
            s.push(e);
        else{// N?u k� t? d� l� m?t to�n t?, l?y hai ph?n t? tr�n d?nh c?a stack `s`, th?c hi?n ph�p to�n tuong ?ng v� dua k?t qu? v�o stack `s`.
            double a = s.top();
            s.pop();
            double b = s.top();
            s.pop();

            switch (c) {
                case '+':
                    s.push(b + a);
                    break;
                case '-':
                    s.push(b - a);
                    break;
                case '*':
                    s.push(b * a);
                    break;
                case '/':
                    s.push(b / a);
                    break;
                case '^':
                    s.push(pow(b,a));
                    break;
            }
        }
    // L?p l?i qu� tr�nh cho d?n khi duy?t h?t chu?i h?u t? `res`.
    }
    //L?y ph?n t? cu?i c�ng tr�n d?nh c?a `s` l� k?t qu? c?a bi?u th?c h?u t?.
    return s.top();// Tr? v? k?t qu?.
}

int main(){
    string bt;
    cout<<"Nhap bieu thuc can tinh: ";cin>>bt;
    string res = TrungToSangHauTo(bt);// S? d?ng h�m `TrungToSangHauTo()` d? chuy?n bi?u th?c trung t? sang bi?u th?c h?u t?.
    double kq = TinhGiaTriHauTo(res);// S? d?ng h�m `TinhGiaTriHauTo()` d? t�nh gi� tr? c?a bi?u th?c h?u t?.
    cout<<bt<<"= "<<kq;// Xu?t k?t qu? ra m�n h�nh.

    return 0;
}

