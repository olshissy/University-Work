package game.actors;


import edu.monash.fit2099.engine.actions.Action;
import edu.monash.fit2099.engine.actions.ActionList;
import edu.monash.fit2099.engine.actors.Actor;
import edu.monash.fit2099.engine.displays.Display;
import edu.monash.fit2099.engine.actions.DoNothingAction;
import edu.monash.fit2099.engine.positions.GameMap;
import edu.monash.fit2099.engine.weapons.IntrinsicWeapon;
import game.*;
import game.actions.AttackAction;
import game.behaviours.AttackBehaviour;
import game.behaviours.Behaviour;
import game.behaviours.FollowBehaviour;
import game.behaviours.WanderBehaviour;
import game.reset.Resettable;

//import java.util.HashMap;
import java.util.Random;
import java.util.TreeMap;
import java.util.Map;
/**
 * A turtle that can fly
 */
public class FlyingKoopa extends AbstractKoopa implements Resettable, SpeechCapable {
//    private final Map<Integer, Behaviour> behaviours = new TreeMap<>(); // priority, behaviour
//    private GameMap map;
//    private boolean resetGame = false;
    private int age = 1;

    /**
     * Constructor.
     */
    public FlyingKoopa() {
        super("Flying Koopa", 'F', 150);
        this.addCapability(Status.CAN_FLY);
    }

    @Override
    public String speak() {
        Random rand = new Random();
        int randValue = rand.nextInt(3);
        String line;
        if(randValue == 0){
            line = "Never gonna make you cry!";
        } else if(randValue == 1){
            line = "Koopi koopi koopii~!";
        }else{
            line = "Pam pam pam!";
        }
        return line;
    }
}
