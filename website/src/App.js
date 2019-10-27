import React, { useEffect } from "react"
import styled from "styled-components"
import { Stitch } from "mongodb-stitch-browser-sdk"
import OrdersList from "./OrdersList"
import icon from "./icon.svg"
import { UserApiKeyCredential } from "mongodb-stitch-core-sdk"

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

const ClearOrders = styled.p`
  color: #1b1b1b;
  font-size: 1.8rem;
  cursor: pointer;
  margin-bottom: 24px;
`

const API_KEY =
  "7wznwkK7WjbhrtYqoAMAhhNWIc4d6nRtOuLmZK3jLuu0a0DAvnH87yB2DKgVpixX"
const APP_ID = "waiter-zxnop"

const client = Stitch.initializeDefaultAppClient(APP_ID)

export default function App() {
  useEffect(() => {
    client.auth.loginWithCredential(new UserApiKeyCredential(API_KEY))
  }, [])

  function clearOrders() {
    client.callFunction("delete_orders", [])
  }

  return (
    <Container>
      <Nav>
        <Icon src={icon} alt="Icon" />
        <Title>wAIter</Title>
      </Nav>

      <OrdersList client={client} />

      <ClearOrders onClick={clearOrders}>Clear Orders</ClearOrders>
    </Container>
  )
}
