package game.fountain;

import game.actions.FillUpBottleAction;

/**
 * Water that increases the player's damage
 */
public class PowerWater extends Water {

    /**
     * Constructor
     */
    public PowerWater() {
        super("Power", 15);
        super.setDisplayChar('A');
        this.addAction(new FillUpBottleAction(this));
    }
}
