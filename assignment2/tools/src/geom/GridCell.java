package geom;

/**
 * Represents a cell within the grid.
 * 
 * @author lackofcheese
 * 
 */
public class GridCell {
	/** The row index of the cell. */
	private int row;
	/** The column index of the cell. */
	private int col;

	/**
	 * Constructs a grid cell from its row and column indices.
	 * 
	 * @param row
	 *            the row index of the cell.
	 * @param col
	 *            the column index of the cell.
	 */
	public GridCell(int row, int col) {
		this.row = row;
		this.col = col;
	}

	/**
	 * Returns the row index of the cell.
	 * 
	 * @return the row index of the cell.
	 */
	public int getRow() {
		return row;
	}

	/**
	 * Returns the column index of the cell.
	 * 
	 * @return the column index of the cell.
	 */
	public int getCol() {
		return col;
	}

	@Override
	public boolean equals(Object o) {
		if (!(o instanceof GridCell)) {
			return false;
		}
		GridCell other = (GridCell) o;
		return this.row == other.row && this.col == other.col;
	}

	@Override
	public int hashCode() {
		return row * 3571 + col;
	}

	@Override
	public String toString() {
		return row + " " + col;
	}
}
