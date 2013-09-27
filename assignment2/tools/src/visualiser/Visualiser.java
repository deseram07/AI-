package visualiser;

import game.GameRunner;
import game.GameRunner.GameState;

import java.awt.BorderLayout;
import java.awt.Component;
import java.awt.Container;
import java.awt.Dimension;
import java.awt.Font;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.ComponentEvent;
import java.awt.event.ComponentListener;
import java.awt.event.KeyEvent;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.io.File;
import java.io.IOException;

import javax.swing.BorderFactory;
import javax.swing.Box;
import javax.swing.BoxLayout;
import javax.swing.ImageIcon;
import javax.swing.JApplet;
import javax.swing.JButton;
import javax.swing.JFileChooser;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JMenu;
import javax.swing.JMenuBar;
import javax.swing.JMenuItem;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JSeparator;
import javax.swing.JSlider;
import javax.swing.JTable;
import javax.swing.border.EtchedBorder;
import javax.swing.event.ChangeEvent;
import javax.swing.event.ChangeListener;
import javax.swing.table.AbstractTableModel;

public class Visualiser {
	private Container container;

	private GameRunner gameRunner;
	private VisualisationPanel vp;

	private JPanel infoPanel;
	private JTable scoreTable;
	private JLabel infoLabel;

	private JMenuBar menuBar;
	private JMenu fileMenu;
	private JMenuItem loadSetupItem, writeOutputItem, exitItem;
	private JMenu gameMenu;
	private JMenuItem playPauseItem, resetItem, backItem, forwardItem,
			stepItem;

	private JPanel gameControls;
	private JSlider manualSlider;
	private JSlider framePeriodSlider;

	protected ImageIcon createImageIcon(String path, String description) {
		java.net.URL imgURL = getClass().getResource(path);
		if (imgURL != null) {
			return new ImageIcon(imgURL, description);
		} else {
			return new ImageIcon(path, description);
		}
	}

	private JButton playPauseButton, resetButton, backButton, forwardButton,
			stepButton;
	private ImageIcon playIcon = createImageIcon("play.gif", "Play");
	private ImageIcon pauseIcon = createImageIcon("pause.gif", "Pause");
	private ImageIcon resetIcon = createImageIcon("reset.gif", "Reset");
	private ImageIcon backIcon = createImageIcon("back.gif", "Back");
	private ImageIcon forwardIcon = createImageIcon("forward.gif", "Forward");
	private ImageIcon stepIcon = createImageIcon("step.gif", "Step");

	private boolean hasSetup;
	private boolean playing;
	private boolean wasPlaying;

	private static final int FRAME_PERIOD_MIN = 10;
	private static final int FRAME_PERIOD_MAX = 1000;
	private static final int FRAME_PERIOD_INIT = 100;

	private File defaultPath;

	private class MenuListener implements ActionListener {
		public void actionPerformed(ActionEvent e) {
			String cmd = e.getActionCommand();
			if (cmd.equals("Load setup")) {
				loadSetup();
			} else if (cmd.equals("Write output")) {
				writeOutput();
			} else if (cmd.equals("Play")) {
				vp.playPauseAnimation();
			} else if (cmd.equals("Pause")) {
				vp.playPauseAnimation();
			} else if (cmd.equals("Reset")) {
				vp.resetGame();
			} else if (cmd.equals("Back one step")) {
				vp.gotoFrame(vp.getFrameNumber() - 1);
			} else if (cmd.equals("Forward one step")) {
				vp.gotoFrame(vp.getFrameNumber() + 1);
			} else if (cmd.equals("Simulate one step")) {
				vp.stepGame();
			}
		}
	}

	private class ResizeListener implements ComponentListener {
		@Override
		public void componentResized(ComponentEvent e) {
			updateTickSpacing();
		}

		@Override
		public void componentHidden(ComponentEvent e) {
		}

		@Override
		public void componentMoved(ComponentEvent e) {
		}

		@Override
		public void componentShown(ComponentEvent e) {
		}
	}

