/**
 * Created by miles on 4/18/17.
 */
import java.util.ArrayList;
import java.util.Random;
import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.File;
import java.io.IOException;
public class Kden {
    public static void main(String[] args) {


        ArrayList<int[]> items = new ArrayList<>();
        Random cool = new Random();

        BufferedWriter output = null;
        try {
            File file = new File("file3part2.txt");
            output = new BufferedWriter(new FileWriter(file));
            String totaltext = "";
            for (int i = 55000; i < 110000; i++) {
                //heavy_worthless_rock; 0; 99; 1; 5
                //[item_name]; [class]; [weight]; [cost]; [resale value]
                int cost = cool.nextInt(200000);
                int resale = cool.nextInt(200000);
                while(resale <= cost) {
                    resale += cool.nextInt(200000 - cost);
                }

                output.write(i + "; "+ i + "; "
                        + cool.nextInt(200000) + "; "
                        + cost + "; "
                        + resale + ";\n");

            }
            //System.out.print(totaltext);
            //output.write(text);
        } catch ( IOException e ) {
            e.printStackTrace();
        }

        try {
            output.close();
        } catch (IOException f) {
            f.printStackTrace();
        }
    }
}

/**
 * item must have alphanumeric name

 N (number of items) <= 200,000

 C (number of incompatibilities) <= 200,000

 resale value should always be larger than cost so its a valid item otherwise people wont choose it

 weight should never be greater than P

 generate 200,000 items
 each has unique name (call them 0-199,999)
 number them 0-199,999
 a weight 0-199,999
 a cost 0-199,999
 a resale cost-199,999
 */
