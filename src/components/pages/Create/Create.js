import React from 'react'
import Hero from '../../Hero'
import {CreateObjOne} from './Data'
import Form from '../../Form/Form'
import Upload from '../../Upload'
import Footer from '../../Footer'

function Create() {
    return (
        <>
            <Hero {...CreateObjOne} />
            <Upload />
            <Form />
            <Footer />
        </>
    )
}

export default Create