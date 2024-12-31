package game.actions;

import edu.monash.fit2099.engine.actions.Action;
import edu.monash.fit2099.engine.actors.Actor;
import edu.monash.fit2099.engine.positions.GameMap;
import game.Status;
import game.fountain.Water;
import game.items.Bottle;

import java.util.ArrayList;
import java.util.Stack;

/**
 * Special action for consuming water
 */
public class DrinkWaterAction extends Action {
    private Water water;

    /**
     * Constructor
     */
    public DrinkWaterAction(){
        this.water = Bottle.getInstance().getContents().peek();
    }


    @Override
    public String execute(Actor actor, GameMap map) {
        if(this.water.getEffect().equals("Power") ){
            actor.addCapability(Status.POWER_UP);
        }
        else if (this.water.getEffect().equals("Health")){
            int increase = this.water.getIncreaseInEffect();
            actor.increaseMaxHp(increase);
        }

        Bottle.getInstance().consumeWater();

        return actor + " drinks " + this.water.getClass().getSimpleName();
    }

    @Override
    public String menuDescription(Actor actor) {
        ArrayList<String> bottleContents = new ArrayList<>();
        for(Water water: Bottle.getInstance().getContents()){
            bottleContents.add(water.getClass().getSimpleName());
        }
        String returnString = actor + " consumes Bottle[";

        for(int i = 0; i <= Bottle.getInstance().getContents().size()-2; i++){
            returnString += bottleContents.get(i);
            returnString += ", ";
        }

        if(!Bottle.getInstance().isEmpty()){
            returnString += bottleContents.get(Bottle.getInstance().getContents().size()-1);
        }
        return returnString + "]";
    }
}