	private AbstractTableModel tableDataModel = new AbstractTableModel() {
		/** Required UID */
		private static final long serialVersionUID = 2401048818869542809L;

		public int getColumnCount() {
			if (!gameRunner.setupLoaded()) {
				return 0;
			}
			return 3 + gameRunner.getNumTargets();
		}

		public int getRowCount() {
			return 2;
		}

		public Object getValueAt(int row, int col) {
			if (col == 0) {
				if (row == 0) {
					return "Player";
				} else {
					return "Score";
				}
			}

			if (row == 0) {
				if (col == 1) {
					return "Tracker";
				} else if (col == 2) {
					return "Target total";
				} else {
					return "Target #" + (col - 2);
				}
			} else {
				if (col == 1) {
					return vp.getCurrentState().getTrackerScore();
				} else if (col == 2) {
					return vp.getCurrentState().getTargetScore();
				} else {
					return vp.getCurrentState().getPlayerScores()[col - 2];
				}
			}
		}
	};

	private ResizeListener resizeListener = new ResizeListener();
	private MenuListener menuListener = new MenuListener();

	private ChangeListener manualSliderListener = new ChangeListener() {
		@Override
		public void stateChanged(ChangeEvent e) {
			if (!manualSlider.getValueIsAdjusting() && wasPlaying) {
				wasPlaying = false;
				if (manualSlider.getValue() < manualSlider.getMaximum()) {
					vp.playPauseAnimation();
				}
			}
			int value = manualSlider.getValue();
			if (value < 0) {
				value = 0;
			}
			vp.gotoFrame(value);
		}
	};

	private MouseListener manualSliderClickListener = new MouseListener() {
		@Override
		public void mousePressed(MouseEvent e) {
			if (playing) {
				wasPlaying = true;
				vp.playPauseAnimation();
			}
		}

		@Override
		public void mouseReleased(MouseEvent e) {
		}

		@Override
		public void mouseClicked(MouseEvent e) {
		}

		@Override
		public void mouseEntered(MouseEvent e) {
		}

		@Override
		public void mouseExited(MouseEvent e) {
		}
	};

	private ChangeListener framePeriodListener = new ChangeListener() {
		@Override
		public void stateChanged(ChangeEvent e) {
			vp.setPeriod(framePeriodSlider.getValue());
		}
	};

	private ActionListener playPauseListener = new ActionListener() {
		@Override
		public void actionPerformed(ActionEvent arg0) {
			vp.playPauseAnimation();
		}
	};

	private ActionListener forwardListener = new ActionListener() {
		@Override
		public void actionPerformed(ActionEvent arg0) {
			vp.gotoFrame(vp.getFrameNumber() + 1);
		}
	};

	private ActionListener backListener = new ActionListener() {
		@Override
		public void actionPerformed(ActionEvent arg0) {
			vp.gotoFrame(vp.getFrameNumber() - 1);
		}
	};

	private ActionListener stepListener = new ActionListener() {
		@Override
		public void actionPerformed(ActionEvent arg0) {
			vp.stepGame();
		}
	};

	private ActionListener resetListener = new ActionListener() {
		@Override
		public void actionPerformed(ActionEvent arg0) {
			vp.resetGame();
		}
	};

	public Visualiser(Container container, File defaultPath) {
		this.container = container;
		this.defaultPath = defaultPath;
		this.gameRunner = new GameRunner();
		createComponents();
		setHasSetup(false);
	}

	public Visualiser(Container container) {
		this(container, null);
		try {
			this.defaultPath = new File(".").getCanonicalFile();
		} catch (IOException e) {
		}
	}

	private void createComponents() {
		vp = new VisualisationPanel(gameRunner, this);
		JPanel wp = new JPanel(new BorderLayout());
		wp.add(vp, BorderLayout.CENTER);
		container.setLayout(new BorderLayout());
		wp.setBorder(BorderFactory.createCompoundBorder(
				BorderFactory.createEmptyBorder(5, 10, 10, 10),
				BorderFactory.createEtchedBorder(EtchedBorder.LOWERED)));
		container.add(wp, BorderLayout.CENTER);

		infoPanel = new JPanel();
		infoPanel.setLayout(new BorderLayout());
		infoLabel = new JLabel();
		updateInfoText();
		JPanel p = new JPanel();
		p.add(infoLabel);
		infoPanel.add(p, BorderLayout.CENTER);
		scoreTable = new JTable(tableDataModel);
		// JScrollPane scrollPane = new JScrollPane(scoreTable);
		infoPanel.add(scoreTable, BorderLayout.EAST);
		infoPanel.setBorder(BorderFactory.createEmptyBorder(10, 10, 5, 10));

		container.add(infoPanel, BorderLayout.NORTH);

		createMenus();
		createAnimationControls();
	}

