package loggingsystem;

import imagemanager.*;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.*;

/**
 * A logging system that traces renaming to directory or image ever done with information new name,
 * old name and timestamp.
 */
public class ImageLogger implements Observer{


    /**
     * An instance of the ImageLogger.
     */
    private static ImageLogger ourInstance = new ImageLogger();

    /**
     * The path of the configuration file which demonstrates the MasterLog.
     */
    private final static String filePath = System.getProperty("user.dir") + File.separator + "log.txt";


    /**
     * Constructor for ImageLogger.
     */
    private ImageLogger(){}

    /**
     * Return an instance of ImageLogger.
     *
     * @return the instance of ImageLogger
     */
    public static ImageLogger getOurInstance() {
        return ourInstance;
    }

    /**
     * Writes the new log into the file log.txt.
     *
     * @param newLog a string to log into the file
     * @throws IOException an exception to throw
     */
    private void writeFile(String newLog) throws IOException {
        System.out.println(newLog);
        FileWriter fw = new FileWriter(filePath, true);
        BufferedWriter bw = new BufferedWriter(fw);

        createAvailableTagsFile();

        bw.write(newLog);
        bw.close();
    }

    /**
     * Update this ImageLogger with the information within arg.
     *
     * @param o an observable object
     * @param arg an object to use to update
     */
    @Override
    public void update(Observable o, Object arg){
        ImageFile image = (ImageFile) o;
        String newName = image.getName();
        String oldName = (String) arg;

        String timeStamp = new SimpleDateFormat("yyyy.MM.dd.HH.mm.ss").format(new Date());


        //This string representation of log is going to be written in log.txt file.
        String log = String.format("%s\nOld Name:%s\nNew Name:%s\n\n", timeStamp, oldName, newName);

        //Write the log into log.txt
        try {
            writeFile(log);
        } catch (IOException e) {
            System.err.println("Failed to write into log.txt");
        }
    }


    /**
     * Checks if the availableTags.txt file exists. If not, then create a new one.
     *
     * @throws IOException an exception to throw
     */
    private static void createAvailableTagsFile() throws IOException{
        File logfile = new File(filePath);
        if (!logfile.exists()) {
            System.err.println("we had to make a new log file");
            logfile.createNewFile();
        }
    }
}
