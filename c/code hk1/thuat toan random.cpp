
#include <iostream>
#include <cstdlib>
#include <ctime>
using namespace std;

//Tao hàm GetRandom de chi dinh pham vi sinh so ngau nhiên
int GetRandom(int min,int max){
    return min + (int)(rand()*(max-min+1.0)/(1.0+RAND_MAX));
}

int main(){
    //Su dung hàm srand de thay doi so nguon su dung trong hàm rand
    srand((unsigned int)time(NULL));
    
    for (int i = 0;i < 10;i++) {
        cout << GetRandom(1,6)<<endl;
    }
    
    return 0;
}
