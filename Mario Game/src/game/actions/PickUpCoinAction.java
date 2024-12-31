package game.actions;

import edu.monash.fit2099.engine.actions.Action;
import edu.monash.fit2099.engine.actors.Actor;
import edu.monash.fit2099.engine.positions.GameMap;
import game.items.Coin;
import game.Wallet;

/**
 * Special action for picking up coins
 */
public class PickUpCoinAction extends Action{
    private final Coin item;

    /**
     * Constructor.
     *
     * @param item the coin to pick up
     */
    public PickUpCoinAction(Coin item) {
        this.item = item;
    }

    /**
     * Add the coin value to the wallet value
     *
     * @see Action#execute(Actor, GameMap)
     * @param actor The actor performing the action.
     * @param map The map the actor is on.
     * @return a suitable description to display in the UI
     */
    @Override
    public String execute(Actor actor, GameMap map) {
        Wallet.getInstance().increaseWalletValue(this.item.getValue());
        map.locationOf(actor).removeItem(item);
        return menuDescription(actor);
    }

    /**
     * Describe the action in a format suitable for displaying in the menu.
     *
     * @see Action#menuDescription(Actor)
     * @param actor The actor performing the action.
     * @return a string, e.g. "Player picks up the rock"
     */
    @Override
    public String menuDescription(Actor actor) {
        return actor + " picks up the " + item;
    }
}
