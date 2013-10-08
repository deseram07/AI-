package game;

import geom.GeomTools;
import geom.TrackerGrid;

import java.awt.geom.Line2D;
import java.awt.geom.Point2D;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.InputMismatchException;
import java.util.List;
import java.util.NoSuchElementException;
import java.util.Random;
import java.util.Scanner;
import java.util.Stack;

import divergence.ActionDivergence;
import divergence.MotionHistory;
import divergence.TargetDivergence;
import divergence.TrackerDivergence;
import divergence.ActionCorrector;
import divergence.ZeroDivergence;
import target.Target;
import target.TargetPolicy;
import tracker.Tracker;

/**
 * This class runs the "Game of Spy" for assignment 2. It contains a structured
 * representation of the specifications for a given game setup, and also
 * contains the code that executes the game loop.
 * 
 * @author lackofcheese
 */
public class GameRunner {
	/** The default file to load the game setup from. */
	private static final String DEFAULT_SETUP_FILE = "setup.txt";
	/** The default file to output the game sequence to. */
	private static final String DEFAULT_OUTPUT_FILE = "output.txt";
	/** The default file for the target's divergence distribution. */
	private static final String DEFAULT_TARGET_FILE = "prob-target.txt";
	/** The default file for the tracker's divergence distribution. */
	private static final String DEFAULT_TRACKER_FILE = "prob-tracker.txt";
	/** The file containing the target's divergence distribution. */
	private String targetDistributionFile = DEFAULT_TARGET_FILE;
	/** The file containing the tracker's divergence distribution. */
	private String trackerDistributionFile = DEFAULT_TRACKER_FILE;

	/**
	 * Sets the distribution file for the target's divergence.
	 * 
	 * @param newPath
	 *            the new path.
	 */
	public void setTargetDistribution(String newPath) {
		targetDistributionFile = newPath;
	}

	/**
	 * Sets the distribution file for the tracker's divergence.
	 * 
	 * @param newPath
	 *            the new path.
	 */
	public void setTrackerDistribution(String newPath) {
		trackerDistributionFile = newPath;
	}

	private double MAX_SIGHT_DISTANCE_ERROR = 1e-5;
	private int NUM_CAMERA_ARM_STEPS = 1000;

	/** The source of randomness. */
	private Random random;

	/**
	 * Cosntructs a new GameRunner.
	 */
	public GameRunner() {
		random = new Random();
	}

	/**
	 * Sets the seed for randomization within this GameRunner.
	 * 
	 * @param seed
	 *            the seed for the randomizer.
	 */
	public void setSeed(long seed) {
		random.setSeed(seed);
	}

	/** Runtime motion history of the tracker. */
	private MotionHistory runtimeTrackerMotionHistory;
	/** Runtime motion history of the target. */
	private MotionHistory runtimeTargetMotionHistory;

	/* ------------------------ SETUP PARAMETERS -------------------------- */

	/** True iff a game setup is currently loaded */
	private boolean setupLoaded = false;

	/** The number of targets in the game. */
	private int numTargets;
	/** The (shared) policy of target(s) in the game. */
	private TargetPolicy targetPolicy;
	/** The motion history of the target(s), or null if no such history exists. */
	private MotionHistory targetMotionHistory = null;
	/** The sensing parameters of the target(s). */
	private SensingParameters targetSensingParams;
	/** The initial state(s) of the target(s). */
	private List<AgentState> targetInitialStates;

	/**
	 * The motion history of the tracker, or null if the tracker's motion is
	 * deterministic.
	 */
	private MotionHistory trackerMotionHistory = null;
	/** The sensing parameters of the tracker. */
	private SensingParameters trackerSensingParams;
	/** The initial state of the tracker. */
	private AgentState trackerInitialState;
	/** The distance the tracker can move in one step. */
	private double trackerMoveDistance;

	/** The obstacles in the game space. */
	private List<RectRegion> obstacles;
	/** The goal region for the target(s). */
	private RectRegion goalRegion;

	/**
	 * The obstacles in the game space, in addition to extra obstacles
	 * representing the workspace boundaries.
	 */
	private List<RectRegion> extendedObstacles;

