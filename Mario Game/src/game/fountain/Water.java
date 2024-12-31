package game.fountain;

import edu.monash.fit2099.engine.items.Item;

/**
 * Abstract water class
 */
public abstract class Water extends Item {
    private String effect;
    private int increaseInEffect;

    /**
     * Constructor
     * @param effect effect the water has on the player
     * @param increaseInEffect the value which the effect is increased by
     */
    public Water(String effect, int increaseInEffect){
        super("Water", 'w', false);
        this.effect = effect;
        this.increaseInEffect = increaseInEffect;
    }

    /**
     * @return effect the water has on a player
     */
    public String getEffect(){
        return this.effect;
    }

    /**
     * @return the value which the effect is increased by
     */
    public int getIncreaseInEffect(){
        return this.increaseInEffect;
    }
}
