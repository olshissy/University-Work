package game.items;

import edu.monash.fit2099.engine.actors.Actor;
import edu.monash.fit2099.engine.positions.GameMap;

public interface Consumables{
    /**
     * Gives the effects of a consumable item to the user
     * @param actor the actor consuming the item
     * @param map the game map
     * @return a string value stating the actor is under the effects of the item
     */
    String getEffects(Actor actor, GameMap map);
}