	/**
	 * Loads the problem setup from a text file.
	 * 
	 * @param filename
	 *            the path of the text file to load.
	 * @throws IOException
	 *             if the text file doesn't exist or doesn't meet the assignment
	 *             specifications.
	 */
	public void loadSetup(String filename) throws IOException {
		Path baseFolder = Paths.get(filename).toAbsolutePath().getParent();
		setupLoaded = false;
		BufferedReader input = new BufferedReader(new FileReader(filename));
		String line;
		int lineNo = 0;
		Scanner s;
		try {
			line = input.readLine();
			lineNo++;
			s = new Scanner(line);
			numTargets = s.nextInt();
			s.close();

			line = input.readLine();
			lineNo++;
			s = new Scanner(line);
			boolean hasTargetHistory = (s.next().equals("A2"));
			s.close();

			line = input.readLine();
			lineNo++;
			s = new Scanner(line);
			String policyPath = baseFolder.resolve(s.next()).toString();
			targetPolicy = new TargetPolicy(policyPath);
			trackerMoveDistance = 1.0 / targetPolicy.getGridSize();
			if (hasTargetHistory) {
				String targetHistoryPath = baseFolder.resolve(s.next())
						.toString();
				targetMotionHistory = new MotionHistory(targetHistoryPath);
			}
			s.close();

			line = input.readLine();
			lineNo++;
			targetSensingParams = new SensingParameters(false, line);

			line = input.readLine();
			lineNo++;
			s = new Scanner(line);
			boolean hasTrackerHistory = (s.next().equals("B2"));
			s.close();

			line = input.readLine();
			lineNo++;
			String trackerHistoryPath = null;
			if (hasTrackerHistory) {
				s = new Scanner(line);
				trackerHistoryPath = baseFolder.resolve(s.next()).toString();
				s.close();
			}

			line = input.readLine();
			lineNo++;
			s = new Scanner(line);
			boolean hasCamera = (s.next().equals("C2"));
			s.close();

			if (hasTrackerHistory) {
				trackerMotionHistory = new MotionHistory(trackerHistoryPath);
			}

			line = input.readLine();
			lineNo++;
			trackerSensingParams = new SensingParameters(hasCamera, line);

			line = input.readLine();
			lineNo++;
			trackerInitialState = new AgentState(hasCamera, line);

			targetInitialStates = new ArrayList<AgentState>();
			for (int i = 0; i < numTargets; i++) {
				line = input.readLine();
				lineNo++;
				targetInitialStates.add(new AgentState(false, line));
			}

			line = input.readLine();
			lineNo++;
			goalRegion = new RectRegion(line);

			line = input.readLine();
			lineNo++;
			s = new Scanner(line);
			int numObstacles = s.nextInt();
			s.close();

			obstacles = new ArrayList<RectRegion>();
			for (int i = 0; i < numObstacles; i++) {
				line = input.readLine();
				lineNo++;
				obstacles.add(new RectRegion(line));
			}

			extendedObstacles = new ArrayList<RectRegion>(obstacles);
			extendedObstacles.add(new RectRegion(-1, -1, 1, 3));
			extendedObstacles.add(new RectRegion(-1, -1, 3, 1));
			extendedObstacles.add(new RectRegion(-1, 1, 3, 1));
			extendedObstacles.add(new RectRegion(1, -1, 1, 3));

			setupLoaded = true;
			runtimeTrackerMotionHistory = new MotionHistory();
			runtimeTargetMotionHistory = new MotionHistory();
		} catch (InputMismatchException e) {
			throw new IOException(String.format(
					"Invalid number format on line %d of %s: %s", lineNo,
					filename, e.getMessage()));
		} catch (NoSuchElementException e) {
			throw new IOException(String.format(
					"Not enough tokens on line %d of %s", lineNo, filename));
		} catch (NullPointerException e) {
			throw new IOException(String.format(
					"Line %d expected, but file %s ended.", lineNo, filename));
		} finally {
			input.close();
		}
	}

	/**
	 * Returns whether a setup is currently loaded.
	 * 
	 * @return whether a setup is currently loaded.
	 */
	public boolean setupLoaded() {
		return setupLoaded;
	}

	/**
	 * Returns the number of targets.
	 * 
	 * @return the number of targets.
	 */
	public int getNumTargets() {
		return numTargets;
	}

	/**
	 * Returns the policy of the target.
	 * 
	 * @return the policy of the target.
	 */
	public TargetPolicy getTargetPolicy() {
		return targetPolicy;
	}

	/**
	 * Returns the motion history of the target(s), or null if no motion history
	 * is available.
	 * 
	 * @return the motion history of the target(s), or null if no motion history
	 *         is available.
	 */
	public MotionHistory getTargetMotionHistory() {
		return targetMotionHistory;
	}

	/**
	 * Returns the sensing parameters of the target.
	 * 
	 * @return the sensing parameters of the target.
	 */
	public SensingParameters getTargetSensingParams() {
		return targetSensingParams;
	}

