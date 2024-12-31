package game.items;

/**
 * Represents an item that can be traded
 */
public interface TradeableItem {
    /**
     * Gets the price of the item
     * @return the price of the item
     */
    int getPrice();

    /**
     * Adds the item to the instance of the trading inventory
     */
    default void addItemToInventory(){
        ItemTradingInventory.getInstance().addItem(this);
    }

}
