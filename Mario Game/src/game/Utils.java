package game;

import java.util.Random;

public class Utils {
    public static int rollChance(){
        /**
         * Call function to generate random value from 0 - 100
         */

        Random r = new Random();
        return (r.nextInt(100));
    }
}