	/**
	 * Returns the initial state(s) of the target(s).
	 * 
	 * @return the initial state(s) of the target(s).
	 */
	public List<AgentState> getTargetInitialStates() {
		return targetInitialStates;
	}

	/**
	 * Returns the motion history of the tracker, or null if no motion history
	 * is available.
	 * 
	 * @return the motion history of the tracker, or null if no motion history
	 *         is available.
	 */
	public MotionHistory getTrackerMotionHistory() {
		return trackerMotionHistory;
	}

	/**
	 * Returns the sensing parameters of the tracker.
	 * 
	 * @return the sensing parameters of the tracker.
	 */
	public SensingParameters getTrackerSensingParams() {
		return trackerSensingParams;
	}

	/**
	 * Returns the initial state of the tracker.
	 * 
	 * @return the initial state of the tracker.
	 */
	public AgentState getTrackerInitialState() {
		return trackerInitialState;
	}

	/**
	 * Returns the list of obstacles.
	 * 
	 * @return the list of obstacles.
	 */
	public List<RectRegion> getObstacles() {
		return obstacles;
	}

	/**
	 * Returns the goal region.
	 * 
	 * @return the goal region.
	 */
	public RectRegion getGoalRegion() {
		return goalRegion;
	}

	/* ------------------------ RUNNING THE GAME -------------------------- */

	public class GameState {
		/** True iff the game is already over in this state. */
		private boolean gameComplete;
		/** The turn number of this game. */
		private int turnNo;
		/** True iff it's the tracker's turn to act. */
		private boolean isTrackerTurn;

		/** The players in the game. */
		private Agent[] players;
		/** The divergences for the players' actions. */
		private ActionDivergence[] playerDivs;
		/** The scores of the players. */
		private double[] playerScores;
		/** The states of the players. */
		private AgentState[] playerStates;

		/** The percepts acquired since the last tracker turn. */
		List<Percept> trackerPercepts;

		/**
		 * Constructs a game state representing the initial state of the game
		 * (i.e. just before the 0-th action).
		 */
		public GameState() {
			gameComplete = false;
			turnNo = 0;
			isTrackerTurn = true;
			trackerPercepts = new ArrayList<Percept>();

			players = new Agent[numTargets + 1];
			playerDivs = new ActionDivergence[numTargets + 1];
			playerScores = new double[numTargets + 1];
			playerStates = new AgentState[numTargets + 1];
			for (int i = 1; i <= numTargets; i++) {
				players[i] = new Target(targetPolicy);
				long seed = random.nextLong();
				// System.out.println(String.format("Tracker #%d seed: %d", i,
				// seed));
				try {
					playerDivs[i] = new TargetDivergence(
							targetPolicy.getGrid(), targetDistributionFile);
				} catch (IOException e) {
					e.printStackTrace();
				}
				playerDivs[i].setSeed(seed);
				playerScores[i] = 0;
				playerStates[i] = targetInitialStates.get(i - 1);
			}
			if (trackerMotionHistory == null) {
				playerDivs[0] = new ZeroDivergence();
			} else {
				long seed = random.nextLong();
				// System.out.println(String.format("Target seed: %d", seed));
				try {
					playerDivs[0] = new TrackerDivergence(trackerMoveDistance,
							trackerDistributionFile);
				} catch (IOException e) {
					e.printStackTrace();
				}
				playerDivs[0].setSeed(seed);
			}
			playerScores[0] = 0;
			playerStates[0] = trackerInitialState;

			List<AgentState> targetInitialStatesCopy = new ArrayList<AgentState>();
			for (AgentState as : targetInitialStates) {
				targetInitialStatesCopy.add(new AgentState(as));
			}
			List<RectRegion> obstaclesCopy = new ArrayList<RectRegion>();
			for (RectRegion obstacle : obstacles) {
				obstaclesCopy.add(new RectRegion(obstacle));
			}
			players[0] = new Tracker(numTargets,
					new TargetPolicy(targetPolicy), targetMotionHistory,
					new SensingParameters(targetSensingParams),
					targetInitialStatesCopy,

					trackerMotionHistory, new SensingParameters(
							trackerSensingParams), new AgentState(
							trackerInitialState),

					obstaclesCopy, new RectRegion(goalRegion));
		}

		/**
		 * Duplicates another game state.
		 * 
		 * @param other
		 *            the state to duplicate.
		 */
		public GameState(GameState other) {
			this.gameComplete = other.gameComplete;
			this.turnNo = other.turnNo;
			this.isTrackerTurn = other.isTrackerTurn;

			this.players = other.players;
			this.playerDivs = other.playerDivs;
			this.playerScores = Arrays.copyOf(other.playerScores,
					numTargets + 1);
			this.playerStates = Arrays.copyOf(other.playerStates,
					numTargets + 1);

			this.trackerPercepts = new ArrayList<Percept>(other.trackerPercepts);
		}

