import React from 'react'
import { useState } from 'react'
import Header from '../components/Header';
import hamburger from '../img/hamburger-button.svg';
import concert from '../img/concert.svg';
import festival from '../img/festival.svg';
import trip from '../img/trip.svg';
import collecting from '../img/collecting.svg';
import axios from 'axios';
import floating from '../img/floating.svg';

const Home = () => {
    const [floatingOpen, setFloatingOpen] = useState(false);
    const handleFloating = () => {
        setFloatingOpen(!floatingOpen);
    }
    return(
        <div className="main-container">
            <div className="mobile-view">
                <Header />
                <div className="main-body">
                    <div className="carousel">
                        <div className="carousel-poster"></div>
                        <div className="main-icons">
                            <div className="list-all">
                                <img src={hamburger} alt="list-all" />
                                <span className='icon-title'>전체보기</span>
                            </div>
                            <div className="list-concert">
                                <img src={concert} alt="list-concert" />
                                <span className='icon-title'>콘서트</span>
                            </div>
                            <div className="list-festival">
                                <img src={festival} alt="list-festival" />
                                <span className='icon-title'>페스티벌</span>
                            </div>
                            <div className="list-trip">
                                <img id="trip-icon" src={trip} alt="list-trip" />
                                <span id="trip-title" className='icon-title'>여행지</span>
                            </div>
                            <div className="list-collecting">
                                <img src={collecting} alt="list-collecting" />
                                <span className='icon-title'>모집 중</span>
                            </div>
                        </div>
                    </div>
                    <div className="list-wrap">
                        <div className="realtime-list">
                            <span className='list-title'>실시간 대절 리스트</span>
                            <div className="realtime-row">
                                <div className="realtime-list-detail">
                                    <div className="concert-poster"></div>
                                    <span className="concert-title">2023 Jason Korea Tour</span>
                                    <span className="concert-location">파라다이스 시티 일대</span>
                                </div>
                                <div className="realtime-list-detail">
                                    <div className="concert-poster"></div>
                                    <span className="concert-title">2023 Jason Korea Tour</span>
                                    <span className="concert-location">파라다이스 시티 일대</span>
                                </div>
                                <div className="realtime-list-detail">
                                    <div className="concert-poster"></div>
                                    <span className="concert-title">2023 Jason Korea Tour</span>
                                    <span className="concert-location">파라다이스 시티 일대</span>
                                </div>
                                <div className="realtime-list-detail">
                                    <div className="concert-poster"></div>
                                    <span className="concert-title">2023 Jason Korea Tour</span>
                                    <span className="concert-location">파라다이스 시티 일대</span>
                                </div>
                            </div>
                        </div>
                        <div className="concert-list">
                            <span className='list-title'>콘서트 대절 리스트</span>
                            <div className="realtime-row">
                                <div className="realtime-list-detail">
                                    <div className="concert-poster"></div>
                                    <span className="concert-title">2023 Jason Korea Tour</span>
                                    <span className="concert-location">파라다이스 시티 일대</span>
                                </div>
                                <div className="realtime-list-detail">
                                    <div className="concert-poster"></div>
                                    <span className="concert-title">2023 Jason Korea Tour</span>
                                    <span className="concert-location">파라다이스 시티 일대</span>
                                </div>
                                <div className="realtime-list-detail">
                                    <div className="concert-poster"></div>
                                    <span className="concert-title">2023 Jason Korea Tour</span>
                                    <span className="concert-location">파라다이스 시티 일대</span>
                                </div>
                                <div className="realtime-list-detail">
                                    <div className="concert-poster"></div>
                                    <span className="concert-title">2023 Jason Korea Tour</span>
                                    <span className="concert-location">파라다이스 시티 일대</span>
                                </div>
                            </div>
                        </div>
                    </div>
                    <img className='floating-btn' src={floating} alt="floating button" onClick={handleFloating} />
                    {floatingOpen && (
                        <div className="overlay">
                            {/* 여기에 추가 플로팅 버튼 구현 */}
                        </div>
                    )}
                </div>
            </div>
        </div>
    )
}

export default Home