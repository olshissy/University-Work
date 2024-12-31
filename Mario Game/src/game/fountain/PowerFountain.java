package game.fountain;

import edu.monash.fit2099.engine.positions.Ground;
import edu.monash.fit2099.engine.positions.Location;

/**
 * Fountain containing water that increases the player's damage
 */
public class PowerFountain extends Ground {
    /**
     * Constructor.
     */
    public PowerFountain() {
        super('A');
    }

    @Override
    public void tick(Location location){
        if (location.containsAnActor() && location.getItems().isEmpty()){
            location.addItem(new PowerWater());
        }
    }
}
