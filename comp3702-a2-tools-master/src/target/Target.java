package target;

import game.Action;
import game.ActionResult;
import game.Agent;
import game.Percept;

import java.util.List;

/**
 * Represents a simple target with deterministic motion - not used in A2.
 * 
 * @author lackofcheese
 * 
 */
public class Target implements Agent {
	/** The policy of this target. */
	private TargetPolicy policy;

	/**
	 * Constructs a deterministic target with the given policy.
	 * 
	 * @param policy
	 *            the policy to use.
	 */
	public Target(TargetPolicy policy) {
		this.policy = policy;
	}

	@Override
	public Action getAction(int turnNo, ActionResult previousResult,
			double[] scores, List<Percept> newPercepts) {
		return policy.getAction(previousResult.getResultingState());
	}

	/**
	 * Returns the policy used by this target.
	 * 
	 * @return the policy used by this target.
	 */
	public TargetPolicy getPolicy() {
		return policy;
	}
}
