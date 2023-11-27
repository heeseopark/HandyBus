package HandyBus.HandyBus.Controller.Admin;

import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;

import HandyBus.HandyBus.Controller.Admin.AdminConcertController;
import HandyBus.HandyBus.DTO.ConcertDTO;
import HandyBus.HandyBus.Service.ConcertServiceImpl;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;

import java.util.ArrayList;
import java.util.List;

@ExtendWith(MockitoExtension.class)
public class AdminConcertControllerTest {

    @Mock
    private ConcertServiceImpl concertServiceImpl;

    @InjectMocks
    private AdminConcertController adminConcertController;

    @Test
    public void testGetConcertAndReservationList() {
        // Setup
        List<ConcertDTO> mockConcertList = new ArrayList<>();
        mockConcertList.add(new ConcertDTO()); // Add mock ConcertDTO
        // ... Populate the list as necessary for your test

        when(concertServiceImpl.findUpcomingConcerts()).thenReturn(mockConcertList);

        // Execution
        ResponseEntity<List<ConcertDTO>> response = adminConcertController.getConcertAndReservationList();

        // Assertions
        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(mockConcertList, response.getBody());
        assertNotNull(response.getBody());
        // ... Additional assertions as needed
    }
}

