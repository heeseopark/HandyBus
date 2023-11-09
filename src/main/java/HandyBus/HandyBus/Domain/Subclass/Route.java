package HandyBus.HandyBus.Domain.Subclass;

import jakarta.persistence.CollectionTable;
import jakarta.persistence.ElementCollection;
import jakarta.persistence.Embeddable;
import jakarta.persistence.JoinColumn;

import java.time.LocalTime;
import java.util.List;
import java.util.stream.Collectors;

@Embeddable
public class Route {
    @ElementCollection
    @CollectionTable(name = "bus_route_locations", joinColumns = @JoinColumn(name = "bus_id"))
    private List<LocationTime> locationTimes; // List of location and time information

    public List<Address> getLocations() {
        return locationTimes.stream().map(LocationTime.getAddress()).collect(Collectors.toList());
    }

    public List<LocalTime> getTimes() {
        return locationTimes.stream().map(LocationTime.getTime()).collect(Collectors.toList());
    }
}

