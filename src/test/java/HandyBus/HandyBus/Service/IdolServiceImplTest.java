package HandyBus.HandyBus.Service;

import HandyBus.HandyBus.DTO.IdolDTO;
import HandyBus.HandyBus.DTO.IdolSignUpDTO;
import HandyBus.HandyBus.Domain.IdolDomain;
import HandyBus.HandyBus.Repository.IdolRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.boot.test.context.SpringBootTest;

import java.util.Arrays;
import java.util.List;

import static org.hamcrest.Matchers.any;
import static org.junit.jupiter.api.Assertions.*;


@ExtendWith(MockitoExtension.class)
@SpringBootTest
public class IdolServiceImplTest {

//    @Mock
//    private IdolRepository idolRepository;
//
//    @Mock
//    private ConcertServiceImpl concertServiceImpl;
//
//    @InjectMocks
//    private IdolServiceImpl idolService;
//
//    // JUnit 5에서는 @Before 대신 @BeforeEach를 사용합니다.
//    @BeforeEach
//    public void setUp() {
//        // MockitoAnnotations.initMocks(this); 는 필요 없습니다.
//        // @ExtendWith(MockitoExtension.class) 어노테이션이 초기화를 처리합니다.
//    }
//
//    @Test
//    public void testCreateIdol() {
//        // given: 필요한 데이터와 예상 결과를 설정
//        IdolSignUpDTO signUpDTO = new IdolSignUpDTO(/* 파라미터 설정 */);
//        IdolDomain expectedIdolDomain = new IdolDomain(/* 파라미터 설정 */);
//        Mockito.when(idolRepository.save(any(IdolDomain.class))).thenReturn(expectedIdolDomain);
//
//        // when: 실제 메서드 실행
//        IdolDTO result = idolService.createIdol(signUpDTO);
//
//        // then: 결과 검증
//        assertNotNull(result);
//        assertEquals(expectedIdolDomain.getIdolId(), result.getIdolId());
//        // 기타 필드들에 대한 검증
//    }
//
//    @Test
//    public void testFindAll() {
//        // given
//        List<IdolDomain> idolDomains = Arrays.asList(/* IdolDomain 객체 목록 */);
//        Mockito.when(idolRepository.findAll()).thenReturn(idolDomains);
//
//        // when
//        List<IdolDTO> result = idolService.findAll();
//
//        // then
//        assertNotNull(result);
//        assertFalse(result.isEmpty());
//        assertEquals(idolDomains.size(), result.size());
//    }

}
