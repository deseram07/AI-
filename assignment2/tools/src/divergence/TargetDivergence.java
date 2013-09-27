package divergence;

import java.util.Arrays;

import game.Action;
import game.AgentState;
import geom.GridCell;
import geom.TargetGrid;

/**
 * Represents the divergence in the actions of a target.
 * 
 * @author lackofcheese
 * 
 */
public class TargetDivergence extends ActionDivergence {
	/** The discrete grid over which the target moves. */
	private TargetGrid grid;
	/** The probability of each offset value. */
	private double[] chances;

	/** The angular error offsets (as multiples of PI/4) */
	private static final int[] OFFSETS = new int[] { 0, 1, -1, 2, -2, 3, -3, 4 };
	/**
	 * The chance associated with each offset; the last value is left out since
	 * the chances must add up to 1.
	 */
	private static final double[] DEFAULT_CHANCES = new double[] { 0.5, 0.2,
			0.1, 0.08, 0.03, 0.05, 0.02, 0.01 };

	/**
	 * Creates a divergence with the default distribution.
	 * 
	 * @param grid
	 *            the grid over which the target moves.
	 */
	public TargetDivergence(TargetGrid grid) {
		this(grid, DEFAULT_CHANCES);
	}

	/**
	 * Creates a divergence with the given distribution.
	 * 
	 * @param grid
	 *            the grid over which the target moves.
	 * @param chances
	 *            the distribution over the offsets.
	 */
	public TargetDivergence(TargetGrid grid, double[] chances) {
		this.grid = grid;
		this.chances = Arrays.copyOf(chances, 8);
	}

	/**
	 * Returns a random offset as per the distribution (offsets/chances).
	 * 
	 * @return a random offset as per the distribution (offsets/chances).
	 */
	private double randomOffset() {
		double r = random.nextDouble();

		double total = 0;
		int index = 0;
		for (; index < chances.length; index++) {
			total += chances[index];
			if (r <= total) {
				break;
			}
		}
		if (index >= chances.length) {
			index = chances.length - 1;
		}
		return OFFSETS[index] * Math.PI / 4;
	}

	@Override
	public Action divergeAction(Action action) {
		AgentState currentState = action.getStartState();
		AgentState desiredState = action.getResultingState();
		GridCell startIndex = grid.getCell(currentState.getPosition());
		GridCell desiredIndex = grid.getCell(desiredState.getPosition());
		if (desiredIndex.equals(startIndex)) {
			return new Action(currentState); // No error when standing still.
		}

		// Otherwise, we add a random offset to the heading, and return this
		// action.
		int actionCode = grid.encodeFromIndices(startIndex, desiredIndex);
		double heading = grid.getHeading(actionCode);
		double newHeading = heading + randomOffset();
		int newActionCode = grid.getCodeFromHeading(newHeading);
		GridCell endIndex = grid.decodeFromIndices(startIndex, newActionCode);
		return new Action(currentState, grid.getCentre(endIndex));
	}
}
