package game.items;

import edu.monash.fit2099.engine.items.Item;
import game.Wallet;
import game.fountain.Water;

import java.util.Stack;

/**
 * The bottle to contain the special waters from the fountain
 */
public class Bottle extends Item {
    private Stack<Water> contents = new Stack<>();
    private static Bottle instance;


    /***
     * Constructor.
     */
    private Bottle() {
        super("Bottle", 'b', false);
    }


    public static Bottle getInstance(){
        if(instance == null){
            instance = new Bottle();
        }
        return instance;
    }

    /**
     * @return a boolean stating whether or not the bottle is empty
     */
    public boolean isEmpty(){
        return contents.empty();
    }

    /**
     * Adds water to the bottle
     * @param water the water to be added
     */
    public void addWaterToBottle(Water water){
        contents.push(water);
    }

    /**
     * Removes water from the bottle
     * @return the removed water
     */
    public Water consumeWater(){
        return contents.pop();
    }

    /**
     * @return the contents of the bottle
     */
    public Stack<Water> getContents(){
        return this.contents;
    }
}