	private void createMenus() {
		menuBar = new JMenuBar();
		createFileMenu();
		createGameMenu();
		if (container instanceof JFrame) {
			((JFrame) container).setJMenuBar(menuBar);
		} else if (container instanceof JApplet) {
			((JApplet) container).setJMenuBar(menuBar);
		}
	}

	private void createFileMenu() {
		fileMenu = new JMenu("File");
		fileMenu.setMnemonic(KeyEvent.VK_F);
		fileMenu.getAccessibleContext().setAccessibleDescription(
				"Load configs or close the app.");
		menuBar.add(fileMenu);

		loadSetupItem = new JMenuItem("Load setup");
		loadSetupItem.setMnemonic(KeyEvent.VK_L);
		loadSetupItem.addActionListener(menuListener);
		fileMenu.add(loadSetupItem);

		writeOutputItem = new JMenuItem("Write output");
		writeOutputItem.setMnemonic(KeyEvent.VK_W);
		writeOutputItem.addActionListener(menuListener);
		fileMenu.add(writeOutputItem);

		fileMenu.addSeparator();
		exitItem = new JMenuItem("Exit");
		exitItem.setMnemonic(KeyEvent.VK_X);
		exitItem.addActionListener(menuListener);
		fileMenu.add(exitItem);
	}

	private void createGameMenu() {
		gameMenu = new JMenu("Game");
		gameMenu.setMnemonic(KeyEvent.VK_A);
		fileMenu.getAccessibleContext().setAccessibleDescription(
				"Manage the animation.");
		menuBar.add(gameMenu);
		gameMenu.setEnabled(false);

		stepItem = new JMenuItem("Simulate one step");
		stepItem.setMnemonic(KeyEvent.VK_S);
		stepItem.addActionListener(menuListener);
		gameMenu.add(stepItem);

		playPauseItem = new JMenuItem("Play");
		playPauseItem.setMnemonic(KeyEvent.VK_P);
		playPauseItem.addActionListener(menuListener);
		gameMenu.add(playPauseItem);

		resetItem = new JMenuItem("Reset");
		resetItem.setMnemonic(KeyEvent.VK_T);
		resetItem.addActionListener(menuListener);
		gameMenu.add(resetItem);

		backItem = new JMenuItem("Back one step");
		backItem.setMnemonic(KeyEvent.VK_B);
		backItem.addActionListener(menuListener);
		backItem.setEnabled(false);
		gameMenu.add(backItem);

		forwardItem = new JMenuItem("Forward one step");
		forwardItem.setMnemonic(KeyEvent.VK_F);
		forwardItem.addActionListener(menuListener);
		forwardItem.setEnabled(false);
		gameMenu.add(forwardItem);
	}