		/**
		 * Returns whether this state represents a completed game.
		 * 
		 * @return whether this state represents a completed game.
		 */
		public boolean isGameComplete() {
			return gameComplete;
		}

		/**
		 * Returns true iff it's the tracker's turn to act.
		 * 
		 * @return true iff it's the tracker's turn to act.
		 */
		public boolean isTrackerTurn() {
			return isTrackerTurn;
		}

		/**
		 * Returns the scores of the players.
		 * 
		 * @return the scores of the players.
		 */
		public double[] getPlayerScores() {
			return Arrays.copyOf(playerScores, numTargets + 1);
		}

		/**
		 * Returns the score of the tracker.
		 * 
		 * @return the score of the tracker.
		 */
		public double getTrackerScore() {
			return playerScores[0];
		}

		/**
		 * Returns the total score of the target(s).
		 * 
		 * @return the total score of the target(s).
		 */
		public double getTargetScore() {
			double score = 0;
			for (int i = 1; i <= numTargets; i++) {
				score += playerScores[i];
			}
			return score;
		}

		/**
		 * Returns the score-state of the game, as an integer: +1 = tracker win
		 * / winning 0 = tracker draw / drawing -1 = tracker loss / losing
		 * 
		 * @return the score-state of the game.
		 */
		public int getResult() {
			double trackerScore = getTrackerScore();
			double targetScore = getTargetScore();
			if (trackerScore > targetScore) {
				return 1;
			} else if (trackerScore == targetScore) {
				return 0;
			} else {
				return -1;
			}
		}

		/**
		 * Returns the score-state of the game as a String.
		 * 
		 * @return the score-state of the game.
		 */
		public String getResultString() {
			int trackerScore = (int) getTrackerScore();
			int targetScore = (int) getTargetScore();
			String formatString = "Tracker %5s %d-%d";
			if (trackerScore > targetScore) {
				return String.format(formatString, (gameComplete ? "wins"
						: "winning"), trackerScore, targetScore);
			} else if (trackerScore == targetScore) {
				return String.format(formatString, (gameComplete ? "draws"
						: "drawing"), trackerScore, targetScore);
			} else {
				return String.format(formatString, (gameComplete ? "loses"
						: "losing"), trackerScore, targetScore);
			}
		}

		/**
		 * Returns the turn number of this game.
		 * 
		 * @return the turn number of this game.
		 */
		public int getTurnNo() {
			return turnNo;
		}

		/**
		 * Returns the states of the players.
		 * 
		 * @return the states of the players.
		 */
		public AgentState[] getPlayerStates() {
			return Arrays.copyOf(playerStates, numTargets + 1);
		}
	}

	/** The sequence of attempted actions with associated results */
	private Stack<ActionResult[]> actionResultSequence = new Stack<ActionResult[]>();
	/** The sequence of states of the game. */
	private Stack<GameState> stateSequence = new Stack<GameState>();
	/** The current state of the game. */
	private GameState cs = null;
	/** Corrects the actions of the tracker. */
	private ActionCorrector trackerActionCorrector;

	/** Returns true iff a game is active and complete. */
	public boolean gameComplete() {
		return cs != null && cs.gameComplete;
	}

	/**
	 * Returns the sequence of actions with associated results.
	 * 
	 * @return the sequence of actions with associated results.
	 */
	public Stack<ActionResult[]> getActionResultSequence() {
		return actionResultSequence;
	}

	/**
	 * Returns the sequence of game states.
	 * 
	 * @return the sequence of game states.
	 */
	public Stack<GameState> getStateSequence() {
		return stateSequence;
	}

	/**
	 * Returns the current turn number.
	 * 
	 * @return the current turn number.
	 */
	public int getTurnNo() {
		return cs.turnNo;
	}

	/**
	 * Reinitialises the game (i.e. goes to turn 0).
	 */
	public void initialise() {
		actionResultSequence.clear();
		stateSequence.clear();
		cs = new GameState();
		stateSequence.add(cs);
		trackerActionCorrector = new ActionCorrector(trackerMoveDistance,
				trackerSensingParams);
	}

