package divergence;

import java.io.IOException;

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
public class TargetDivergence extends DivergenceFromFile {
	/** The discrete grid over which the target moves. */
	private TargetGrid grid;

	/**
	 * Creates a divergence with the given distribution.
	 * 
	 * @param grid
	 *            the grid over which the target moves.
	 * @param filename
	 *            the file to load the distribution from.
	 * @throws IOException
	 *             if there is an error loading the distribution file.
	 */
	public TargetDivergence(TargetGrid grid, String filename)
			throws IOException {
		super(filename);
		this.grid = grid;
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

		// Apply the divergence, as per the encoded distribution.
		int desiredCode = grid.encodeFromIndices(startIndex, desiredIndex);
		int divergedCode = divergeCode(desiredCode);
		GridCell endIndex = grid.decodeFromIndices(startIndex, divergedCode);
		return new Action(currentState, grid.getCentre(endIndex));
	}
}
