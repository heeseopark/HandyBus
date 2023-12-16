import React from 'react'
import Logo from '../img/logo.svg'

const Header = () => {
  return (
    <div className="header_wrap" >
        <img className="logo" src={Logo} alt="logo" />
    </div>
  )
}

export default Header