	/**
	 * Undoes all moves after the given turn number.
	 * 
	 * @param desiredTurnNo
	 *            the turn number to revert to.
	 */
	public void undoTo(int desiredTurnNo) {
		if (desiredTurnNo >= cs.turnNo) {
			return;
		}

		int turnNo = cs.turnNo;
		while (turnNo > desiredTurnNo) {
			GameState state = stateSequence.pop();
			turnNo -= 1;
			if (state.isTrackerTurn()) {
				actionResultSequence.pop();
			} else {
				for (int i = 0; i < numTargets; i++) {
					actionResultSequence.pop();
				}
			}
		}
		cs = stateSequence.get(turnNo);
	}

	/**
	 * Runs the full game.
	 */
	public void runFull() {
		initialise();
		while (!gameComplete()) {
			simulateTurn();
		}
	}

	/**
	 * Simulates a single turn for a single player.
	 * 
	 * @param playerNo
	 *            the player to simulate a turn for.
	 */
	public ActionResult simulatePlayerTurn(int playerNo) {
		// Default result - information on preceding action not given.
		ActionResult previousResult = new ActionResult(null, null,
				new AgentState(cs.playerStates[playerNo]), 0);

		Action desiredAction;
		if (playerNo == 0) {
			// Retrieve the result of the previous tracker action, if present.
			int actionIndex = actionResultSequence.size() - 2;
			if (actionIndex >= 0) {
				previousResult = actionResultSequence.get(actionIndex)[0];
			}
			// Copy the game's scores to inform the tracker.
			double[] scores = Arrays.copyOf(cs.playerScores, numTargets + 1);
			desiredAction = cs.players[0].getAction(cs.turnNo, previousResult,
					scores, new ArrayList<Percept>(cs.trackerPercepts));
			cs.trackerPercepts.clear();
			// Correct the action to ensure values are within the correct
			// ranges.
			desiredAction = trackerActionCorrector.divergeAction(desiredAction);
		} else {
			desiredAction = cs.players[playerNo].getAction(cs.turnNo,
					previousResult, null, null);
		}

		// Diverge the action.
		Action divergedAction = cs.playerDivs[playerNo]
				.divergeAction(desiredAction);

		// Simulate the action.
		double reward = simulateAction(cs.turnNo, playerNo, divergedAction);
		cs.playerScores[playerNo] += reward;

		// If a target reached the goal, the game ends.
		if (playerNo != 0 && isWithinGoal(cs.playerStates[playerNo])) {
			cs.gameComplete = true;
		}
		return new ActionResult(desiredAction, divergedAction,
				cs.playerStates[playerNo], reward);
	}

	/**
	 * Simulates a single turn of the game.
	 */
	public void simulateTurn() {
		// Duplicate the state for modification.
		cs = new GameState(cs);
		if (cs.isTrackerTurn) {
			ActionResult result = simulatePlayerTurn(0);
			actionResultSequence.add(new ActionResult[] { result });
		} else {
			ActionResult[] results = new ActionResult[numTargets];
			for (int i = 1; i <= numTargets; i++) {
				results[i - 1] = simulatePlayerTurn(i);
			}
			actionResultSequence.add(results);
		}
		cs.turnNo += 1;
		cs.isTrackerTurn = !cs.isTrackerTurn;
		stateSequence.add(cs);
	}

	/**
	 * Simulates an action taken by a player; this consists of any movement and
	 * also testing for which other players can be seen.
	 * 
	 * @param turnNo
	 *            the turn number.
	 * @param playerNo
	 *            the acting player.
	 * @param action
	 *            the action taken.
	 * @return the reward for the action.
	 */
	public double simulateAction(int turnNo, int playerNo, Action action) {
		boolean isHQCall = false;
		double reward = 0;

		// Execute any movement or camera adjustment.
		if (action.isMovement()) {
			simulateMovement(turnNo, playerNo, action);
		} else if (action.isCameraAdjustment()) {
			simulateCameraAdjustment(turnNo, playerNo, action);
		}

		// Check whether this is an HQ call, and update the reward if so.
		if (playerNo == 0) {
			TrackerAction trackerAction = (TrackerAction) action;
			if (trackerAction.isHQCall()) {
				isHQCall = true;
				reward -= 5;
			}
		}

		// Check whether the tracker and target see each other.
		if (playerNo == 0) {
			// Evaluate the tracker's scoring.
			for (int otherNo = 1; otherNo <= numTargets; otherNo++) {
				boolean canSee = GeomTools.canSee(cs.playerStates[playerNo],
						cs.playerStates[otherNo], trackerSensingParams,
						obstacles, MAX_SIGHT_DISTANCE_ERROR,
						NUM_CAMERA_ARM_STEPS);
				if (canSee) {
					// Reward for seeing the target.
					reward += 1;
				}
				// If we saw the target or called HQ, we obtain a percept of the
				// target's state.
				if (canSee || isHQCall) {
					cs.trackerPercepts.add(new Percept(turnNo, otherNo,
							new AgentState(cs.playerStates[otherNo])));
				}
			}
		} else {
			// If the target sees the tracker, the target gets rewarded.
			if (GeomTools.canSee(cs.playerStates[playerNo], cs.playerStates[0],
					targetSensingParams, obstacles, MAX_SIGHT_DISTANCE_ERROR,
					NUM_CAMERA_ARM_STEPS)) {
				reward += 1;
			}
			// The tracker sees the target -> percept but no reward.
			if (GeomTools.canSee(cs.playerStates[0], cs.playerStates[playerNo],
					trackerSensingParams, obstacles, MAX_SIGHT_DISTANCE_ERROR,
					NUM_CAMERA_ARM_STEPS)) {
				cs.trackerPercepts.add(new Percept(turnNo, playerNo,
						new AgentState(cs.playerStates[playerNo])));
			}
		}
		return reward;
	}

