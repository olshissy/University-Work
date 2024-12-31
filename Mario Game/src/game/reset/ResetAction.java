package game.reset;

import edu.monash.fit2099.engine.actions.Action;
import edu.monash.fit2099.engine.actors.Actor;
import edu.monash.fit2099.engine.positions.GameMap;

/**
 * A special action for resetting the game
 */
public class ResetAction extends Action {
    boolean counter;
    ResetManager resetManager = ResetManager.getInstance();
    @Override
    public String execute(Actor actor, GameMap map) {
        resetManager.run();
        return "Reset Complete";

    }
    @Override
    public String hotkey(){
        return "r";
    }

    @Override
    public String menuDescription(Actor actor) {
       return "Reset Game";
    }
}
