import React from 'react'
import styled from 'styled-components'

const Container = styled.header`
    width: 100%;
    background: grey;
    text-align: center;
    padding: 1rem;
`

const Header = () =>
    <Container>
        <h1>Sampler Box</h1>
    </Container>

export default Header;
