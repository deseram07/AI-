package visualiser;


import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class ProblemSetup {
	private boolean problemLoaded = false;
	private boolean solutionLoaded = false;
	
	private int asvCount;
	private State initialState;
	private State goalState;
	private List<Obstacle> obstacles;
	
	private List<State> path;
	
	public void loadProblem(String filename) throws IOException {
		problemLoaded = false;
		solutionLoaded = false;
		BufferedReader input = new BufferedReader(new FileReader(filename));
		try {
			asvCount = Integer.valueOf(input.readLine().trim());
			initialState = new State(asvCount, input.readLine().trim());
			goalState = new State(asvCount, input.readLine().trim());
			
			int numObstacles = Integer.valueOf(input.readLine().trim());
			obstacles = new ArrayList<Obstacle>();
			for (int i = 0; i < numObstacles; i++) {
				obstacles.add(new Obstacle(input.readLine().trim()));
			}
			input.close();
			problemLoaded = true;
		} catch (NumberFormatException e) {
			throw new IOException("Invalid number format.");
		} catch (IndexOutOfBoundsException e) {
			throw new IOException("Invalid format; not enough tokens in a line.");
		}
	}
	
	public void loadSolution(String filename) throws IOException {
		if (!problemLoaded) {
			return;
		}
		solutionLoaded = false;
		BufferedReader input = new BufferedReader(new FileReader(filename));
		try {
			String[] tokens = input.readLine().trim().split("\\s+");
			int pathLength = Integer.valueOf(tokens[0]);
			path = new ArrayList<State>();
			for (int i = 0; i < pathLength; i++) {
				State s = new State(asvCount, input.readLine().trim());
				path.add(s);
			}
			input.close();
			solutionLoaded = true;
		} catch (NumberFormatException e) {
			throw new IOException("Invalid number format.");
		} catch (IndexOutOfBoundsException e) {
			throw new IOException("Invalid format; not enough tokens in a line.");
		}
	}
	
	public int getASVCount() {
		return asvCount;
	}
	
	public State getInitialState() {
		return initialState;
	}
	
	public State getGoalState() {
		return goalState;
	}
	
	public List<State> getPath() {
		return new ArrayList<State>(path);
	}
	
	public List<Obstacle> getObstacles() {
		return new ArrayList<Obstacle>(obstacles);
	}
	
	public boolean problemLoaded() {
		return problemLoaded;
	}
	
	public boolean solutionLoaded() {
		return solutionLoaded;
	}
}
