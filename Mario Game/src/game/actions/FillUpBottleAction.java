package game.actions;

import edu.monash.fit2099.engine.actions.Action;
import edu.monash.fit2099.engine.actors.Actor;
import edu.monash.fit2099.engine.positions.GameMap;
import game.fountain.Water;
import game.items.Bottle;

/**
 * Special action for filling up the bottle
 */
public class FillUpBottleAction extends Action {
    private final Water water;

    /**
     * Constructor
     *
     * @param water the water to fill up the bottle with
     */
    public FillUpBottleAction(Water water){
        this.water = water;
    }

    /**
     * Fill up the bottle with the required water
     *
     * @see Action#execute(Actor, GameMap)
     * @param actor The actor performing the action
     * @param map The map the actor is on
     * @return a suitable desctiption to display in the UI
     */
    @Override
    public String execute(Actor actor, GameMap map){
        Bottle.getInstance().addWaterToBottle(this.water);
        map.locationOf(actor).removeItem(water);
        return menuDescription(actor);
    }

    /**
     * Describe the action in a format suitable for displaying in the menu
     *
     * @see Action#menuDescription(Actor)
     * @param actor The actor performing the action
     * @return a string, e.g. "Player picks up the rock"
     */
    @Override
    public String menuDescription(Actor actor){
        return actor + " refills " + water.getClass().getSimpleName();
    }

}
