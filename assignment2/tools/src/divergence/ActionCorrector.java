package divergence;

import game.Action;
import game.SensingParameters;
import game.TrackerAction;

/**
 * Corrects actions, in order to fix actions that move by the wrong distance, or
 * use invalid camera arm lengths.
 * 
 * @author lackofcheese
 * 
 */
public class ActionCorrector extends ActionDivergence {
	/** The allowed distance value. */
	private double stepDistance;
	/** The tracker's sensing parameters */
	private SensingParameters sp;

	/**
	 * Constructs an ActionCorrector with the given standard distance to travel.
	 * 
	 * @param stepDistance
	 *            the standard move distance.
	 * @param sp
	 *            the sensing parameters of the tracker.
	 */
	public ActionCorrector(double stepDistance, SensingParameters sp) {
		this.stepDistance = stepDistance;
	}

	@Override
	public TrackerAction divergeAction(Action action) {
		TrackerAction trackerAction = (TrackerAction) action;
		double distance = trackerAction.getDistance();
		if (trackerAction.isCameraAdjustment()) {
			double armLength = trackerAction.getResultingState()
					.getCameraArmLength();
			if (armLength < sp.getMinLength()) {
				return new TrackerAction(trackerAction.getStartState(),
						sp.getMinLength());
			} else if (armLength > sp.getMaxLength()) {
				return new TrackerAction(trackerAction.getStartState(),
						sp.getMaxLength());
			}
		}

		if (!trackerAction.isMovement() || distance == 0
				|| distance == stepDistance) {
			return trackerAction;
		}
		// Fix the distance to to its correct value.
		return new TrackerAction(trackerAction.getStartState(),
				trackerAction.getHeading(), stepDistance);
	}
}
