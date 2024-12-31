package game.fountain;

import edu.monash.fit2099.engine.positions.Ground;
import edu.monash.fit2099.engine.positions.Location;

/**
 * Fountain containing water that can heal the player
 */
public class HealingFountain extends Ground {

    /**
     * Constructor.
     */
    public HealingFountain() {
        super('H');
    }

    @Override
    public void tick(Location location){
        if(location.containsAnActor() && location.getItems().isEmpty()){
            location.addItem(new HealingWater());
        }
    }
}
