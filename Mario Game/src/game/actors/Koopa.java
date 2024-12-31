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
 * A turtle.
 */
public class Koopa extends AbstractKoopa implements Resettable {
//    private final Map<Integer, Behaviour> behaviours = new TreeMap<>(); // priority, behaviour
//    private GameMap map;
//    private boolean resetGame = false;
    private int age = 1;

    /**
     * Constructor.
     */
    public Koopa() {
        super("Koopa", 'K', 100);
    }

}
