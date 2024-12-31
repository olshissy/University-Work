package game.items;

import java.util.ArrayList;

/**
 * Represents the inventory that is available for trading
 */
public class ItemTradingInventory {
    private ArrayList<TradeableItem> itemsToTrade = new ArrayList<>();
    private static ItemTradingInventory instance;

    /**
     * Singleton instance of the ItemTradingInventory
     * @return the instance
     */
    public static ItemTradingInventory getInstance(){
        if(instance == null){
            instance = new ItemTradingInventory();
        }
        return instance;
    }

    /**
     * @return the item trading inventory list
     */
    public ArrayList<TradeableItem> getItemsToTrade(){return itemsToTrade;}

    /**
     * Add an item to the trading inventory
     * @param item the item to add
     */
    public void addItem(TradeableItem item){
        itemsToTrade.add(item);
    }
}
