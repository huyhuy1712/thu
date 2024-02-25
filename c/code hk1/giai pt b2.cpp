#include <stdio.h>
#include <math.h> 

int main(){
	float a,b,c;
	printf("nhap a: ");
	scanf("%f",&a); 
	printf("nhap b: ");
	scanf("%f",&b);
	printf("nhap c: ");
	scanf("%f",&c);
	
	float delta = b*b - (4*a*c);
	float x1, x2; 
	 if(delta > 0){
	 	x1 = (-b + sqrt(delta)) / (2*a);
		 x2 = (-b - sqrt(delta)) / (2*a); 
	 }
	 if(delta == 0){
	 	x1 = x2 = (-b) / (2*a) ;
	 } 
	 else{
	 	printf("pt vo nghiem"); 
	 }
	 printf("x1= %f\nx2= %f",x1,x2); 
} 
