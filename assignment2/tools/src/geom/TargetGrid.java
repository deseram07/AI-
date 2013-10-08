package geom;

import game.Action;

import java.awt.geom.Point2D;

/**
 * Represents a square grid over the workspace.
 * 
 * @author lackofcheese
 * 
 */
public class TargetGrid implements ActionEncoder {
	/** The number of rows and columns. */
	private int gridSize;

	/**
	 * Constructs a square grid with the given number of rows and columns.
	 * 
	 * @param gridSize
	 *            the number of rows and columns.
	 */
	public TargetGrid(int gridSize) {
		this.gridSize = gridSize;
	}

	/**
	 * Returns the number of rows and columns in the grid.
	 * 
	 * @return the number of rows and columns in the grid.
	 */
	public int getGridSize() {
		return gridSize;
	}

	/**
	 * Returns the action code corresponding to a movement between the given
	 * cells.
	 * 
	 * @param start
	 *            the start cell.
	 * @param end
	 *            the end cell.
	 * @return the action code for a movement from the start cell to the end
	 *         cell.
	 */
	public int encodeFromIndices(GridCell start, GridCell end) {
		int rowDelta = end.getRow() - start.getRow();
		int colDelta = end.getCol() - start.getCol();
		return rowDelta * 3 + colDelta + 4;
	}

	/**
	 * Returns the end cell resulting from taking the action with the given
	 * action code from the starting cell.
	 * 
	 * @param start
	 *            the start cell.
	 * @param actionCode
	 *            the action to take.
	 * @return the end cell after taking the given action from the start cell.
	 */
	public GridCell decodeFromIndices(GridCell start, int actionCode) {
		return new GridCell(start.getRow() + actionCode / 3 - 1, start.getCol()
				+ actionCode % 3 - 1);
	}

	/**
	 * Returns the heading corresponding to the given action.
	 * 
	 * @param actionCode
	 *            the action.
	 * @return the heading corresponding to the given action.
	 */
	public double getHeading(int actionCode) {
		switch (actionCode) {
		case 0:
			return 3 * Math.PI / 4;
		case 1:
			return Math.PI / 2;
		case 2:
			return Math.PI / 4;
		case 3:
			return Math.PI;
		case 4:
		case 5:
			return 0;
		case 6:
			return -3 * Math.PI / 4;
		case 7:
			return -Math.PI / 2;
		case 8:
			return -Math.PI / 4;
		default:
			return 0;
		}
	}

	/**
	 * Returns the action closest to the given heading.
	 * 
	 * @param heading
	 *            the heading to take.
	 * @return the action closest to the given heading.
	 */
	public int getCodeFromHeading(double heading) {
		int numEighths = (int) Math.round(heading * 4 / Math.PI);
		numEighths %= 8;
		if (numEighths <= -4) {
			numEighths += 8;
		} else if (numEighths > 4) {
			numEighths -= 8;
		}
		switch (numEighths) {
		case -3:
			return 6;
		case -2:
			return 7;
		case -1:
			return 8;
		case 0:
			return 5;
		case 1:
			return 2;
		case 2:
			return 1;
		case 3:
			return 0;
		case 4:
			return 3;
		default:
			return 0;
		}
	}

	/**
	 * Returns the grid cell containing the given point.
	 * 
	 * @param pos
	 *            the point to locate.
	 * @return the grid cell containing the given point.
	 */
	public GridCell getCell(Point2D pos) {
		int row = (int) ((1 - pos.getY()) * gridSize);
		int col = (int) (pos.getX() * gridSize);
		return new GridCell(row, col);
	}

	/**
	 * Returns the centre point of the given cell.
	 * 
	 * @param cell
	 *            the cell.
	 * @return the centre point of the given cell.
	 */
	public Point2D getCentre(GridCell cell) {
		return new Point2D.Double(0 + (cell.getCol() + 0.5) / gridSize, 1
				- (cell.getRow() + 0.5) / gridSize);
	}

	/**
	 * Returns the action code corresponding to the given action.
	 * 
	 * @param a
	 *            the action to encode.
	 * @return the action code corresponding to the given action.
	 */
	public int encodeAction(Action a) {
		GridCell startCell = getCell(a.getStartState().getPosition());
		GridCell endCell = getCell(a.getResultingState().getPosition());
		return encodeFromIndices(startCell, endCell);
	}
}