	private void createAnimationControls() {
		Font sliderFont = new Font("Arial", Font.PLAIN, 12);

		gameControls = new JPanel();
		gameControls
				.setLayout(new BoxLayout(gameControls, BoxLayout.PAGE_AXIS));

		JLabel manualLabel = new JLabel("Frame #");
		manualLabel.setAlignmentX(Component.CENTER_ALIGNMENT);
		manualSlider = new JSlider(JSlider.HORIZONTAL);
		manualSlider.setPaintTicks(true);
		manualSlider.setPaintLabels(true);
		manualSlider.setFont(sliderFont);
		manualSlider.addChangeListener(manualSliderListener);
		manualSlider.addMouseListener(manualSliderClickListener);
		manualSlider.setMinorTickSpacing(1);
		manualSlider.addComponentListener(resizeListener);

		JLabel framePeriodLabel = new JLabel("Frame period (ms)");
		framePeriodLabel.setAlignmentX(Component.CENTER_ALIGNMENT);
		framePeriodSlider = new JSlider(JSlider.HORIZONTAL, FRAME_PERIOD_MIN,
				FRAME_PERIOD_MAX, FRAME_PERIOD_INIT);
		framePeriodSlider.setMajorTickSpacing(200);
		framePeriodSlider.setMinorTickSpacing(10);
		framePeriodSlider.setPaintTicks(true);
		framePeriodSlider.setPaintLabels(true);
		framePeriodSlider.setLabelTable(framePeriodSlider.createStandardLabels(
				200, 200));
		framePeriodSlider.setFont(sliderFont);
		framePeriodSlider.addChangeListener(framePeriodListener);
		JPanel framePeriodPanel = new JPanel();
		framePeriodPanel.setLayout(new BoxLayout(framePeriodPanel,
				BoxLayout.PAGE_AXIS));
		framePeriodPanel.add(framePeriodLabel);
		framePeriodPanel.add(Box.createRigidArea(new Dimension(0, 2)));
		framePeriodPanel.add(framePeriodSlider);
		vp.setPeriod(framePeriodSlider.getValue());

		stepButton = new JButton(stepIcon);
		stepButton.addActionListener(stepListener);
		backButton = new JButton(backIcon);
		backButton.addActionListener(backListener);
		backButton.setEnabled(false);
		forwardButton = new JButton(forwardIcon);
		forwardButton.addActionListener(forwardListener);
		forwardButton.setEnabled(false);
		playPauseButton = new JButton(playIcon);
		playPauseButton.addActionListener(playPauseListener);
		resetButton = new JButton(resetIcon);
		resetButton.addActionListener(resetListener);

		gameControls.add(new JSeparator(JSeparator.HORIZONTAL));
		gameControls.add(Box.createRigidArea(new Dimension(0, 2)));
		gameControls.add(manualLabel);
		gameControls.add(Box.createRigidArea(new Dimension(0, 2)));
		gameControls.add(manualSlider);
		gameControls.add(Box.createRigidArea(new Dimension(0, 5)));
		JPanel p2 = new JPanel();
		p2.setLayout(new BoxLayout(p2, BoxLayout.LINE_AXIS));
		p2.add(backButton);
		p2.add(Box.createRigidArea(new Dimension(5, 0)));
		p2.add(forwardButton);
		p2.add(Box.createRigidArea(new Dimension(5, 0)));
		p2.add(stepButton);
		p2.add(Box.createRigidArea(new Dimension(5, 0)));
		p2.add(playPauseButton);
		p2.add(Box.createRigidArea(new Dimension(5, 0)));
		p2.add(resetButton);
		p2.add(framePeriodPanel);
		gameControls.add(p2);
		gameControls.setBorder(BorderFactory.createEmptyBorder(0, 10, 5, 10));
		container.add(gameControls, BorderLayout.SOUTH);
	}

	private File askForFile() {
		JFileChooser fc = new JFileChooser(defaultPath);
		int returnVal = fc.showOpenDialog(container);
		if (returnVal != JFileChooser.APPROVE_OPTION) {
			return null;
		}
		return fc.getSelectedFile();
	}

	private void showFileError(File f) {
		JOptionPane.showMessageDialog(container,
				"Error loading " + f.getName(), "File I/O Error",
				JOptionPane.ERROR_MESSAGE);
	}

	private void loadSetup(File f) {
		try {
			gameRunner.loadSetup(f.getPath());
			setHasSetup(true);
		} catch (IOException e) {
			JOptionPane.showMessageDialog(container, e.getMessage(), "",
					JOptionPane.ERROR_MESSAGE);
			showFileError(f);
		}
	}

	private void loadSetup() {
		File f = askForFile();
		if (f == null) {
			return;
		}
		loadSetup(f);
	}

	private void writeOutput(File f) {
		try {
			gameRunner.writeResults(f.getPath());
		} catch (IOException e) {
			showFileError(f);
		}
	}

