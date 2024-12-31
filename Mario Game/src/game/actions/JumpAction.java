package game.actions;

import edu.monash.fit2099.engine.actions.Action;
import edu.monash.fit2099.engine.actors.Actor;
import edu.monash.fit2099.engine.positions.GameMap;
import edu.monash.fit2099.engine.positions.Location;
import game.Status;
import game.ground.Jumpable;
import game.Utils;

/**
 * Special action for jumping onto higher grounds
 */
public class JumpAction extends Action {

    private Jumpable targetOfJump;
    private String direction;
    private Location locationOfJump;


    /**
     * Constructor
     * @param targetOfJump the ground where the player is going to jump
     * @param direction the direction of the jump
     * @param locationOfJump the location of the ground where the player is going to jump
     */
    public JumpAction(Jumpable targetOfJump,String direction, Location locationOfJump){
        this.targetOfJump = targetOfJump;
        this.direction = direction;
        this.locationOfJump = locationOfJump;

    }


    @Override
    public String execute(Actor actor, GameMap map) {
        Location actorLocation = map.locationOf(actor);
        String results;

        if(actor.hasCapability(Status.CAN_FLY)){
            map.moveActor(actor, locationOfJump);
        }

        if(actor.hasCapability(Status.MUSHROOM)){
            map.moveActor(actor, locationOfJump);
            results = String.format("Successful jump made!");
        } else if(Utils.rollChance() <=this.targetOfJump.getSuccessRate()){
            map.moveActor(actor, locationOfJump);
            results = String.format("Successful jump made!");
        }else{
            actor.hurt(this.targetOfJump.getFallDamage());
            results = String.format("Jump was not successful");
        }

        return results;
    }

    @Override
    public String menuDescription(Actor actor) {
        return actor + " Jumps to " + direction;
    }
}
