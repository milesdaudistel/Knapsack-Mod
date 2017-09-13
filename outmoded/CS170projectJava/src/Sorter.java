/**
 * Created by miles on 4/26/17.
 */
import java.util.ArrayList;
import java.util.Random;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.File;
import java.io.IOException;
public class Sorter {
    public static void main(String[] args) {
        //[P pounds]
        //[M dollars]
        //[N number of items]
        //[C number of constraints]

        //BufferedReader in = new BufferedReader(new FileReader("foo.in"));

        //put a file into buffered reader
        //create an arraylist of arraylists
        //each arraylist holds the strings of that class type
        //arraylist of arraylists numbered from 0 to N-1, since classes can be 0 to N-1
        //read a line
        //split based on semicolons
        //look at second parameter, the class
        //add that to arraylist of arraylists at the index = to its class #
        //now you have an array of arrays, with each array containing 1 class
        //print to new file
        //add in constraints later

        ArrayList<ArrayList<String>> classes = new ArrayList<>();

        BufferedReader input = null;
        BufferedWriter output = null;
        try {

            input = new BufferedReader(new FileReader("project_instances/problem1.in"));


            File file = new File("got_eem.txt");

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
//sort the items according to class in ascending order
//sort the constraints horizontally in ascending order
//sort the constraints vertically in ascending order

//compare items within a class to check for superior items
//delete the inferior items

//compare classes to see if there are any superior classes