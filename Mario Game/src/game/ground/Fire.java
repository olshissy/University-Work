package game.ground;

import edu.monash.fit2099.engine.actors.Actor;
import edu.monash.fit2099.engine.positions.Ground;
import edu.monash.fit2099.engine.positions.Location;
import game.Status;

/**
 * Used for bowser and when the player has the fire flower active (for attacking)
 */
public class Fire extends Ground {
    int turns = 0;
    Ground ground;

    public Fire(Ground ground) {
        super('v');
        this.ground = ground;
    }

    @Override
    public void tick(Location location) {
        if(turns >=3){
            location.setGround(ground);
        }
        if(location.containsAnActor()) {
            location.getActor().hurt(20);
        }

        turns++;
    }
}
