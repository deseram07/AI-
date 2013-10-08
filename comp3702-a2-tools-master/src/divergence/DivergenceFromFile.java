package divergence;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.HashMap;
import java.util.InputMismatchException;
import java.util.Map;
import java.util.NoSuchElementException;
import java.util.Scanner;

/**
 * Represents the divergence in the actions of an agent
 * 
 * @author lackofcheese
 * 
 */
public abstract class DivergenceFromFile extends ActionDivergence {
	/** The probability distribution for this divergence. */
	private HashMap<Integer, HashMap<Integer, Double>> distribution;

	/**
	 * Creates a divergence with the given distribution.
	 * 
	 * @param filename
	 *            the file to load the distribution from.
	 */
	public DivergenceFromFile(String filename) throws IOException {
		distribution = new HashMap<Integer, HashMap<Integer, Double>>();
		BufferedReader input = new BufferedReader(new FileReader(filename));
		String line;
		int lineNo = 0;
		Scanner s;
		try {
			lineNo++;
			while ((line = input.readLine()) != null) {
				s = new Scanner(line);
				int desiredState = s.nextInt();
				int resultingState = s.nextInt();
				double probability = s.nextDouble();
				HashMap<Integer, Double> dist = distribution.get(desiredState);
				if (dist == null) {
					dist = new HashMap<Integer, Double>();
					distribution.put(desiredState, dist);
				}
				dist.put(resultingState, probability);
				lineNo++;
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
	 * Diverges an action based on its action code.
	 * 
	 * @param desiredCode
	 *            the desired action code.
	 * @return the diverged action code.
	 */
	public int divergeCode(int desiredCode) {
		double r = random.nextDouble();
		double totalProb = 0;
		int resultCode = 0;
		for (Map.Entry<Integer, Double> entry : distribution.get(desiredCode)
				.entrySet()) {
			resultCode = entry.getKey();
			totalProb += entry.getValue();
			if (totalProb >= r) {
				break;
			}
		}
		return resultCode;
	}
}