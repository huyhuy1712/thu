import java.util.Scanner;
public class bt7 {
    public static void main(String[] args){
        Scanner input = new Scanner(System.in);
        System.out.print("nhap ngay: ");
        int ngay = input.nextInt();
        System.out.print("nhap thang: ");
        int thang = input.nextInt();
        System.out.print("nhap nam: ");
        int nam = input.nextInt();
                switch(thang){
            case 2: // tháng có 28 ngày
            if(ngay < 28 || ngay > 1){
                System.out.println("ngay truoc: "+(ngay-1)+"/"+thang+"/"+nam);
                System.out.println("ngay sau: "+(ngay+1)+"/"+thang+"/"+nam);
            }
            if(ngay == 28){
            System.out.println("ngay truoc: "+(ngay-1)+"/"+thang+"/"+nam);
            System.out.println("ngay sau: 1/"+(thang+1)+"/"+nam);
            }
            if(ngay == 1){
                System.out.println("ngay truoc: 31/"+(thang-1)+"/"+nam);
                System.out.println("ngay sau: "+(ngay+1)+"/"+thang+"/"+nam);
            }
            break;
        case 1,3,5,7,8,10,12: // tháng có 31 ngày
        if(ngay < 31 || ngay > 1){
            System.out.println("ngay truoc: "+(ngay-1)+"/"+thang+"/"+nam);
            System.out.println("ngay sau: "+(ngay+1)+"/"+thang+"/"+nam);
        }
        if(ngay == 31 && thang == 12 ){
            System.out.println("ngay truoc: "+(ngay-1)+"/"+thang+"/"+nam);
            System.out.println("ngay sau: 1/1"+"/"+nam+1);
        }
        if(ngay == 1 && thang == 1){
            System.out.println("ngay truoc: 31/12/"+(nam-1));
            System.out.println("ngay sau: "+(ngay+1)+"/"+thang+"/"+nam);
        }
        if(ngay == 31 && thang != 12){
            System.out.println("ngay truoc: "+(ngay-1)+"/"+thang+"/"+nam);
            System.out.println("ngay sau: 1/"+(thang+1)+"/"+(nam+1));
        }
        if(ngay == 1 && thang != 1 && thang != 8){
            System.out.println("ngay truoc: 30/"+(thang-1)+"/"+nam);
            System.out.println("ngay sau: "+(ngay+1)+"/"+thang+"/"+nam);
        }
if(ngay == 1 && thang == 8){
    System.out.println("ngay truoc: 31/"+(thang-1)+"/"+nam);
    System.out.println("ngay sau: "+(ngay+1)+"/"+thang+"/"+nam);
}
break;
default: // tháng có 30 ngày
    if(ngay < 30 || ngay > 1){
        System.out.println("ngay truoc: "+(ngay-1)+"/"+thang+"/"+nam);
        System.out.println("ngay sau: "+(ngay+1)+"/"+thang+"/"+nam);
}
if(ngay == 30){
    System.out.println("ngay truoc: "+(ngay-1)+"/"+thang+"/"+nam);
    System.out.println("ngay sau: 1/"+(thang+1)+"/"+nam);
    }
    if(ngay == 1){
        System.out.println("ngay truoc: 31/"+(thang-1)+"/"+nam);
        System.out.println("ngay sau: "+(ngay+1)+"/"+thang+"/"+nam);
}
    }
}}
