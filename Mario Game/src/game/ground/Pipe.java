package game.ground;

import edu.monash.fit2099.engine.actions.ActionList;
import edu.monash.fit2099.engine.actors.Actor;
import edu.monash.fit2099.engine.positions.GameMap;
import edu.monash.fit2099.engine.positions.Ground;
import edu.monash.fit2099.engine.positions.Location;
import game.*;
import game.actions.TeleportAction;
import game.actors.PiranhaPlant;
import game.reset.Resettable;

/**
 * A pipe which can be used to teleport to the next map and back
 */
public class Pipe extends Ground implements Jumpable, Resettable {
    int turn = 1;
    Location pipeLocation;
    boolean resetGame;

    /**
     * Constructor
     */
    public Pipe(){
        super('C');
        this.registerInstance();
    }

    @Override
    public int getFallDamage() {
        return 0;
    }

    @Override
    public int getSuccessRate() {
        return 0;
    }


    @Override
    public ActionList allowableActions(Actor otherActor, Location location, String direction){
        ActionList actions = new ActionList();
        if(location.containsAnActor()){
           actions.add(new TeleportAction(otherActor, Application.secondaryMap));
        }
        return actions;
    }

    @Override
    public void tick(Location location) {
        pipeLocation = location;
        if(turn==1){
            location.addActor(new PiranhaPlant());
        }
        turn++;

        if(resetGame){
            if(!pipeLocation.containsAnActor()){ //if pipe location has an actor
                pipeLocation.addActor(new PiranhaPlant());
            }
        }
    }

    @Override
    public void resetInstance() {
        resetGame = true;
    }
}