	/**
	 * Simulates only the camera adjustment aspect of an action.
	 * 
	 * @param turnNo
	 *            the turn number.
	 * @param playerNo
	 *            the acting player.
	 * @param action
	 *            the action taken.
	 */
	public void simulateCameraAdjustment(int turnNo, int playerNo, Action action) {
		AgentState startState = action.getStartState();
		// If the action is invalid, ignore it.
		if (!startState.hasCamera()
				|| !startState.equals(cs.playerStates[playerNo])) {
			return;
		}
		AgentState resultingState = action.getResultingState();

		// If we are lengthening the camera arm, make sure it's valid.
		if (resultingState.getCameraArmLength() > startState
				.getCameraArmLength()) {
			Point2D playerPos = startState.getPosition();
			Point2D cameraPos = GeomTools.calculateViewPosition(resultingState);
			Line2D.Double playerLine = new Line2D.Double(playerPos, cameraPos);
			// If the new camera arm length causes collision, don't update.
			if (!GeomTools.isCollisionFree(playerLine, extendedObstacles)) {
				return;
			}
		}

		// Adjustment successful - update the state.
		cs.playerStates[playerNo] = resultingState;
	}

	/**
	 * Simulates only the movement aspect of an action.
	 * 
	 * @param turnNo
	 *            the turn number.
	 * @param playerNo
	 *            the acting player.
	 * @param action
	 *            the action taken.
	 */
	public void simulateMovement(int turnNo, int playerNo, Action action) {
		AgentState startState = action.getStartState();
		// If the start state doesn't match, we ignore the action.
		if (!startState.equals(cs.playerStates[playerNo])) {
			return;
		}

		Point2D startPos = startState.getPosition();
		double startHeading = startState.getHeading();

		AgentState endState = action.getResultingState();
		Point2D endPos = endState.getPosition();
		double endHeading = action.getHeading();
		double distance = action.getDistance();
		boolean hasCamera = endState.hasCamera();
		double armLength = endState.getCameraArmLength();

		// If the action includes an impossible turn, ignore the action.
		if (hasCamera
				&& (startHeading != endHeading)
				&& !GeomTools.canTurn(startPos, startHeading, endHeading,
						armLength, extendedObstacles)) {
			return;
		}

		// If the movement is invalid, ignore the whole action.
		if (distance != 0
				&& !GeomTools.canMove(startPos, endPos, hasCamera, armLength,
						extendedObstacles)) {
			return;
		}

		endState = new AgentState(endPos, endHeading, hasCamera, armLength);
		cs.playerStates[playerNo] = endState;
	}

	/**
	 * Returns true iff the given state lies within the goal.
	 * 
	 * @param s
	 *            the state to test.
	 * @return true iff the given state lies within the goal.
	 */
	public boolean isWithinGoal(AgentState s) {
		return goalRegion.getRect().contains(s.getPosition());
	}

	/**
	 * Writes the current game results to an output file.
	 * 
	 * @param outputPath
	 *            the path to write to.
	 * @throws IOException
	 *             if the file cannot be written.
	 */
	public void writeResults(String outputPath) throws IOException {
		String lineSep = System.getProperty("line.separator");
		FileWriter writer = new FileWriter(outputPath);
		writer.write(cs.turnNo + lineSep);
		writer.write(numTargets + lineSep);
		writer.write(trackerInitialState + lineSep);
		for (AgentState as : targetInitialStates) {
			writer.write(as + lineSep);
		}
		for (ActionResult[] results : actionResultSequence) {
			for (ActionResult result : results) {
				if (result.getDesiredAction() == null) {
					writer.write("-" + lineSep);
				} else {
					writer.write(result.getResultingState() + " "
							+ result.getReward() + lineSep);
				}
			}
		}
		writer.close();
	}

