package game.actors;

import edu.monash.fit2099.engine.actions.Action;
import edu.monash.fit2099.engine.actions.ActionList;
import edu.monash.fit2099.engine.actions.DoNothingAction;
import edu.monash.fit2099.engine.actors.Actor;
import edu.monash.fit2099.engine.displays.Display;
import edu.monash.fit2099.engine.items.Item;
import edu.monash.fit2099.engine.positions.GameMap;
import game.items.PowerStar;
import game.Status;
import game.items.SuperMushroom;
import game.items.Wrench;
import game.actions.SpeakAction;
import game.actions.TradeAction;

import java.util.Random;

/**
 * A friendly NPC
 */
public class Toad extends Actor implements SpeechCapable {
    private boolean otherPlayerPower = false;
    private boolean otherPlayerWrench = false;
    private int age = 1;

    /**
     * Constructor
     */
    public Toad() {
        super("Toad", 'O', 500);
        this.addItemToInventory(new PowerStar());
        this.addItemToInventory(new SuperMushroom());
        this.addItemToInventory(new Wrench());
    }

    @Override
    public ActionList allowableActions(Actor otherActor, String direction, GameMap map) {
        ActionList actions = new ActionList();
        if (otherActor.hasCapability(Status.CAN_TRADE)){
            for(Item item: this.getInventory()) {
                actions.add(new TradeAction(item,this));
            }
        }
        if (otherActor.hasCapability(Status.CAN_SPEAK)){
            actions.add(new SpeakAction(this));

        }

        if (otherActor.hasCapability(Status.STAR)){
            this.otherPlayerPower = true;
        }
        if (otherActor.getWeapon().toString().equals("Wrench")){
            this.otherPlayerWrench = true;
        }
        return actions;
    }


    @Override
    public Action playTurn(ActionList actions, Action lastAction, GameMap map, Display display) {
        if (this.age % 2 == 0){
            System.out.println("Toad: \"" + this.speak() + "\"");
        }
        age ++;
        return new DoNothingAction();
    }

    @Override
    public String speak() {
        Random rand = new Random();
        String line;
        int randValue = 0;
        if (this.otherPlayerPower && this.otherPlayerWrench) {
            while (randValue <= 1) {
                randValue = rand.nextInt(4);
            }
        } else if (this.otherPlayerPower) {
            randValue = 1;
            while (randValue == 1) {
                randValue = rand.nextInt(4);
            }
        } else if (this.otherPlayerWrench) {
            while (randValue == 0) {
                randValue = rand.nextInt(4);
            }
        } else {
            randValue = rand.nextInt(4);
        }


        if (randValue == 0) {
            line = "You might need a wrench to smash Koopa's hard shells.";
        } else if (randValue == 1) {
            line = "You better get back to finding the Power Stars.";
        } else if (randValue == 2) {
            line = "The Princess is depending on you! You are our only hope.";
        } else {
            line = "Being imprisoned in these walls can drive a fungus crazy";
        }
        return line;
    }
}
