package game.actions;

import edu.monash.fit2099.engine.actions.Action;
import edu.monash.fit2099.engine.actors.Actor;
import edu.monash.fit2099.engine.positions.GameMap;
import game.Status;

/**
 * Special action for ending the game
 */
public class WinGameAction extends Action {
    private Actor target;

    /**
     * Constructor
     * @param target the actor who is going to win the game
     */
    public WinGameAction(Actor target){
        this.target = target;
    }

    @Override
    public String execute(Actor actor, GameMap map) {
        map.removeActor(this.target);
        return "Mario has rescued Peach and won the game";
    }

    @Override
    public String menuDescription(Actor actor) {
        return actor + " recues Peach";
    }
}
