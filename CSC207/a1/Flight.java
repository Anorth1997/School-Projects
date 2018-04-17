
import java.util.ArrayList;

public class Flight {
	private String name;
	private ArrayList<Airport> airports;
	private String date;

	public Flight(String name, String date) {
		this.name = name;
		this.date = date;
		this.airports = new ArrayList<>();
	}

	public void addAirport(Airport airport) {
        if (airports.contains(airport)) {
            return;
        } else {
            airports.add(airport);
            airport.addFlight(this);
        }
    }

	public boolean equals(Object obj) {
		if (obj instanceof Flight) {
			return (this.getName().equals(((Flight) obj).getName())) && (this.getDate().equals(((Flight) obj).getDate()));
		} else {
			return false;
		}
	}

	public ArrayList getAirports() {
		return this.airports;
	}

	public String getName() {
		return this.name;
	}

	public String getDate() {
		return this.date;
	}

	public String toString() {
	    String store = "";
		for (Airport x: this.airports) {
		    store += "\n" + x.getName();
        }
		return this.name + ", " + this.date + store;
	}
}
