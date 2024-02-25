import java.util.*;
import javax.sound.sampled.SourceDataLine;
public class bt21 {
    public static void main(String[] args) {
    int max = 1000;
    int min = 0;
    Random r = new Random();
    int n = r.nextInt(max - min + 1) + min;
    System.out.println(n);
}
}
