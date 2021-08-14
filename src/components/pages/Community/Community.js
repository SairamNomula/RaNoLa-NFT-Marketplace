import React from 'react'
import Works from '../../Works'
import Auction from '../../Auction'
import Hero from '../../Hero'
import {homeObjOne,homeObjTwo} from './Data'

function Community() {
    return (
        <>
            <Hero {...homeObjOne} />
            <Works />
            <Hero {...homeObjTwo} />
            <Auction />
        </>
    )
}

export default Community
