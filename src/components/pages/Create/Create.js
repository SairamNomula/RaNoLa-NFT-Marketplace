import React from 'react'
import Hero from '../../Hero'
import {CreateObjOne} from './Data'
import Footer from '../../Footer'
function Create() {
    return (
        <>
            <Hero {...CreateObjOne} />
            <Footer />
        </>
    )
}

export default Create