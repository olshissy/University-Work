package game.actors;

import edu.monash.fit2099.engine.actions.Action;
import edu.monash.fit2099.engine.actions.ActionList;
import edu.monash.fit2099.engine.actions.DoNothingAction;
import edu.monash.fit2099.engine.actors.Actor;
import edu.monash.fit2099.engine.displays.Display;
import edu.monash.fit2099.engine.positions.GameMap;
import game.Status;
import game.actions.SpeakAction;
import game.actions.WinGameAction;

import java.util.Random;

/**
 * A friendly NPC
 */
public class PrincessPeach extends Actor implements SpeechCapable{
    //private final Map<Integer, Behaviour> behaviours = new TreeMap<>();
    private int age = 1;
    /**
     * Constructor
     */
    public PrincessPeach() {
        super("Princess Peach", 'P', 500);
    }

    @Override
    public ActionList allowableActions(Actor otherActor, String direction, GameMap map) {
        ActionList actions = new ActionList();
        if(otherActor.hasCapability(Status.HAS_KEY)){
            actions.add(new WinGameAction(otherActor));
        }
        return actions;
    }


    @Override
    public Action playTurn(ActionList actions, Action lastAction, GameMap map, Display display) {
        if(this.age % 2 == 0){
            System.out.println("Princess Peach: \"" + this.speak() + "\"");
        }
        age++;

        return new DoNothingAction();
    }

    @Override
    public String speak() {
        Random rand = new Random();
        int randValue = rand.nextInt(3);
        String line;
        if(randValue == 0){
            line = "Dear Mario, I'll be waiting for you...";
        }
        else if(randValue == 1){
            line = "Never gonna give you up!";
        }else{
            line = "Release me, or I will kick you!";
        }
        return line;
    }
}
