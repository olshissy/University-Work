package game.actions;

import edu.monash.fit2099.engine.actions.Action;
import edu.monash.fit2099.engine.actors.Actor;
import edu.monash.fit2099.engine.positions.GameMap;
import game.Status;

import java.util.Random;

/**
 * A special action for speaking with other actors
 */
public class SpeakAction extends Action {
    private Actor target;

    /**
     * Constructor
     * @param target the target of the monologue
     */
    public SpeakAction(Actor target){
        this.target = target;
    }


    @Override
    public String execute(Actor actor, GameMap map) {
        Random random = new Random();
        int randomInt = 0;
        if(actor.hasCapability(Status.STAR) && actor.getWeapon().toString().equals("Wrench")){
            while(randomInt <= 1){
                randomInt = random.nextInt(4);
            }
        } else if (actor.hasCapability(Status.STAR)){
            randomInt = 1;
            while(randomInt==1){
                randomInt = random.nextInt(4);
            }
        } else if (actor.getWeapon().toString().equals("Wrench")){
            while(randomInt==0){
                randomInt = random.nextInt(4);
            }
        }else{
            randomInt = random.nextInt(4);
        }

        switch(randomInt){
            case 0:
                return "You might need a wrench to smash Koopa's hard shells.";
            case 1:
                return "You better get back to finding the Power Stars.";
            case 2:
                return "The Princess is depending on you! You are our only hope.";
            case 3:
                return "Being imprisoned in these walls can drive a fungus crazy :(";
        } return null;
    }

    @Override
    public String menuDescription(Actor actor) {
        return String.format("Mario talks with %s",target.toString());
    }
}
