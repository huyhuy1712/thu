#include<iostream>
#include<math.h>
#include <stack>
#include<cmath>
#include <string>

using namespace std;

int Priority(char c){ // Hàm `priority(char c)` dùng d? xác d?nh d? uu tiên c?a toán t?:
    if(c=='^')// N?u toán t? là `^` thì tr? v? 5.
        return 5;
    else if(c=='*' || c=='/')// N?u toán t? là `*` ho?c `/` thì tr? v? 4.
        return 4; 
    else if(c=='+' || c=='-')// N?u toán t? là `+` ho?c `-` thì tr? v? 2.
        return 3;
    else
        return 2;// Ngu?c l?i, tr? v? 2.
}

string TrungToSangHauTo(string st){ // Hàm `TrungToSangHauTo(string st)` dùng d? chuy?n bi?u th?c trung t? sang bi?u th?c h?u t?.
    stack<char> s;// Ð?u tiên, khai báo m?t stack `s` và m?t chu?i `res` d? luu k?t qu?.
    string res= "";
    double pi = 3.141592654;
    double e = 2.718281828;

    for(int i=0;i<st.length();i++){// Duy?t t?ng ký t? trong chu?i trung t? `st`.
        char c = st[i];
        if(isdigit(c))// N?u ký t? dó là m?t ch? s?, thêm nó vào chu?i h?u t? `res`.
            res += c;
        else if(c == 'p' && st.substr(i, 2) == "pi"){// Xác d?nh `pi`.
            res+= to_string(pi);// Thêm giá tr? `pi` vào.
            i++;// D?ch chuy?n con tr? `i` sang bên ph?i 1 don v?
        }
        else if(c == 'e')// Xác d?nh e.
            res+= to_string(e);// Thêm giá tr? `e` vào.
        else if(c=='(')// N?u ký t? dó là m?t d?u m? ngo?c `(`, thêm nó vào stack `s`.
            s.push(c);
        else if(c==')'){// N?u ký t? dó là m?t d?u dóng ngo?c `)`. 
            while(!s.empty() && s.top()!='('){
                res+=s.top(); // l?y ph?n t? trên d?nh c?a `s` và thêm nó vào chu?i `postfix`, l?p l?i cho d?n khi g?p ph?i d?u m? ngo?c `(`
                s.pop();
            }
            if(!s.empty() && s.top() =='(')
                s.pop();//  Sau dó lo?i b? d?u ngo?c`(` t? stack `s`.
        }
        else{
            while(!s.empty() && Priority(c) <= Priority(s.top())){// N?u ký t? dó là m?t toán t?, l?y ph?n t? trên d?nh c?a `s`. N?u d? uu tiên c?a toán t? trên d?nh `s` l?n hon ho?c b?ng d? uu tiên c?a toán t? hi?n t?i. Cu?i cùng thêm toán t? hi?n t?i vào `s`.
                res+= s.top();//  thì l?y ph?n t? dó ra kh?i `s` và thêm vào chu?i `postfix`, l?p l?i quá trình trên cho d?n khi `s` r?ng ho?c d? uu tiên c?a toán t? trên d?nh `s` nh? hon d? uu tiên c?a toán t? hi?n t?i.
                s.pop();
            }
            s.push(c);// Cu?i cùng thêm toán t? hi?n t?i vào `s`.
        }
    // L?p l?i quá trình cho d?n khi duy?t h?t chu?i trung t? `st`.
    }

    while (!s.empty()) {
res += s.top();// L?y h?t các ph?n t? còn l?i trong `s` ra và thêm vào chu?i `res`.
        s.pop();
    }

    return res;// Tr? v? chu?i h?u t? `res`.
}

double TinhGiaTriHauTo(string res){// Hàm `TinhGiaTriHauTo(string postfix)` dùng d? tính giá tr? c?a bi?u th?c h?u t?.
    stack<double> s;// Ð?u tiên, khai báo m?t stack `s`.
    double pi = 3.141592654;
    double e = 2.718281828;

    for(int i=0;i<res.length();i++){// Duy?t t?ng ký t? trong chu?i h?u t? `res`.
        char c = res[i];
        if(isdigit(c))// N?u ký t? dó là m?t ch? s?, dua nó vào stack `s`.
            s.push(c-'0');// `c-'0'` d? bi?n d?i t? kí t? sang giá tr? vd: '10' = 10
        else if (c == 'p'){// dua giá tr? c?a `pi` vào stack.
            s.push(pi);
            i += 1;
        }
        else if (c == 'e')// dua giá tr? c?a `e` vào stack
            s.push(e);
        else{// N?u ký t? dó là m?t toán t?, l?y hai ph?n t? trên d?nh c?a stack `s`, th?c hi?n phép toán tuong ?ng và dua k?t qu? vào stack `s`.
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
    // L?p l?i quá trình cho d?n khi duy?t h?t chu?i h?u t? `res`.
    }
    //L?y ph?n t? cu?i cùng trên d?nh c?a `s` là k?t qu? c?a bi?u th?c h?u t?.
    return s.top();// Tr? v? k?t qu?.
}

int main(){
    string bt;
    cout<<"Nhap bieu thuc can tinh: ";cin>>bt;
    string res = TrungToSangHauTo(bt);// S? d?ng hàm `TrungToSangHauTo()` d? chuy?n bi?u th?c trung t? sang bi?u th?c h?u t?.
    double kq = TinhGiaTriHauTo(res);// S? d?ng hàm `TinhGiaTriHauTo()` d? tính giá tr? c?a bi?u th?c h?u t?.
    cout<<bt<<"= "<<kq;// Xu?t k?t qu? ra màn hình.

    return 0;
}

