package divergence;

import java.util.Random;

import game.Action;

/**
 * Diverges an action.
 * 
 * @author lackofcheese
 * 
 */
public abstract class ActionDivergence {
	/** The source of randomness. */
	protected Random random;

	/**
	 * Constructs an action divergence.
	 */
	public ActionDivergence() {
		random = new Random();
	}

	/**
	 * Sets the seed of the randomizer to the given value.
	 * 
	 * @param seed
	 *            the new seed value.
	 */
	public void setSeed(long seed) {
		random.setSeed(seed);
	}

	/**
	 * Returns a diverged action.
	 * 
	 * @param action
	 *            the action to modify.
	 * @return a diverged action.
	 */
	public abstract Action divergeAction(Action action);
}
