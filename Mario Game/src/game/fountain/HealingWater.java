package game.fountain;

import game.actions.FillUpBottleAction;

/**
 * Water that heals the player
 */
public class HealingWater extends Water {
    /**
     * Constructor
     */
    public HealingWater() {
        super("Health", 50);
        super.setDisplayChar('H');
        this.addAction(new FillUpBottleAction(this));
    }
}
