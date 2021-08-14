import React from 'react'
import {Link} from 'react-router-dom'
import {BsBrush} from 'react-icons/bs'
import {FaRobot} from 'react-icons/fa'
import {FcCamera} from 'react-icons/fc'
import {RiBrush4Fill} from 'react-icons/ri'
import {IconContext} from 'react-icons/lib'
import {Button} from './Button'
import './Auction.css'

function Auction() {
    return (
        <IconContext.Provider value={{color: '#fff', size: 64}}>
        <div>
            <div className="auction__section">
                <div className="auction__wrapper">
                    <h1 className="auction__heading">Popular collections</h1>
                    <h3 className="auction__subheading">Most popular ---</h3>
                    <div className="auction__container">
                        <Link to='/connect' className='auction__container-card'>
                            <div className="auction__container-cardInfo">
                                <div className="icon">
                                    <BsBrush />
                                </div>
                                <h3>Illusions</h3>
                                <Button buttonSize='btn--wide' buttonColor='primary'>
                                    View more
                                </Button>
                            </div>
                        </Link>

                        <Link to='/connect' className='auction__container-card'>
                            <div className="auction__container-cardInfo">
                                <div className="icon">
                                    <FcCamera />
                                </div>
                                <h3>Photography</h3>
                                <Button buttonSize='btn--wide' buttonColor='purple'>
                                    View more
                                </Button>
                            </div>
                        </Link>
                        
                        <Link to='/connect' className='auction__container-card'>
                            <div className="auction__container-cardInfo">
                                <div className="icon">
                                    <FaRobot />
                                </div>
                                <h3>Robotic Arts</h3>
                                <Button buttonSize='btn--wide' buttonColor='primary'>
                                    View more
                                </Button>
                            </div>
                        </Link>

                        <Link to='/connect' className='auction__container-card'>
                            <div className="auction__container-cardInfo">
                                <div className="icon">
                                    <RiBrush4Fill />
                                </div>
                                <h3>Arts</h3>
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

export default Auction
