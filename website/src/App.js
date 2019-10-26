import React from "react"
import styled from "styled-components"
import OrdersList from "./OrdersList"
import icon from "./icon.svg"

const Container = styled.div`
  background-color: #f9f9f9;
  height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
`

const Nav = styled.nav`
  background-color: #13bbd2;
  padding: 16px;
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
`

const Icon = styled.img`
  width: 40px;
  height: 40px;
  margin-right: 8px;
`

const Title = styled.h1`
  color: white;
  font-weight: 500;
  font-size: 2.4rem;
`

export default function App() {
  return (
    <Container>
      <Nav>
        <Icon src={icon} alt="Icon" />
        <Title>wAIter</Title>
      </Nav>

      <OrdersList />
    </Container>
  )
}
