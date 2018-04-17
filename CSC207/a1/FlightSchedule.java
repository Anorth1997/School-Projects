import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.HashMap;
import java.util.Scanner;

public class FlightSchedule {
	public static void main(String[] args) throws IOException{

        File file = new File("FlightList.txt");
        Scanner sc = new Scanner(file);

        HashMap<String, Airport> stock = new HashMap<>();

		while (sc.hasNextLine()) { // Don't use != because compares memory addresses.
            String[] flightinfo = sc.nextLine().split("\\s\\|\\s");
            if (flightinfo.length > 1) {
                flightinfo[flightinfo.length - 1] = flightinfo[flightinfo.length - 1].substring(0, 3); //da
                for (int i = 1; i < flightinfo.length; i++) {
                    if (!stock.containsKey(flightinfo[i]))
                        stock.put(flightinfo[i], new Airport(flightinfo[i]));
                    Flight just = new Flight(flightinfo[0].split("\\s")[0], flightinfo[0].split("\\s")[1]);
                    stock.get(flightinfo[i]).addFlight(just);
                }
            }
		}


		BufferedReader kbd = new BufferedReader(new InputStreamReader(System.in));
		System.out.println("Enter the name of an airport");
		String input = kbd.readLine();
		while (!input.equals("exit")) {
		    if (stock.containsKey(input))
		        System.out.println(stock.get(input));
		    input = kbd.readLine();
        }
	}
}