	/**
	 * Loads a completed game from an output file.
	 * 
	 * @param filename
	 *            the path to read from
	 * @throws IOException
	 *             if the file cannot be read.
	 */
	public void loadGame(String filename) throws IOException {
		if (!setupLoaded) {
			return;
		}
		actionResultSequence = new Stack<ActionResult[]>();
		stateSequence = new Stack<GameState>();
		stateSequence.push(new GameState());
		cs = new GameState();

		BufferedReader input = new BufferedReader(new FileReader(filename));
		String line;
		int lineNo = 0;
		Scanner s;
		try {
			line = input.readLine();
			lineNo++;
			s = new Scanner(line);
			int numTurns = s.nextInt();
			s.close();

			for (int i = 0; i < numTargets + 2; i++) {
				// Skip the initial-state lines.
				line = input.readLine();
				lineNo++;
			}

			int playerNo = 0;
			ActionResult[] results = new ActionResult[1];
			int numLines = (numTurns / 2) * (numTargets + 1);
			for (int i = 0; i < numLines; i++) {
				if (i == numLines - 1) {
					cs.gameComplete = true;
				}

				line = input.readLine();
				lineNo++;
				s = new Scanner(line);
				double x = s.nextDouble();
				double y = s.nextDouble();
				double heading = Math.toRadians(s.nextDouble());
				boolean hasCamera = cs.isTrackerTurn
						&& trackerSensingParams.hasCamera();
				double cameraArmLength = 0;
				if (hasCamera) {
					cameraArmLength = s.nextDouble();
				}
				double reward = s.nextDouble();
				s.close();
				Action action;
				AgentState oldState = cs.playerStates[playerNo];
				AgentState newState = new AgentState(new Point2D.Double(x, y),
						heading, hasCamera, cameraArmLength);
				cs.playerStates[playerNo] = newState;
				if (cs.isTrackerTurn) {
					if (!oldState.getPosition().equals(newState.getPosition())) {
						action = new TrackerAction(oldState, heading,
								trackerMoveDistance);
					} else if (oldState.getHeading() != newState.getHeading()) {
						action = new TrackerAction(oldState, heading, 0);
					} else if (oldState.getCameraArmLength() != newState
							.getCameraArmLength()) {
						action = new TrackerAction(oldState,
								newState.getCameraArmLength());
					} else {
						// HQ call are ignored - it won't matter in the
						// visualiser.
						action = new TrackerAction(oldState, false);
					}
				} else {
					action = new Action(oldState, newState.getPosition());
				}

				int index = (playerNo == 0) ? 0 : playerNo - 1;
				results[index] = new ActionResult(action, action, newState,
						reward);
				cs.playerScores[playerNo] += reward;

				playerNo += 1;
				if (cs.isTrackerTurn) {
					cs.turnNo += 1;
					stateSequence.push(cs);
					cs = new GameState(cs);
					cs.isTrackerTurn = false;
					actionResultSequence.push(results);
					results = new ActionResult[numTargets];
				} else if (playerNo > numTargets) {
					playerNo = 0;
					cs.turnNo += 1;
					stateSequence.push(cs);
					cs = new GameState(cs);
					cs.isTrackerTurn = true;
					actionResultSequence.push(results);
					results = new ActionResult[1];
				}
			}

		} catch (InputMismatchException e) {
			throw new IOException(String.format(
					"Invalid number format on line %d of %s: %s", lineNo,
					filename, e.getMessage()));
		} catch (NoSuchElementException e) {
			throw new IOException(String.format(
					"Not enough tokens on line %d of %s", lineNo, filename));
		} catch (NullPointerException e) {
			throw new IOException(String.format(
					"Line %d expected, but file %s ended.", lineNo, filename));
		} finally {
			input.close();
		}
	}

	/**
	 * Returns the runtime target motion history.
	 * 
	 * @return the runtime target motion history.
	 */
	public MotionHistory getRuntimeTargetMotionHistory() {
		return runtimeTargetMotionHistory;
	}

	/**
	 * Returns the runtime tracker motion history.
	 * 
	 * @return the runtime tracker motion history.
	 */
	public MotionHistory getRuntimeTrackerMotionHistory() {
		return runtimeTrackerMotionHistory;
	}

	/**
	 * Saves the current history to the runtime variables.
	 */
	public void saveHistory() {
		addTargetHistoryEntries(runtimeTargetMotionHistory);
		addTrackerHistoryEntries(runtimeTrackerMotionHistory);
	}

