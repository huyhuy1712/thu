
#include <iostream>
#include <cstdlib>
#include <ctime>
using namespace std;

//Tao h�m GetRandom de chi dinh pham vi sinh so ngau nhi�n
int GetRandom(int min,int max){
    return min + (int)(rand()*(max-min+1.0)/(1.0+RAND_MAX));
}

int main(){
    //Su dung h�m srand de thay doi so nguon su dung trong h�m rand
    srand((unsigned int)time(NULL));
    
    for (int i = 0;i < 10;i++) {
        cout << GetRandom(1,6)<<endl;
    }
    
    return 0;
}
