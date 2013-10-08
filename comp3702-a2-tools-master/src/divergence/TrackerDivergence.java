package divergence;

import java.io.IOException;

import game.Action;
import game.TrackerAction;
import geom.GridCell;
import geom.TrackerGrid;
import geom.Vector2D;

/**
 * Represents the divergence in the actions of a tracker.
 * 
 * @author lackofcheese
 * 
 */
public class TrackerDivergence extends DivergenceFromFile {
	/** The discrete grid over which the tracker moves. */
	private TrackerGrid grid;

	/**
	 * Creates a tracker divergence with the given distribution.
	 * 
	 * @param stepDistance
	 *            the amount this tracker moves per turn.
	 * @param filename
	 *            the file to load the distribution from.
	 * @throws IOException
	 *             if there is an error loading the distribution file.
	 */
	public TrackerDivergence(double stepDistance, String filename)
			throws IOException {
		super(filename);
		this.grid = new TrackerGrid(stepDistance / 2);
	}

	@Override
	public TrackerAction divergeAction(Action action) {
		TrackerAction trackerAction = (TrackerAction) action;
		if (!trackerAction.isMovement() || trackerAction.getDistance() == 0) {
			return trackerAction;
		}

		int desiredCode = grid.encodeAction(trackerAction);
		int divergedCode = divergeCode(desiredCode);
		GridCell newCell = grid.decodeToCell(divergedCode);
		Vector2D actualDisplacement = grid.getRandomPoint(newCell, random);

		return new TrackerAction(trackerAction.getStartState(),
				actualDisplacement.getDirection(),
				actualDisplacement.getMagnitude());
	}
}
