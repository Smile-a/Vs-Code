package MyJavaDemo;

import java.util.ArrayList;
import java.util.Arrays;

public class javaDemo {
    public static void main(String[] args) {
        String[] arr = new String[] { "1", "2" };
        ArrayList<String> params = new ArrayList<>();
        for (String s : arr) {
            params.add("'" + s + "'");
        }
        System.out.println(String.join(",", params));
    }
}