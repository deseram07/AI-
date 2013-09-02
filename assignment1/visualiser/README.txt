A visualiser for COMP3702 Assignment 1, by Dimitri Klimenko (tutor).

(1) Running the JAR
To run it, simply run the JAR archive with Java 7 (double-clicking should work
if Java is installed properly). If this doesn't work or you want to run it
with a different version, I recommend using Eclipse - simply add the contents
of visualiser.zip to the "src" folder in a new project, and it should work.
Alternatively, see the manual compilation instructions further below.

You can also run it from the command line with optional
command-line arguments:
    java -jar visualiser.jar [problem-file] [solution-file]

For example, using the test cases provided here:
    java -jar visualiser.jar test_problem.txt test_solution.txt


(2) Command lines and the Java Path
Note that for the command-line commands to work Java would have to be on your
system path; if not, you'll have to specify a full path instead of just "java",
e.g.
"C:\Program Files (x86)\Java\jdk1.7.0_25\bin\java.exe"
or
/usr/java/jdk1.7.0_25/bin/java


(3) Manual Compilation
If you want to compile and run the code manually, you will need to do the
following:
1) Extract visualiser.zip into your desired folder.
2) From within this folder, run the command:
    javac visualiser/*.java
3) Now, to run the code, you simply run:
    java visualiser/Visualiser

As with the JAR, you can add command-line arguments, e.g.
    java visualiser/Visualiser test_problem.txt test_solution.txt

Moreover, full paths will be needed if you don't have Java on your system
path; see the details in section (2).
