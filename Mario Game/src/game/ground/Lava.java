package game.ground;

import edu.monash.fit2099.engine.actors.Actor;
import edu.monash.fit2099.engine.positions.Ground;
import edu.monash.fit2099.engine.positions.Location;
import game.Status;

/**
 * Ground in the second map of the game
 */
public class Lava extends Ground {
    /**
     * Constructor.
     * has the capabilites of hurting the player that steps on it
     */
    public Lava() {
        super('L');
    }

    @Override
    public boolean canActorEnter(Actor actor) {
        boolean res = false;
        if (actor.hasCapability(Status.CAN_ENTER)){
            res = true;
        }
        return res;
    }

    @Override
    /**
     * Each tick will check if player is standing on the lava and hurt the player accordingly
     */
    public void tick(Location location) {
        if(location.containsAnActor()){
            location.getActor().hurt(15);
        }
    }
}
