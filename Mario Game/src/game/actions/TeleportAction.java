package game.actions;

import edu.monash.fit2099.engine.actions.Action;
import edu.monash.fit2099.engine.actions.MoveActorAction;
import edu.monash.fit2099.engine.actors.Actor;
import edu.monash.fit2099.engine.positions.GameMap;
import edu.monash.fit2099.engine.positions.Location;
import game.behaviours.TeleportationSingleton;

/**
 * Special action for teleporting to the second map and back
 */
public class TeleportAction extends Action {
    Actor actor;
    GameMap secondaryMap;

    /**
     * Constructor
     * @param actor the actor that is teleporting
     * @param secondaryMap the map the player is teleporting to
     */
    public TeleportAction(Actor actor, GameMap secondaryMap){
        this.actor = actor;
        this.secondaryMap = secondaryMap;
    }

    @Override
    public String execute(Actor actor, GameMap map) {
        if(secondaryMap.at(0,0).containsAnActor()){
            Actor pipeActor = secondaryMap.at(0,0).getActor();
            secondaryMap.removeActor(pipeActor);
        }
        if(TeleportationSingleton.getInstance().isWarped()){
            GameMap returnMap = TeleportationSingleton.getInstance().getEarliestMap();
            Location returnCoordinates = TeleportationSingleton.getInstance().getEarliestLocation();
            map.moveActor(actor, returnMap.at(returnCoordinates.x(),returnCoordinates.y()));
        }else{
            TeleportationSingleton.getInstance().addNewCoordinate(map,map.locationOf(actor));
            map.moveActor(actor, secondaryMap.at(0,0));
        }
        
        return "Player successfuly Teleported";
    }

    @Override
    public String menuDescription(Actor actor) {
        return actor + " uses the warp pipe";
    }
}