	private void writeOutput() {
		File f = askForFile();
		if (f == null) {
			return;
		}
		writeOutput(f);
	}

	public void setHasSetup(boolean hasSetup) {
		this.hasSetup = hasSetup;
		if (hasSetup) {
			vp.resetGame();
		}
		tableDataModel.fireTableStructureChanged();
		updateControls();
		gameControls.setVisible(hasSetup);
		gameMenu.setEnabled(hasSetup);
		writeOutputItem.setEnabled(hasSetup);
		vp.repaint();
	}

	public void setPlaying(boolean playing) {
		if (this.playing == playing) {
			return;
		}
		this.playing = playing;
		if (playing) {
			playPauseItem.setText("Pause");
			playPauseButton.setIcon(pauseIcon);
		} else {
			playPauseItem.setText("Play");
			playPauseButton.setIcon(playIcon);
		}
		playPauseButton.repaint();

	}

	public void updateControls() {
		if (!hasSetup) {
			return;
		}
		boolean canBack = vp.getFrameNumber() > 0;
		backButton.setEnabled(canBack);
		backItem.setEnabled(canBack);

		boolean canForward = vp.getFrameNumber() < gameRunner.getTurnNo();
		forwardButton.setEnabled(canForward);
		forwardItem.setEnabled(canForward);

		boolean canStep = (!gameRunner.gameComplete() || canForward);
		stepButton.setEnabled(canStep);
		stepItem.setEnabled(canStep);
	}

	public void updateInfoText() {
		if (!gameRunner.setupLoaded()) {
			infoLabel.setText("No problem to display.");
			return;
		}
		GameState state = vp.getCurrentState();
		if (state.isGameComplete()) {
			infoLabel.setText("Game complete! " + state.getResultString());
//			gameRunner.resetHistory();
//			gameRunner.saveHistory();
//			System.out.println("Tracker motion history:");
//			System.out.println(gameRunner.getRuntimeTrackerMotionHistory());
//			System.out.println("Target motion history:");
//			System.out.println(gameRunner.getRuntimeTargetMotionHistory());
		} else if (state.isTrackerTurn()) {
			infoLabel.setText("Tracker to act.");
		} else {
			infoLabel.setText("Targets to act.");
		}
	}

	public void updateTable() {
		tableDataModel.fireTableDataChanged();
	}

	public void updateMaximum() {
		int maximum = gameRunner.getTurnNo();
		manualSlider.setMaximum(maximum);
		updateTickSpacing();
		updateControls();
	}

	public void updateSliderSpacing(JSlider slider) {
		int width = slider.getBounds().width;
		int max = slider.getMaximum();
		int spacing = 1;
		int mode = 1;
		double pxPerLabel = (double) width * spacing / max;
		if (pxPerLabel <= 0) {
			return;
		}
		while (pxPerLabel <= 30) {
			if (mode == 1) {
				spacing *= 2;
				pxPerLabel *= 2;
				mode = 2;
			} else if (mode == 2) {
				spacing = spacing * 5 / 2;
				pxPerLabel *= 2.5;
				mode = 5;
			} else {
				spacing *= 2;
				pxPerLabel *= 2;
				mode = 1;
			}
		}
		slider.setMajorTickSpacing(spacing);
		int min = slider.getMinimum();
		if (min % spacing > 0) {
			min += (spacing - (min % spacing));
		}
		slider.setLabelTable(slider.createStandardLabels(spacing, min));
	}

	public void updateTickSpacing() {
		updateSliderSpacing(manualSlider);
		updateSliderSpacing(framePeriodSlider);
	}

	public void setFrameNumber(int frameNumber) {
		manualSlider.setValue(frameNumber);
		updateControls();
	}

	public static void main(String[] args) {
		JFrame frame = new JFrame("Assignment 1 visualiser");
		Visualiser vis = new Visualiser(frame);
		if (args.length > 0) {
			vis.loadSetup(new File(args[0]));
		}
		frame.setSize(800, 1000);
		frame.addWindowListener(new WindowAdapter() {
			public void windowClosing(WindowEvent e) {
				System.exit(0);
			}
		});
		frame.setVisible(true);
	}
}
