import java.util.List;
import java.util.ArrayList;

public class Sample {

    public int add(int a, int b) {
        return a + b;
    }

    public void printAll(List<String> items) {
        for (String item : items) {
            if (item != null) {
                System.out.println(item);
            }
        }
    }

    public static void main(String[] args) {
        Sample s = new Sample();
        System.out.println(s.add(2, 3));
    }
}