	/**
	 * Resets the runtime history.
	 */
	public void resetHistory() {
		runtimeTargetMotionHistory = new MotionHistory();
		runtimeTrackerMotionHistory = new MotionHistory();
	}

	/**
	 * Adds the current entries to the given target motion history.
	 * 
	 * @param history
	 *            the history to add to.
	 */
	public void addTargetHistoryEntries(MotionHistory history) {
		for (int i = 1; i < actionResultSequence.size(); i += 2) {
			ActionResult[] results = actionResultSequence.get(i);
			for (ActionResult result : results) {
				history.addEntry(result, targetPolicy.getGrid());
			}
		}
	}

	/**
	 * Adds the current entries to the given tracker motion history.
	 * 
	 * @param history
	 *            the history to add to.
	 */
	public void addTrackerHistoryEntries(MotionHistory history) {
		for (int i = 0; i < actionResultSequence.size(); i += 2) {
			ActionResult[] results = actionResultSequence.get(i);
			history.addEntry(results[0], new TrackerGrid(
					trackerMoveDistance / 2));
		}
	}

	/* ---------------------- COMMAND LINE RUNNER ------------------------ */
	/**
	 * Runs a game, and outputs the result.
	 * 
	 * @param outputPath
	 *            the file to output to, or null if no file output is wanted.
	 * @param verbose
	 *            true iff System output on the game result is required.
	 * @return the result of the game: 1 -> Tracker victory. 0 -> Draw. -1 ->
	 *         Tracker loss.
	 */
	public int runVerbose(String outputPath, boolean verbose) {
		runFull();
		int winResult = cs.getResult();
		if (verbose) {
			System.out.print(cs.getResultString() + ";");
			double[] scores = cs.getPlayerScores();
			if (numTargets > 1) {
				System.out.print(" target scores: ");
				StringBuilder sb = new StringBuilder();
				for (int i = 1; i <= numTargets; i++) {
					double score = scores[i];
					sb.append(String.format("%d ", (int) score));
				}
				System.out.println(sb);
			} else {
				System.out.println();
			}
		}

		if (outputPath != null) {
			try {
				writeResults(outputPath);
			} catch (IOException e) {
				System.err.println("Failed to write output: " + e.getMessage());
			}
		}
		return winResult;
	}

	/**
	 * Runs a game, with the problem setup file passed from the command line.
	 * 
	 * @param args
	 *            command line arguments; the first should be the setup file.
	 */
	public static void main(String[] args) {
		String setupFile = null;
		String outputFile = null;
		String targetFile = null;
		String trackerFile = null;
		for (int i = 0; i < args.length; i++) {
			String arg = args[i].trim();
			if (arg.equals("-o")) {
				i++;
				if (i < args.length) {
					outputFile = args[i].trim();
				}
			} else {
				if (setupFile == null) {
					setupFile = arg;
				} else if (targetFile == null) {
					targetFile = arg;
				} else if (trackerFile == null) {
					trackerFile = arg;
				}
			}
		}
		if (setupFile == null) {
			setupFile = DEFAULT_SETUP_FILE;
		}
		if (outputFile == null) {
			outputFile = DEFAULT_OUTPUT_FILE;
		}
		if (targetFile == null) {
			targetFile = DEFAULT_TARGET_FILE;
		}
		if (trackerFile == null) {
			trackerFile = DEFAULT_TRACKER_FILE;
		}
		GameRunner runner = new GameRunner();
		runner.setTargetDistribution(targetFile);
		runner.setTrackerDistribution(trackerFile);
		long globalSeed = new Random().nextLong();
		System.out.println("Global seed: " + globalSeed);
		runner.setSeed(globalSeed);

		try {
			runner.loadSetup(setupFile);
		} catch (IOException e) {
			System.err.println("Failed to load setup file: " + e.getMessage());
			return;
		}
		int numGames = 100;
		int numWins = 0;
		for (int i = 0; i < numGames; i++) {
			int result = runner.runVerbose(outputFile, true);
			runner.saveHistory();
			if (result == 1) {
				numWins += 1;
			}
		}
		System.out.println(String.format("Tracker won %d of %d games.",
				numWins, numGames));
		/*
		 * try { runner.getRuntimeTargetMotionHistory().writeToFile(
		 * "targetMotionHistory.txt");
		 * runner.getRuntimeTrackerMotionHistory().writeToFile(
		 * "trackerMotionHistory.txt"); } catch (IOException e) {
		 * e.printStackTrace(); }
		 */
	}
}