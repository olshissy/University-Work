package game.behaviours;

import edu.monash.fit2099.engine.actions.Action;
import edu.monash.fit2099.engine.actors.Actor;
import edu.monash.fit2099.engine.positions.Exit;
import edu.monash.fit2099.engine.positions.GameMap;
import game.actions.AttackAction;

import java.util.List;

/**
 * Represents a factory for creating an attack action
 */
public class AttackBehaviour implements Behaviour {
    private Actor target;
    private String direction;


    @Override
    public Action getAction(Actor actor, GameMap map) {
        List<Exit> exitList;
        exitList = map.locationOf(actor).getExits();
        int counter = 0;

        while (counter < exitList.size()){
            if (exitList.get(counter).getDestination().containsAnActor()) {
                if (exitList.get(counter).getDestination().getActor().getClass().getName().equals("game.actors.Player")){
                    target = exitList.get(counter).getDestination().getActor();
                    direction = exitList.get(counter).getName();
                    return new AttackAction(target, direction);
                }
            }
            counter++;}
        return null;}
}