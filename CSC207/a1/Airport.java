
import java.util.ArrayList;

public class Airport {
	private String name;
	private ArrayList<Flight> flights;

	public Airport(String name) {
		this.name = name;
		this.flights = new ArrayList<>();
	}

	public boolean wasVisitedBy(Flight flight) {
        return this.flights.contains(flight);
	}

	public boolean onSameFlight(Airport ap) {
        for (Flight flight: this.flights) {
            if (ap.flights.contains(flight)) {
                return true;
            }
        }
        return false;
    }

	public void addFlight(Flight flight) {
        if (flights.contains(flight)) {
            return;
        } else {
            flights.add(flight);
            flight.addAirport(this);
        }
    }

	public boolean equals(Object obj) {
	    if (obj instanceof Airport && this.getName().equals(((Airport) obj).getName()) && this.flights.size() == ((Airport) obj).flights.size()) {
	        for (Flight flight: this.flights) {
                if (!((Airport) obj).flights.contains(flight)) {
                    return false;
                }
            }
            for (Flight flight: ((Airport) obj).flights) {
	            if (!this.flights.contains(flight)) {
	                return false;
                }
            }
            return true;
	    } else {
	        return false;
        }
	}

	public String getName() {
		return this.name;
	}

	public String toString() {
		StringBuilder store = new StringBuilder("(");
		if (this.flights.isEmpty()) {
		    store.append(")");
        } else {
		    for (int i = 0; i < this.flights.size(); i++) {
                if (i == this.flights.size() - 1) {
                    store.append(this.flights.get(i).getName() + ")");
                } else {
                    store.append(this.flights.get(i).getName() + ", ");
                }
            }

        }
        return this.name + " " + store;
	}

}
