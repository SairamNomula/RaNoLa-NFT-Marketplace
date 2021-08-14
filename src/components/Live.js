import React from 'react'
import {Link} from 'react-router-dom'
import {BsBrush} from 'react-icons/bs'
import {FaRobot} from 'react-icons/fa'
import {FcCamera} from 'react-icons/fc'
import {RiBrush4Fill} from 'react-icons/ri'
import {IconContext} from 'react-icons/lib'
import {Button} from './Button'
import './Live.css'

function Live() {
    return (
        <IconContext.Provider value={{color: '#fff', size: 64}}>
        <div>
            <div className="Live__section">
                <div className="Live__wrapper">
                    <h1 className="Live__heading">Auctions</h1>
                    <h3 className="Live__subheading">Live Auctions ---</h3>
                    <div className="Live__container">
                        <Link to='/connect' className='Live__container-card'>
                            <div className="Live__container-cardInfo">
                                <div className="icon">
                                    <BsBrush />
                                </div>
                                <h3>Illusions</h3>
                                <ul className='Live__container-features'>
                                    <li>by Sairam Nomula</li>
                                    <li>1.7BNB</li>
                                </ul>
                                <Button buttonSize='btn--wide' buttonColor='primary'>
                                    View more
                                </Button>
                            </div>
                        </Link>

                        <Link to='/connect' className='Live__container-card'>
                            <div className="Live__container-cardInfo">
                                <div className="icon">
                                    <FcCamera />
                                </div>
                                <h3>Photography</h3>
                                <ul className='Live__container-features'>
                                    <li>by Sairam Nomula</li>
                                    <li>1.7BNB</li>
                                </ul>
                                <Button buttonSize='btn--wide' buttonColor='purple'>
                                    View more
                                </Button>
                            </div>
                        </Link>
                        
                        <Link to='/connect' className='Live__container-card'>
                            <div className="Live__container-cardInfo">
                                <div className="icon">
                                    <FaRobot />
                                </div>
                                <h3>Robotic Arts</h3>
                                <ul className='Live__container-features'>
                                    <li>by Sairam Nomula</li>
                                    <li>1.7BNB</li>
                                </ul>
                                <Button buttonSize='btn--wide' buttonColor='primary'>
                                    View more
                                </Button>
                            </div>
                        </Link>

                        <Link to='/connect' className='Live__container-card'>
                            <div className="Live__container-cardInfo">
                                <div className="icon">
                                    <RiBrush4Fill />
                                </div>
                                <h3>Arts</h3>
                                <ul className='Live__container-features'>
                                    <li>by Sairam Nomula</li>
                                    <li>1.7BNB</li>
                                </ul>
                                <Button buttonSize='btn--wide' buttonColor='purple'>
                                    View more
                                </Button>
                            </div>
                        </Link>
                        
                        
                    </div>
                </div>
            </div>
        </div>
        </IconContext.Provider>
    )
}

export default Live
