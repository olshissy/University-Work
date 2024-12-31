package game.actions;

import edu.monash.fit2099.engine.actions.Action;
import edu.monash.fit2099.engine.actors.Actor;
import edu.monash.fit2099.engine.items.Item;
import edu.monash.fit2099.engine.positions.GameMap;
import game.items.ItemTradingInventory;
import game.items.TradeableItem;
import game.Wallet;

import java.util.ArrayList;

/**
 * A special action for trading items
 */
public class TradeAction extends Action {
    private int price;
    private Item item;
    private Actor NPC;

    /**
     * COnstructor
     * @param item the item to be traded
     * @param NPC the actor to be trading the items
     */
    public TradeAction(Item item, Actor NPC) {
        this.item = item;
        this.NPC = NPC;
        ArrayList<TradeableItem> tradeInventory = ItemTradingInventory.getInstance().getItemsToTrade();
        this.price = tradeInventory.get(tradeInventory.indexOf(item)).getPrice();

    }

    @Override
    public String execute(Actor actor, GameMap map) {
        int walletValue = Wallet.getInstance().getValue();
        if(walletValue >= price){
            Wallet.getInstance().decreaseWalletValue(price);
            NPC.removeItemFromInventory(item);
            actor.addItemToInventory(item);
        }
        else{
            return "You don't have enough coins!";
        }
        return String.format("Mario buys %s for %d", item.toString(), price);
    }

    @Override
    public String menuDescription(Actor actor) {
        return String.format("Mario buys %s ($%d)", item.toString(), price);
    }


}
