package divergence;

import game.Action;
import game.AgentState;
import game.TrackerAction;
import geom.GridCell;
import geom.TrackerGrid;
import geom.Vector2D;

/**
 * Implements divergence for the tracker movements.
 * 
 * @author lackofcheese
 * 
 */
public class TrackerDivergence extends ActionDivergence {
	/** The allowed distance value. */
	private double stepDistance;

	/** The grid associated with this tracker. */
	private TrackerGrid trackerGrid;

	/** The distribution for a two-square move. */
	private double[][] chances20;

	/** The distribution for a knight-type move. */
	private double[][] chances21;

	/** The distribution for a diagonal move. */
	private double[][] chances11;

	/** The default distribution for a two-square move. */
	private static final double[][] DEFAULT_CHANCES_20 = new double[][] {
			{ 0.005, 0.005, 0.005, 0.005, 0.005 },
			{ 0.005, 0.005, 0.005, 0.005, 0.005 },
			{ 0.005, 0.010, 0.020, 0.010, 0.005 },
			{ 0.010, 0.020, 0.050, 0.020, 0.010 },
			{ 0.010, 0.085, 0.600, 0.085, 0.010 },

	};

	/** The default distribution for a knight-type move. */
	private static final double[][] DEFAULT_CHANCES_21 = new double[][] {
			{ 0.005, 0.005, 0.005, 0.005, 0.005 },
			{ 0.005, 0.005, 0.005, 0.020, 0.005 },
			{ 0.005, 0.005, 0.020, 0.050, 0.020 },
			{ 0.005, 0.005, 0.020, 0.080, 0.050 },
			{ 0.005, 0.020, 0.100, 0.500, 0.050 },

	};

	/** The default distribution for a diagonal move. */
	private static final double[][] DEFAULT_CHANCES_11 = new double[][] {
			{ 0.005, 0.005, 0.005, 0.005, 0.005 },
			{ 0.005, 0.005, 0.005, 0.020, 0.005 },
			{ 0.005, 0.005, 0.020, 0.050, 0.020 },
			{ 0.005, 0.005, 0.050, 0.625, 0.050 },
			{ 0.005, 0.005, 0.020, 0.050, 0.020 },

	};

	/**
	 * Returns a random cell index from the given distribution.
	 * 
	 * @param distribution
	 *            the distributon to use.
	 * @return a random cell index from the given distribution.
	 */
	private GridCell fromDistribution(double[][] distribution) {
		double r = random.nextDouble();
		double total = 0;
		for (int row = -2; row <= 2; row++) {
			for (int col = -2; col <= 2; col++) {
				double p = distribution[row + 2][col + 2];
				total += p;
				if (r <= total) {
					// System.out.println("p = " + p);
					return new GridCell(row, col);
				}
			}
		}
		// System.out.println("!!!! " + total);
		return new GridCell(2, 2);
	}

	/**
	 * Returns a diverged version of the given tracker movements.
	 * 
	 * @param targetCell
	 *            the
	 * @return
	 */
	private GridCell divergeCell(GridCell targetCell) {
		boolean invertRow = false;
		boolean invertCol = false;
		boolean transpose = false;
		int row = targetCell.getRow();
		int col = targetCell.getCol();
		if (row < 0) {
			row = -row;
			invertRow = true;
		}
		if (col < 0) {
			col = -col;
			invertCol = true;
		}
		if (col > row) {
			int temp = row;
			row = col;
			col = temp;
			transpose = true;
		}
		GridCell divergedCell;
		if (row == 2 && col == 0) {
			// System.out.println("Type 20");
			divergedCell = fromDistribution(chances20);
		} else if (row == 2 && col == 1) {
			// System.out.println("Type 21");
			divergedCell = fromDistribution(chances21);
		} else if (row == 1 && col == 1) {
			// System.out.println("Type 11");
			divergedCell = fromDistribution(chances11);
		} else {
			throw new RuntimeException("Invalid divergence!?");
		}

		row = divergedCell.getRow();
		col = divergedCell.getCol();
		// System.out.println("T: " + row + " " + col);
		if (transpose) {
			int temp = row;
			row = col;
			col = temp;
		}
		if (invertCol) {
			col = -col;
		}
		if (invertRow) {
			row = -row;
		}
		return new GridCell(row, col);
	}

	/**
	 * Constructs a TrackerDivergence with the given standard distance to
	 * travel, and the default distributions.
	 * 
	 * @param stepDistance
	 *            the standard move distance.
	 */
	public TrackerDivergence(double stepDistance) {
		this(stepDistance, DEFAULT_CHANCES_20, DEFAULT_CHANCES_21,
				DEFAULT_CHANCES_11);
	}

	/**
	 * Constructs a ZeroDivergence with the given standard distance to travel,
	 * and the given distribtuons.
	 * 
	 * @param stepDistance
	 *            the standard move distance.
	 * @param chances02
	 *            the distribution for orthogonal two-square moves.
	 * @param chances12
	 *            the distribution for knight-type moves.
	 * @param chances11
	 *            the distribution for diagonal moves.
	 */
	public TrackerDivergence(double stepDistance, double[][] chances20,
			double[][] chances21, double[][] chances11) {
		this.stepDistance = stepDistance;
		this.chances20 = chances20;
		this.chances21 = chances21;
		this.chances11 = chances11;
		this.trackerGrid = new TrackerGrid(stepDistance / 2);
	}

	@Override
	public TrackerAction divergeAction(Action action) {
		TrackerAction trackerAction = (TrackerAction) action;
		if (!trackerAction.isMovement() || trackerAction.getDistance() == 0) {
			return trackerAction;
		}

		AgentState startState = trackerAction.getStartState();
		Vector2D desiredDisplacement = new Vector2D(stepDistance,
				trackerAction.getHeading());
		GridCell targetCell = trackerGrid.getCell(desiredDisplacement);

		// System.out.println("Desired: " + trackerAction.getHeading());
		// System.out.println("Desired: " + targetCell.getRow() + " " +
		// targetCell.getCol());
		// System.out.println("Desired: " + desiredDisplacement);

		GridCell newCell = divergeCell(targetCell);
		Vector2D actualDisplacement = trackerGrid.getRandomPoint(newCell,
				random);

		// System.out.println("Actual: " + newCell.getRow() + " " +
		// newCell.getCol());
		// System.out.println("Actual: " + actualDisplacement);

		return new TrackerAction(startState, actualDisplacement.getDirection(),
				actualDisplacement.getMagnitude());
	}
}
