import React, {useState, useEffect} from 'react'
import {Link} from 'react-router-dom'
import {RiCopperCoinLine} from 'react-icons/ri'
import {FaBars, FaTimes} from 'react-icons/fa'
import {Button} from '../Button'
import './Navbar.css'
import {IconContext} from 'react-icons/lib';
import {injected} from '../Wallet/connector';
import { useWeb3React } from '@web3-react/core';


function Navbar() {

    const [click, setClick] = useState(false)
    const [button, setButton] =useState(true)
    const handleClick = () => setClick(!click)
    const closeMobileMenu = () => setClick(false)
    const showButton =() => {
        if(window.innerWidth <= 968) {
            setButton(false)
        } else {
            setButton(true);
        }
    }

    useEffect(() => {
        showButton()
    }, [])

    window.addEventListener('resize', showButton)

    const {active, account, activate, deactivate} = useWeb3React()
    
    async function connect(){
        try {
            await activate(injected)
        } catch (e){
            console.log(e)
        }
    }

    async function disconnect(){
        try {
            deactivate()
        } catch (e){
            console.log(e)
        }
    }

    return (
        <>
        <IconContext.Provider value={{ color: '#fff'}}>
           <div className="navbar">
            <div className="navbar-container container">
                <Link to='/' className="navbar-logo" onClick={closeMobileMenu}>
                    <RiCopperCoinLine className="navbar-icon" />
                    RaNoLa
                </Link>
                <div className="menu-icon" onClick={handleClick}>
                    {click ? <FaTimes /> : <FaBars />}
                </div>
                <ul className={click ? 'nav-menu active' : 'nav-menu'}>
                    <li className='nav-item'>
                        <Link to='/'className="nav-links" onClick={closeMobileMenu}>
                            Home
                        </Link>
                    </li>
                    <li className='nav-item'>
                        <Link to='/Auctions' className="nav-links" onClick={closeMobileMenu}>
                            Auctions
                        </Link>
                    </li>
                    <li className='nav-item'>
                        <Link to='/Community' className="nav-links" onClick={closeMobileMenu}>
                            Community
                        </Link>
                    </li>
                    <li className='nav-item'>
                        <Link to='/Create' className="nav-links" onClick={closeMobileMenu}>
                            Create
                        </Link>
                    </li>
                    <li className="nav-btn">
                        {/* {click ? (
                            <Link to="/"  onClick={handleClick} className="btn-link">
                                <Button buttonStyle='btn--outline'>Connected</Button>
                            </Link>
                        ): (
                            <Link to="/Connect" onClick={handleClick} className="btn-link">
                                <Button buttonStyle='btn--outline'>Connect Wallet</Button>
                            </Link>
                        )} */}
                        <Button onClick={connect} buttonStyle='btn--outline'>Connect</Button>
                        {active ? <span>Connect With <b> {account}</b></span> : <span>Not Connected</span>}
                        {/* <Button onClick={disconnect} buttonStyle='btn--outline'>Disconnected</Button>  */}
                    </li>
                </ul>
            </div>
        </div>
        </IconContext.Provider>
        </>
    )
}

export default Navbar;